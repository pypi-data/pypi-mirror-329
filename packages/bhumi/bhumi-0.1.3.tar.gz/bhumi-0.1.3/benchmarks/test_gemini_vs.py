import asyncio
import os
import json
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
    print("\n🚀 Testing Gemini via LiteLLM (Async)...")
    
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
                print(f"Response time: {elapsed:.2f}s")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - total_start
    memory_used = peak_memory - initial_memory
    
    print("\nLiteLLM Async Results:")
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

async def test_native_async():
    """Test Gemini via native aiohttp"""
    print("\n🚀 Testing Gemini via native aiohttp...")
    
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
                print(f"Response time: {elapsed:.2f}s")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - total_start
    memory_used = peak_memory - initial_memory
    
    print("\nNative Async Results:")
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

async def test_bhumi_async():
    """Test Gemini via Bhumi async client"""
    print("\n🚀 Testing Gemini via Bhumi...")
    
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    
    client = GeminiClient(
        max_concurrent=30,
        model=MODEL,
        debug=False
    )
    
    total_start = time.time()
    responses = []
    semaphore = asyncio.Semaphore(30)
    
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
                print(f"Response time: {elapsed:.2f}s")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - total_start
    memory_used = peak_memory - initial_memory
    
    print("\nBhumi Results:")
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

def plot_results(litellm_results, native_results, bhumi_results, genai_results):
    """Plot comparison graphs"""
    plt.figure(figsize=(15, 5))
    
    # Colors for each implementation
    colors = {
        'LiteLLM\n(Async)': '#666666',
        'Native\n(aiohttp)': '#999999',
        'Bhumi\n(Async)': '#90EE90',
        'Google\nGenAI': '#4285F4'  # Google blue
    }
    
    implementations = list(colors.keys())
    
    # Plot 1: Total Response Time
    plt.subplot(1, 3, 1)
    total_times = [
        litellm_results['total_time'],
        native_results['total_time'],
        bhumi_results['total_time'],
        genai_results['total_time']
    ]
    
    bars = plt.bar(implementations, total_times, color=[colors[i] for i in implementations])
    plt.title('Total Response Time')
    plt.ylabel('Time (seconds)')
    for bar, val in zip(bars, total_times):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.2f}s', ha='center', va='bottom')
    
    # Plot 2: Throughput
    plt.subplot(1, 3, 2)
    throughput = [len(PROMPTS)/t for t in total_times]
    
    bars = plt.bar(implementations, throughput, color=[colors[i] for i in implementations])
    plt.title('Throughput')
    plt.ylabel('Requests/Second')
    for bar, val in zip(bars, throughput):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.2f}', ha='center', va='bottom')
    
    # Plot 3: Memory Usage
    plt.subplot(1, 3, 3)
    memory_usage = [
        litellm_results['peak_memory'],
        native_results['peak_memory'],
        bhumi_results['peak_memory'],
        genai_results['peak_memory']
    ]
    
    bars = plt.bar(implementations, memory_usage, color=[colors[i] for i in implementations])
    plt.title('Peak Memory Usage')
    plt.ylabel('Memory (MB)')
    for bar, val in zip(bars, memory_usage):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.1f}MB', ha='center', va='bottom')
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"gemini_comparison_{timestamp}.png"
    plt.savefig(plot_filename)
    print(f"\n📈 Plot saved as: {plot_filename}")

if __name__ == "__main__":
    litellm_results = asyncio.run(test_litellm_async())
    print("\n" + "=" * 80 + "\n")
    native_results = asyncio.run(test_native_async())
    print("\n" + "=" * 80 + "\n")
    bhumi_results = asyncio.run(test_bhumi_async())
    print("\n" + "=" * 80 + "\n")
    genai_results = asyncio.run(test_google_genai_async())
    
    # Plot comparison graphs
    plot_results(litellm_results, native_results, bhumi_results, genai_results) 