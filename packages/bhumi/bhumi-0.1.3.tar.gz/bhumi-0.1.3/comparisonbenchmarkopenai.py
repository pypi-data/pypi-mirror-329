import os
import json
import time
import asyncio
import requests
from openai import AsyncOpenAI
from bhumi.client import OpenAIClient
import aiohttp

api_key="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"
   
# API Configuration
API_KEY = api_key
MODEL = "gpt-4o-mini"

# Benchmark settings - increased for better concurrency testing
N_REQUESTS = 20  # More requests to test throughput
CONCURRENT_REQUESTS = 10  # Higher concurrency
BATCH_SIZE = 5  # Process in batches

async def make_direct_request(client: None, prompt: str) -> tuple[float, str]:
    """Make a direct request to OpenAI API"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ]
    }
    
    start_time = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response_data = await response.json()
                text = response_data['choices'][0]['message']['content']
    except Exception as e:
        text = f"Error: {str(e)}"
    
    duration = time.time() - start_time
    return duration, text

async def make_official_request(client: AsyncOpenAI, prompt: str) -> tuple[float, str]:
    """Make a request using official OpenAI client"""
    start_time = time.time()
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ]
        )
        text = response.choices[0].message.content
    except Exception as e:
        text = f"Error: {str(e)}"
    
    duration = time.time() - start_time
    return duration, text

async def make_bhumi_request(client: OpenAIClient, prompt: str) -> tuple[float, str]:
    """Make a request through Bhumi"""
    start_time = time.time()
    
    response = await client.acompletion(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        api_key=API_KEY
    )
    
    duration = time.time() - start_time
    return duration, response.text

async def run_batch(func, client, prompts, batch_size) -> list:
    """Run a batch of requests"""
    tasks = [func(client, prompt) for prompt in prompts[:batch_size]]
    return await asyncio.gather(*tasks)

async def run_benchmark():
    """Run comparison benchmark"""
    print("\n🔍 Running OpenAI API Comparison Benchmark")
    print(f"Total requests: {N_REQUESTS}")
    print(f"Concurrent requests: {CONCURRENT_REQUESTS}")
    print(f"Batch size: {BATCH_SIZE}")
    
    # Test prompts
    prompts = [
        "Write a haiku about coding",
        "Write a limerick about Python",
        "Write a short poem about AI",
        "Write a haiku about debugging",
        "Write a verse about programming",
    ] * (N_REQUESTS // 5 + 1)  # Multiply to get enough prompts
    
    # Direct API requests
    print("\n📡 Testing direct API calls...")
    start_time = time.time()
    direct_results = []
    for i in range(0, N_REQUESTS, BATCH_SIZE):
        batch = await run_batch(make_direct_request, None, prompts[i:i+BATCH_SIZE], BATCH_SIZE)
        direct_results.extend(batch)
    direct_total = time.time() - start_time
    
    # Official client requests
    print("\n🔷 Testing official OpenAI client...")
    official_client = AsyncOpenAI(api_key=API_KEY)
    start_time = time.time()
    official_results = []
    for i in range(0, N_REQUESTS, BATCH_SIZE):
        batch = await run_batch(make_official_request, official_client, prompts[i:i+BATCH_SIZE], BATCH_SIZE)
        official_results.extend(batch)
    official_total = time.time() - start_time
    
    # Bhumi requests
    print("\n🚀 Testing Bhumi client...")
    bhumi_client = OpenAIClient(
        max_concurrent=CONCURRENT_REQUESTS,
        model=MODEL,
        debug=False
    )
    start_time = time.time()
    bhumi_results = []
    for i in range(0, N_REQUESTS, BATCH_SIZE):
        batch = await run_batch(make_bhumi_request, bhumi_client, prompts[i:i+BATCH_SIZE], BATCH_SIZE)
        bhumi_results.extend(batch)
    bhumi_total = time.time() - start_time
    
    # Calculate statistics
    def calc_stats(results, total_time):
        durations = [r[0] for r in results]
        return {
            'total': total_time,
            'avg': sum(durations) / len(durations),
            'min': min(durations),
            'max': max(durations),
            'rps': len(durations) / total_time,  # Use total time for true throughput
            'concurrent_rps': len(durations) / sum(durations)  # Theoretical max throughput
        }
    
    direct_stats = calc_stats(direct_results, direct_total)
    official_stats = calc_stats(official_results, official_total)
    bhumi_stats = calc_stats(bhumi_results, bhumi_total)
    
    # Print results
    def print_stats(name, stats):
        print(f"\n{name}:")
        print(f"Total time: {stats['total']:.2f}s")
        print(f"Average request: {stats['avg']:.2f}s")
        print(f"Min request: {stats['min']:.2f}s")
        print(f"Max request: {stats['max']:.2f}s")
        print(f"Actual requests/second: {stats['rps']:.2f}")
        print(f"Theoretical max requests/second: {stats['concurrent_rps']:.2f}")
    
    print("\n📊 Results:")
    print_stats("Direct API", direct_stats)
    print_stats("Official Client", official_stats)
    print_stats("Bhumi Client", bhumi_stats)
    
    # Print example responses
    print("\n✨ Example Responses:")
    print("\nDirect API:")
    print(direct_results[0][1])
    print("\nOfficial Client:")
    print(official_results[0][1])
    print("\nBhumi Client:")
    print(bhumi_results[0][1])

if __name__ == "__main__":
    asyncio.run(run_benchmark()) 