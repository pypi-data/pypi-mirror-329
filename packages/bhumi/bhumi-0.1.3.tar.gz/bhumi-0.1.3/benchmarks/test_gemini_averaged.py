import asyncio
import os
import time
import litellm
import aiohttp
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
from bhumi.client import GeminiClient
from google import genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyDXWUOcqUw3FF3o3WaftJkSZDJRX7rGtys"
# Configuration
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDXWUOcqUw3FF3o3WaftJkSZDJRX7rGtys")
MODEL = "gemini-1.5-flash-8b"
NUM_RUNS = 3  # Number of times to run each test
MAX_CONCURRENT = 30

# Initialize Google GenAI client
genai_client = genai.Client()

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
    """Test Gemini via LiteLLM with async/await"""
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
                        model=f"gemini/{MODEL}",
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
    """Test Gemini via native aiohttp"""
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
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
                headers = {"Content-Type": "application/json"}
                params = {"key": API_KEY}
                data = {
                    "contents": [{
                        "parts": [{"text": prompt}],
                        "role": "user"
                    }]
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, params=params, json=data) as resp:
                        response = await resp.json()
                
                current_memory = get_process_memory()
                peak_memory = max(peak_memory, current_memory)
                elapsed = time.time() - start_time
                text = response["candidates"][0]["content"]["parts"][0]["text"]
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
    """Test Gemini via Bhumi async client"""
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    
    client = GeminiClient(
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
                    model=f"gemini/{MODEL}",
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

async def test_google_genai_async():
    """Test Gemini via Google's official client"""
    print("\n🚀 Testing Google GenAI (Async)...")
    
    total_start = time.time()
    responses = []
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    semaphore = asyncio.Semaphore(30)
    
    async def process_prompt(prompt):
        nonlocal peak_memory
        async with semaphore:
            start_time = time.time()
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: genai_client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )
                )
                
                current_memory = get_process_memory()
                peak_memory = max(peak_memory, current_memory)
                
                elapsed = time.time() - start_time
                responses.append((prompt, response.text, elapsed))
                print(f"Response time: {elapsed:.2f}s")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - total_start
    memory_used = peak_memory - initial_memory
    
    print("\nGoogle GenAI Results:")
    print("=" * 60)
    print(f"Total time: {total_time:.2f}s")
    print(f"Peak memory usage: {peak_memory:.2f}MB")
    print(f"Memory increase: {memory_used:.2f}MB")
    print("=" * 60)
    
    return {
        'responses': responses,
        'total_time': total_time,
        'peak_memory': peak_memory
    }

async def run_averaged_tests():
    """Run all tests multiple times and average the results"""
    results = {
        'LiteLLM(async)': [],
        'Native(aiohttp)': [],
        'Bhumi(native)': [],
        'Google GenAI(async)': []
    }
    
    for run in range(NUM_RUNS):
        print(f"\n🔄 Run {run + 1}/{NUM_RUNS}")
        
        print("\n🚀 Testing LiteLLM...")
        results['LiteLLM(async)'].append(await test_litellm_async())
        
        print("\n🚀 Testing Native...")
        results['Native(aiohttp)'].append(await test_native_async())
        
        print("\n🚀 Testing Bhumi...")
        results['Bhumi(native)'].append(await test_bhumi_async())
        
        print("\n🚀 Testing GenAI...")
        results['Google GenAI(async)'].append(await test_google_genai_async())
    
    # Calculate averages
    averaged_results = {}
    for client in results:
        avg_time = sum(r['total_time'] for r in results[client]) / NUM_RUNS
        avg_memory = sum(r['peak_memory'] for r in results[client]) / NUM_RUNS
        
        print(f"\n📊 {client} Averaged Results:")
        print(f"Time: {avg_time:.2f}s")
        print(f"Memory: {avg_memory:.2f}MB")
        
        averaged_results[client] = {
            'total_time': avg_time,
            'peak_memory': avg_memory,
            'responses': results[client][0]['responses']  # Keep first run's responses
        }
    
    return averaged_results

def plot_averaged_results(results):
    """Plot comparison graphs for averaged results"""
    plt.figure(figsize=(15, 5))
    
    implementations = list(results.keys())
    colors = {
        'LiteLLM(async)': '#666666',
        'Native(aiohttp)': '#999999',
        'Bhumi(native)': '#90EE90',
        'Google GenAI(async)': '#4285F4'
    }
    
    # Plot 1: Total Response Time
    plt.subplot(1, 3, 1)
    times = [results[impl]['total_time'] for impl in implementations]
    bars = plt.bar(implementations, times, color=[colors[impl] for impl in implementations])
    plt.title('Average Total Response Time')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
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
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"gemini_averaged_comparison_{timestamp}.png"
    plt.savefig(plot_filename)
    print(f"\n📈 Plot saved as: {plot_filename}")

if __name__ == "__main__":
    averaged_results = asyncio.run(run_averaged_tests())
    plot_averaged_results(averaged_results) 