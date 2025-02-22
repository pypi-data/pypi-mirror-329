import asyncio
import os
import time
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from bhumi.base_client import BaseLLMClient, LLMConfig
from google import genai
from openai import AsyncOpenAI
import anthropic
import aiohttp
import dotenv
from typing import List, Dict
import statistics
import httpx
import numpy as np
from pydantic import BaseModel
import pandas as pd

dotenv.load_dotenv()

# Provider configurations
PROVIDER_CONFIGS = {
    'openai': {
        'api_key': os.getenv("OPENAI_API_KEY"),
        'model': "gpt-4o-mini",
        'base_url': "https://api.openai.com/v1"
    },
    'gemini': {
        'api_key': os.getenv("GEMINI_API_KEY"),
        'model': "gemini-1.5-flash-8b",
        'base_url': "https://generativelanguage.googleapis.com/v1/models"
    },
    'anthropic': {
        'api_key': os.getenv("ANTHROPIC_API_KEY"),
        'model': "claude-3-haiku-20240307",
        'base_url': "https://api.anthropic.com/v1",
        'max_tokens': 1024  # Add max_tokens for Anthropic
    }
}

# Test prompts
TEST_PROMPTS = [
    "What is 2+2?",
    "Name a color",
    "Say hello",
    "Count to 3",
    "Name a fruit"
]

class PromptRequest(BaseModel):
    prompt: str

