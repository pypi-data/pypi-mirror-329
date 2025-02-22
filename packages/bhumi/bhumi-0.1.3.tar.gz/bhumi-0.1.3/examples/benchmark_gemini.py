import asyncio
import os
import time
import litellm
import aiohttp
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
from bhumi.base_client import BaseLLMClient, LLMConfig
from google import genai
import dotenv

dotenv.load_dotenv()

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.5-flash-8b"
NUM_RUNS = 3
MAX_CONCURRENT = 30
BATCH_SIZE = 10  # Added batch size configuration

# Initialize Google GenAI client
genai_client = genai.Client(api_key=API_KEY)

# Test prompts (repeated to increase load)
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

async def test_bhumi_async():
    """Test Gemini via Bhumi async client"""
    initial_memory = get_process_memory()
    peak_memory = initial_memory
    
    config = LLMConfig(
        api_key=API_KEY,
        model=f"gemini/{MODEL}",
        debug=False
    )
    
    client = BaseLLMClient(config, max_concurrent=MAX_CONCURRENT)
    total_start = time.time()
    responses = []
    
    # Group prompts into batches
    batches = [PROMPTS[i:i + BATCH_SIZE] for i in range(0, len(PROMPTS), BATCH_SIZE)]
    
    async def process_batch(batch):
        nonlocal peak_memory
        start_time = time.time()
        try:
            # Create messages for all prompts in batch
            messages = [{"role": "user", "content": prompt} for prompt in batch]
            
            # Process batch concurrently
            batch_responses = await asyncio.gather(*[
                client.completion([msg]) for msg in messages
            ])
            
            current_memory = get_process_memory()
            peak_memory = max(peak_memory, current_memory)
            elapsed = time.time() - start_time
            
            # Store responses with their prompts and timing
            for prompt, response in zip(batch, batch_responses):
                responses.append((prompt, response["text"], elapsed/len(batch)))
                
        except Exception as e:
            print(f"Bhumi Batch Error: {str(e)}")
    
    # Process all batches concurrently
    await asyncio.gather(*[process_batch(batch) for batch in batches])
    
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
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
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
            except Exception as e:
                print(f"GenAI Error: {str(e)}")
    
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

async def run_averaged_tests():
    """Run all tests multiple times and average the results"""
    results = {
        'Bhumi(native)': [],
        'Google GenAI(async)': [],
        'Native HTTP': []
    }
    
    for run in range(NUM_RUNS):
        print(f"\n🔄 Run {run + 1}/{NUM_RUNS}")
        
        print("\n🚀 Testing Bhumi...")
        results['Bhumi(native)'].append(await test_bhumi_async())
        
        print("\n🚀 Testing GenAI...")
        results['Google GenAI(async)'].append(await test_google_genai_async())
        
        print("\n🚀 Testing Native HTTP...")
        results['Native HTTP'].append(await test_native_async())
    
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
            'responses': results[client][0]['responses']
        }
    
    return averaged_results

def plot_averaged_results(results):
    """Plot comparison graphs for averaged results"""
    plt.figure(figsize=(15, 5))
    
    implementations = list(results.keys())
    colors = {
        'Bhumi(native)': '#90EE90',
        'Google GenAI(async)': '#4285F4',
        'Native HTTP': '#FF6B6B'  # Added color for native implementation
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
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"gemini_averaged_comparison_{timestamp}.png"
    plt.savefig(plot_filename)
    print(f"\n📈 Plot saved as: {plot_filename}")

if __name__ == "__main__":
    averaged_results = asyncio.run(run_averaged_tests())
    plot_averaged_results(averaged_results) 