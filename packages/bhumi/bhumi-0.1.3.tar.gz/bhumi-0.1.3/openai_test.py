import os
import asyncio
import time
from bhumi.client import OpenAIClient

api_key = "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"

# Configuration
API_KEY = api_key
MODEL = "gpt-4o"
N_REQUESTS = 10
CONCURRENT_REQUESTS = 5

async def make_request(client: OpenAIClient, prompt: str) -> tuple[float, str]:
    """Make a single request and return timing"""
    start_time = time.time()
    
    response = await client.acompletion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        api_key=API_KEY
    )
    
    duration = time.time() - start_time
    return duration, response.text

async def run_benchmark():
    """Run benchmark with multiple concurrent requests"""
    print(f"\n🚀 Running OpenAI benchmark...")
    print(f"Requests: {N_REQUESTS}")
    print(f"Concurrent requests: {CONCURRENT_REQUESTS}")
    
    # Initialize client
    client = OpenAIClient(
        max_concurrent=CONCURRENT_REQUESTS,
        model=MODEL,
        debug=False
    )
    
    # Test prompts
    prompts = [
        "Write a haiku about coding",
        "Write a limerick about Python",
        "Write a short poem about AI",
        "Write a haiku about debugging",
        "Write a verse about programming",
    ]
    
    # Create tasks
    tasks = []
    for i in range(N_REQUESTS):
        prompt = prompts[i % len(prompts)]
        tasks.append(make_request(client, prompt))
    
    # Run requests in batches
    print("\n⏳ Making requests...")
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    # Calculate statistics
    durations = [r[0] for r in results]
    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    
    # Print results
    print("\n📊 Results:")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average request time: {avg_duration:.2f}s")
    print(f"Min request time: {min_duration:.2f}s")
    print(f"Max request time: {max_duration:.2f}s")
    print(f"Requests per second: {N_REQUESTS/total_time:.2f}")
    
    # Print some example responses
    print("\n✨ Example responses:")
    for i, (_, response) in enumerate(results[:3]):
        print(f"\nResponse {i+1}:")
        print(response)

if __name__ == "__main__":
    asyncio.run(run_benchmark()) 