def create_provider_apps(provider: str):
    """Create FastAPI apps for a specific provider"""
    bhumi_app = FastAPI()
    native_app = FastAPI()
    raw_app = FastAPI()
    
    config = PROVIDER_CONFIGS[provider]
    bhumi_client = BaseLLMClient(LLMConfig(
        api_key=config['api_key'],
        model=f"{provider}/{config['model']}",
        debug=False,
    ), max_concurrent=100)
    
    # Bhumi Implementation
    @bhumi_app.post("/generate")
    async def generate_bhumi(request: PromptRequest):
        response = await bhumi_client.completion([
            {"role": "user", "content": request.prompt}
        ])
        return {"response": response["text"]}
    
    # Native Implementation
    @native_app.post("/generate")
    async def generate_native(request: PromptRequest):
        if provider == 'gemini':
            genai_client = genai.Client(api_key=config['api_key'])
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: genai_client.models.generate_content(
                    model=config['model'],
                    contents=request.prompt
                )
            )
            return {"response": response.text}
        elif provider == 'openai':
            openai_client = AsyncOpenAI(api_key=config['api_key'])
            response = await openai_client.chat.completions.create(
                model=config['model'],
                messages=[{"role": "user", "content": request.prompt}]
            )
            return {"response": response.choices[0].message.content}
        elif provider == 'anthropic':
            anthropic_client = anthropic.Anthropic(api_key=config['api_key'])
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: anthropic_client.messages.create(
                    model=config['model'],
                    max_tokens=config['max_tokens'],
                    messages=[
                        {"role": "user", "content": request.prompt}
                    ]
                )
            )
            return {"response": response.content[0].text}
    
    # Raw Implementation
    @raw_app.post("/generate")
    async def generate_raw(request: PromptRequest):
        if provider == 'gemini':
            url = f"{config['base_url']}/{config['model']}:generateContent"
            headers = {"Content-Type": "application/json"}
            params = {"key": config['api_key']}
            data = {
                "contents": [{
                    "parts": [{"text": request.prompt}],
                    "role": "user"
                }]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, params=params, json=data) as resp:
                    response = await resp.json()
                    return {"response": response["candidates"][0]["content"]["parts"][0]["text"]}
        elif provider == 'anthropic':
            url = f"{config['base_url']}/messages"
            headers = {
                "x-api-key": config['api_key'],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            data = {
                "model": config['model'],
                "max_tokens": config['max_tokens'],
                "messages": [
                    {"role": "user", "content": request.prompt}
                ]
            }
        else:  # OpenAI
            url = f"{config['base_url']}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['api_key']}"
            }
            data = {
                "model": config['model'],
                "messages": [{"role": "user", "content": request.prompt}]
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                response = await resp.json()
                if provider == 'gemini':
                    return {"response": response["candidates"][0]["content"]["parts"][0]["text"]}
                elif provider == 'anthropic':
                    return {"response": response["content"][0]["text"]}
                else:
                    return {"response": response["choices"][0]["message"]["content"]}
    
    # Add health check endpoints
    for app in [bhumi_app, native_app, raw_app]:
        @app.get("/health")
        async def health():
            return {"status": "ok"}
    
    return bhumi_app, native_app, raw_app

async def load_test_server(port: int, num_requests: int) -> Dict:
    """Load test a server with concurrent requests"""
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Create tasks for all requests
        tasks = []
        for _ in range(num_requests):
            prompt = np.random.choice(TEST_PROMPTS)
            tasks.append(client.post(
                f"http://localhost:{port}/generate",
                json={"prompt": prompt},
                timeout=30.0
            ))
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process responses
        successful_responses = []
        failed_requests = 0
        
        for response in responses:
            if isinstance(response, Exception):
                print(f"Request error: {str(response)}")
                failed_requests += 1
            elif response.status_code == 200:
                successful_responses.append(response.elapsed.total_seconds())
            else:
                print(f"Request failed with status {response.status_code}")
                failed_requests += 1
        
        end_time = time.time()
        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        return {
            'total_time': end_time - start_time,
            'avg_response_time': statistics.mean(successful_responses) if successful_responses else 0,
            'peak_memory': peak_memory,
            'memory_increase': peak_memory - initial_memory,
            'successful_requests': len(successful_responses),
            'failed_requests': failed_requests
        }

async def verify_server(port: int) -> bool:
    """Verify server is up and responding"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://localhost:{port}/health")
            return response.status_code == 200
        except Exception as e:
            print(f"Server verification failed: {str(e)}")
            return False

def plot_server_results(results: Dict):
    """Plot server benchmark results"""
    plt.figure(figsize=(20, 10))
    implementations = list(results.keys())
    colors = {
        # Bhumi implementations all in coral
        'Bhumi (OpenAI)': '#FF7F50',    # Coral
        'Bhumi (Gemini)': '#FF7F50',    # Coral
        'Bhumi (Anthropic)': '#FF7F50', # Coral
        
        # Native implementations in provider colors
        'Native (OpenAI)': '#00A67E',   # OpenAI Green
        'Native (Gemini)': '#4285F4',   # Google Blue
        'Native (Anthropic)': '#000000', # Anthropic Black
        
        # Raw implementations in provider colors
        'Raw (OpenAI)': '#00A67E',      # OpenAI Green
        'Raw (Gemini)': '#4285F4',      # Google Blue
        'Raw (Anthropic)': '#000000'    # Anthropic Black
    }
    
    # Create a case-insensitive color mapping
    color_map = {k.lower(): v for k, v in colors.items()}
    
    # Use the case-insensitive mapping for colors
    impl_colors = [color_map[impl.lower()] for impl in implementations]
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    
    # Plot 1: Total Time
    times = [results[impl]['avg_total_time'] for impl in implementations]
    axes[0, 0].bar(implementations, times, color=impl_colors)
    axes[0, 0].set_title('Average Total Processing Time')
    axes[0, 0].set_ylabel('Time (seconds)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot 2: Response Time
    resp_times = [results[impl]['avg_response_time'] for impl in implementations]
    axes[0, 1].bar(implementations, resp_times, color=impl_colors)
    axes[0, 1].set_title('Average Response Time per Request')
    axes[0, 1].set_ylabel('Time (seconds)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Plot 3: Memory Usage
    memory = [results[impl]['avg_peak_memory'] for impl in implementations]
    axes[1, 0].bar(implementations, memory, color=impl_colors)
    axes[1, 0].set_title('Average Peak Memory Usage')
    axes[1, 0].set_ylabel('Memory (MB)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Plot 4: Success Rate
    success_rates = [results[impl]['avg_success_rate'] for impl in implementations]
    axes[1, 1].bar(implementations, success_rates, color=impl_colors)
    axes[1, 1].set_title('Average Success Rate')
    axes[1, 1].set_ylabel('Success Rate (%)')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"benchmarks/plots/llm_comparison_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_filename, bbox_inches='tight')
    print(f"\n📈 Plot saved as: {plot_filename}")

def plot_bhumi_speedup(results: Dict):
    """Plot Bhumi's relative performance improvement"""
    plt.figure(figsize=(15, 8))
    
    # Create case-insensitive lookup for results
    results_lookup = {k.lower(): v for k, v in results.items()}
    
    providers = ['openai', 'gemini', 'anthropic']
    metrics = ['Response Time', 'Memory Usage']
    
    # Calculate speedup ratios
    speedups = {provider: {} for provider in providers}
    for provider in providers:
        bhumi_key = f'bhumi ({provider})'.lower()
        native_key = f'native ({provider})'.lower()
        raw_key = f'raw ({provider})'.lower()
        
        bhumi_time = results_lookup[bhumi_key]['avg_response_time']
        bhumi_memory = results_lookup[bhumi_key]['avg_peak_memory']
        
        native_time = results_lookup[native_key]['avg_response_time']
        native_memory = results_lookup[native_key]['avg_peak_memory']
        
        raw_time = results_lookup[raw_key]['avg_response_time']
        raw_memory = results_lookup[raw_key]['avg_peak_memory']
        
        speedups[provider] = {
            'Native Time': native_time / bhumi_time,
            'Raw Time': raw_time / bhumi_time,
            'Native Memory': native_memory / bhumi_memory,
            'Raw Memory': raw_memory / bhumi_memory
        }
    
    # Create grouped bar plot
    x = np.arange(len(providers))
    width = 0.2
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot time speedup
    ax1.bar(x - width/2, [speedups[p]['Native Time'] for p in providers], width, label='vs Native', color='#4285F4')
    ax1.bar(x + width/2, [speedups[p]['Raw Time'] for p in providers], width, label='vs Raw', color='#00A67E')
    ax1.set_ylabel('Speedup Factor (higher is better)')
    ax1.set_title('Response Time Improvement\n(Bhumi vs Other Implementations)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(providers)
    ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    ax1.legend()
    
    # Add value labels
    for i, provider in enumerate(providers):
        ax1.text(i - width/2, speedups[provider]['Native Time'], 
                f'{speedups[provider]["Native Time"]:.1f}x', 
                ha='center', va='bottom')
        ax1.text(i + width/2, speedups[provider]['Raw Time'],
                f'{speedups[provider]["Raw Time"]:.1f}x',
                ha='center', va='bottom')
    
    # Plot memory improvement
    ax2.bar(x - width/2, [speedups[p]['Native Memory'] for p in providers], width, label='vs Native', color='#4285F4')
    ax2.bar(x + width/2, [speedups[p]['Raw Memory'] for p in providers], width, label='vs Raw', color='#00A67E')
    ax2.set_ylabel('Memory Efficiency Factor (higher is better)')
    ax2.set_title('Memory Usage Improvement\n(Bhumi vs Other Implementations)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(providers)
    ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    ax2.legend()
    
    # Add value labels
    for i, provider in enumerate(providers):
        ax2.text(i - width/2, speedups[provider]['Native Memory'],
                f'{speedups[provider]["Native Memory"]:.1f}x',
                ha='center', va='bottom')
        ax2.text(i + width/2, speedups[provider]['Raw Memory'],
                f'{speedups[provider]["Raw Memory"]:.1f}x',
                ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"benchmarks/plots/bhumi_speedup_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_filename, bbox_inches='tight')
    print(f"\n📈 Speedup plot saved as: {plot_filename}")

def save_results_to_csv(results: Dict):
    """Save benchmark results to CSV with detailed stats"""
    stats = []
    for impl, data in results.items():
        if 'runs' in data:
            avg_data = {
                'Implementation': impl,
                'Total Time (s)': data['avg_total_time'],
                'Response Time (s)': data['avg_response_time'],
                'Peak Memory (MB)': data['avg_peak_memory'],
                'Success Rate (%)': data['avg_success_rate'],
                'Throughput (req/s)': len(data['runs'][0]['successful_requests']) / data['avg_total_time'],
                'Memory Efficiency (req/MB)': len(data['runs'][0]['successful_requests']) / data['avg_peak_memory'],
                'Failed Requests': data['runs'][0]['failed_requests']
            }
            stats.append(avg_data)
    
    df = pd.DataFrame(stats)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"benchmarks/results/benchmark_results_{timestamp}.csv"
    os.makedirs("benchmarks/results", exist_ok=True)
    df.to_csv(csv_filename, index=False)
    print(f"\n📊 Results saved to: {csv_filename}")

async def main(providers: List[str] = None, num_requests: int = 15, num_runs: int = 1):
    if providers is None:
        providers = ['openai', 'gemini', 'anthropic']
    
    # Validate providers
    valid_providers = set(PROVIDER_CONFIGS.keys())
    providers = [p.lower() for p in providers]
    if not all(p in valid_providers for p in providers):
        raise ValueError(f"Invalid provider. Must be one of: {valid_providers}")
    
    # Create apps and prepare benchmark tasks
    results = {}
    port = 8000
    benchmark_tasks = []
    
    for provider in providers:
        bhumi_app, native_app, raw_app = create_provider_apps(provider)
        
        for impl_type, app in [
            ('Bhumi', bhumi_app),
            ('Native', native_app),
            ('Raw', raw_app)
        ]:
            name = f"{impl_type} ({provider.title()})"
            results[name] = {'runs': [], 'port': port}
            
            # Create server configuration
            config = uvicorn.Config(app, port=port, log_level="info")
            server = uvicorn.Server(config)
            
            # Create benchmark task
            benchmark_tasks.append((name, server, port, num_requests, num_runs))
            port += 1
    
    # Run benchmarks concurrently for each implementation
    async def run_benchmark(name, server, port, num_requests, num_runs):
        server_task = asyncio.create_task(server.serve())
        await asyncio.sleep(2)
        
        if not await verify_server(port):
            print(f"❌ {name} server failed to start properly")
            return name, []
        
        print(f"✅ {name} server started successfully")
        
        # Run tests
        run_results = []
        for run in range(num_runs):
            print(f"\n🔄 Run {run + 1}/{num_runs} for {name}")
            run_results.append(await load_test_server(port, num_requests))
        
        # Stop server
        server.should_exit = True
        await server_task
        
        return name, run_results
    
    # Execute all benchmarks concurrently
    benchmark_results = await asyncio.gather(
        *(run_benchmark(name, server, port, num_requests, num_runs) 
          for name, server, port, num_requests, num_runs in benchmark_tasks)
    )
    
    # Process results
    for name, run_results in benchmark_results:
        if run_results:  # Only process if we got results
            results[name]['runs'] = run_results
            # Calculate averages
            results[name]['avg_total_time'] = statistics.mean(r['total_time'] for r in run_results)
            results[name]['avg_response_time'] = statistics.mean(r['avg_response_time'] for r in run_results)
            results[name]['avg_peak_memory'] = statistics.mean(r['peak_memory'] for r in run_results)
            results[name]['avg_success_rate'] = statistics.mean(r['successful_requests']/num_requests * 100 for r in run_results)
    
    # Plot and save results
    plot_server_results(results)
    plot_bhumi_speedup(results)
    save_results_to_csv(results)
    return results

if __name__ == "__main__":
    # Example: benchmark specific providers
    asyncio.run(main(['openai', 'gemini', 'anthropic'], num_requests=30, num_runs=1)) 