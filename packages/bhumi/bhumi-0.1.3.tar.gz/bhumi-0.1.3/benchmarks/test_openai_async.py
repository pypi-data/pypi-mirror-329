import asyncio
import os
import time
import aiohttp
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
from bhumi.client import OpenAIClient
import openai
import litellm
import csv
import logging
from pathlib import Path
import dotenv

from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
# Add after the imports at the top of the file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = Path("benchmark_results")
log_dir.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=log_dir / f"openai_benchmark_{timestamp}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# OPENAI_KEY = "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"

os.environ['OPENAI_API_KEY'] = OPENAI_KEY


# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
NUM_RUNS = 3
MAX_CONCURRENT = 30

# Initialize OpenAI client
openai.api_key = API_KEY

# Test prompts
PROMPTS = [
    "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming",
    "Write a short story about a robot learning to code",
    "What is the capital of France?",
    "What is the capital of Germany?",
    "What is the capital of Italy?",
    "What is the capital of Spain?",
    "What is the capital of Portugal?",
    "Write a haiku about AI",
    "Explain blockchain in one sentence",
    "Tell me a programming joke",
] * 4

def get_process_memory():
    """Get current process memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

async def test_litellm_async():
    """Test OpenAI via LiteLLM with async/await"""
    total_start = time.time()
    responses = []
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    async def process_prompt(prompt):
        nonlocal peak_memory
        async with semaphore:
            start_time = time.time()
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: litellm.completion(
                        model=MODEL,
                        messages=[{"role": "user", "content": prompt}],
                        api_key=API_KEY
                    )
                )
                current_memory = get_process_memory()
                peak_memory = max(peak_memory, current_memory)
                elapsed = time.time() - start_time
                responses.append((prompt, response.choices[0].message.content, elapsed))
            except Exception as e:
                print(f"LiteLLM Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    return {
        'responses': responses,
        'total_time': time.time() - total_start,
        'peak_memory': peak_memory,
        'memory_increase': peak_memory - initial_memory
    }

async def test_native_async():
    """Test OpenAI via native aiohttp"""
    total_start = time.time()
    responses = []
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    async def process_prompt(prompt):
        nonlocal peak_memory
        async with semaphore:
            start_time = time.time()
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data) as resp:
                        response = await resp.json()
                
                current_memory = get_process_memory()
                peak_memory = max(peak_memory, current_memory)
                elapsed = time.time() - start_time
                text = response["choices"][0]["message"]["content"]
                responses.append((prompt, text, elapsed))
            except Exception as e:
                print(f"Native Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    return {
        'responses': responses,
        'total_time': time.time() - total_start,
        'peak_memory': peak_memory,
        'memory_increase': peak_memory - initial_memory
    }

async def test_bhumi_async():
    """Test OpenAI via Bhumi async client"""
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    
    client = OpenAIClient(
        max_concurrent=MAX_CONCURRENT,
        model=MODEL,
        debug=False
    )
    
    total_start = time.time()
    responses = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    async def process_prompt(prompt):
        nonlocal peak_memory
        async with semaphore:
            start_time = time.time()
            try:
                response = await client.acompletion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    api_key=API_KEY
                )
                current_memory = get_process_memory()
                peak_memory = max(peak_memory, current_memory)
                elapsed = time.time() - start_time
                responses.append((prompt, response.text, elapsed))
            except Exception as e:
                print(f"Bhumi Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    return {
        'responses': responses,
        'total_time': time.time() - total_start,
        'peak_memory': peak_memory,
        'memory_increase': peak_memory - initial_memory
    }

async def test_openai_async():
    """Test OpenAI via official async client"""
    total_start = time.time()
    responses = []
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    client = openai.AsyncOpenAI(api_key=API_KEY)
    
    async def process_prompt(prompt):
        nonlocal peak_memory
        async with semaphore:
            start_time = time.time()
            try:
                response = await client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                current_memory = get_process_memory()
                peak_memory = max(peak_memory, current_memory)
                elapsed = time.time() - start_time
                responses.append((prompt, response.choices[0].message.content, elapsed))
            except Exception as e:
                print(f"OpenAI Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    return {
        'responses': responses,
        'total_time': time.time() - total_start,
        'peak_memory': peak_memory,
        'memory_increase': peak_memory - initial_memory
    }

def save_to_csv(results, timestamp):
    """Save benchmark results to CSV"""
    csv_path = log_dir / f"openai_benchmark_{timestamp}.csv"
    
    # Prepare data for CSV
    csv_data = []
    for implementation, data in results.items():
        row = {
            'Implementation': implementation,
            'Average Response Time (s)': data['total_time'],
            'Peak Memory (MB)': data['peak_memory'],
            'Requests/Second': len(PROMPTS) / data['total_time']
        }
        csv_data.append(row)
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)
    
    logging.info(f"Results saved to CSV: {csv_path}")
    print(f"\n📊 Results saved to CSV: {csv_path}")

async def run_averaged_tests():
    """Run all tests multiple times and average the results"""
    results = {
        'LiteLLM(async)': [],
        'Native(aiohttp)': [],
        'Bhumi(native)': [],
        'OpenAI(async)': []
    }
    
    logging.info(f"Starting benchmark tests - {NUM_RUNS} runs with {MAX_CONCURRENT} max concurrent requests")
    logging.info(f"Model: {MODEL}")
    logging.info(f"Number of prompts per run: {len(PROMPTS)}")
    
    for run in range(NUM_RUNS):
        logging.info(f"\nStarting Run {run + 1}/{NUM_RUNS}")
        print(f"\n🔄 Run {run + 1}/{NUM_RUNS}")
        
        for implementation in results.keys():
            print(f"\n🚀 Testing {implementation}...")
            logging.info(f"Testing {implementation}")
            
            if implementation == 'LiteLLM(async)':
                run_result = await test_litellm_async()
            elif implementation == 'Native(aiohttp)':
                run_result = await test_native_async()
            elif implementation == 'Bhumi(native)':
                run_result = await test_bhumi_async()
            else:  # OpenAI(async)
                run_result = await test_openai_async()
            
            results[implementation].append(run_result)
            
            logging.info(f"{implementation} - Run {run + 1} - "
                        f"Time: {run_result['total_time']:.2f}s, "
                        f"Memory: {run_result['peak_memory']:.2f}MB")
    
    # Calculate averages
    averaged_results = {}
    for client in results:
        avg_time = sum(r['total_time'] for r in results[client]) / NUM_RUNS
        avg_memory = sum(r['peak_memory'] for r in results[client]) / NUM_RUNS
        
        print(f"\n📊 {client} Averaged Results:")
        print(f"Time: {avg_time:.2f}s")
        print(f"Memory: {avg_memory:.2f}MB")
        
        logging.info(f"{client} Final Averaged Results - "
                    f"Time: {avg_time:.2f}s, "
                    f"Memory: {avg_memory:.2f}MB")
        
        averaged_results[client] = {
            'total_time': avg_time,
            'peak_memory': avg_memory,
            'responses': results[client][0]['responses']
        }
    
    # Save results to CSV
    save_to_csv(averaged_results, timestamp)
    
    return averaged_results

def plot_averaged_results(results):
    """Plot comparison graphs for averaged results"""
    plt.figure(figsize=(15, 5))
    
    implementations = list(results.keys())
    colors = {
        'LiteLLM(async)': '#666666',
        'Native(aiohttp)': '#999999',
        'Bhumi(native)': '#FF9B82',  # Bhumi's coral orange (hsl(15, 85%, 70%))
        'OpenAI(async)': '#000000'   # Black for OpenAI
    }
    
    # Plot 1: Total Response Time
    plt.subplot(1, 3, 1)
    times = [results[impl]['total_time'] for impl in implementations]
    bars = plt.bar(implementations, times, color=[colors[impl] for impl in implementations])
    plt.title('Average Total Response Time')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45, ha='right')
    for bar, val in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.2f}s', ha='center', va='bottom')
    
    # Plot 2: Throughput
    plt.subplot(1, 3, 2)
    throughput = [len(PROMPTS)/t for t in times]
    bars = plt.bar(implementations, throughput, color=[colors[i] for i in implementations])
    plt.title('Average Throughput')
    plt.ylabel('Requests/Second')
    for bar, val in zip(bars, throughput):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.2f}', ha='center', va='bottom')
    
    # Plot 3: Memory Usage
    plt.subplot(1, 3, 3)
    memory = [results[impl]['peak_memory'] for impl in implementations]
    bars = plt.bar(implementations, memory, color=[colors[i] for i in implementations])
    plt.title('Average Peak Memory Usage')
    plt.ylabel('Memory (MB)')
    for bar, val in zip(bars, memory):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.1f}MB', ha='center', va='bottom')
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"openai_averaged_comparison_{timestamp}.png"
    plt.savefig(plot_filename)
    print(f"\n📈 Plot saved as: {plot_filename}")

if __name__ == "__main__":
    logging.info("Starting benchmark script")
    averaged_results = asyncio.run(run_averaged_tests())
    plot_averaged_results(averaged_results)
    logging.info("Benchmark complete") 