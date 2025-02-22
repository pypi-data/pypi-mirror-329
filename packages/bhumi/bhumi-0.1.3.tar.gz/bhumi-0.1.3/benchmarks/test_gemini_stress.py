import asyncio
import os
import time
import psutil
from google import genai
from bhumi.client import GeminiClient
import matplotlib.pyplot as plt
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import concurrent.futures

os.environ["GOOGLE_API_KEY"] = "AIzaSyDXWUOcqUw3FF3o3WaftJkSZDJRX7rGtys"
GEMINI_KEY = os.environ["GOOGLE_API_KEY"]
TEST_DURATION = 5  # seconds
PROMPT = "Why is the sky blue?"
MAX_CONCURRENT = 10  # Limit concurrent requests

# Initialize clients
genai_client = genai.Client()
bhumi_client = GeminiClient(
    max_concurrent=MAX_CONCURRENT,
    model="gemini-1.5-flash-8b",
    debug=True  # Enable debug mode
)

def get_process_memory():
    """Get current process memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

class Metrics:
    def __init__(self):
        self.request_times = []
        self.memory_usage = []
        self.timestamps = []
        self.success_count = 0
        self.error_count = 0
        self.start_time = None

def test_google_genai():
    print("\n🚀 Testing Google GenAI...")
    metrics = Metrics()
    metrics.start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        futures = []
        while time.time() - metrics.start_time < TEST_DURATION:
            if len(futures) >= MAX_CONCURRENT:
                # Wait for some futures to complete
                done, futures = concurrent.futures.wait(
                    futures, return_when=concurrent.futures.FIRST_COMPLETED
                )
            
            future = executor.submit(lambda: genai_client.models.generate_content(
                model="gemini-1.5-flash-8b",
                contents=PROMPT
            ))
            futures.append(future)
            print(f"Google GenAI: Submitted request {len(futures)}")
    
    return metrics

async def test_bhumi():
    print("\n🚀 Testing Bhumi...")
    metrics = Metrics()
    metrics.start_time = time.time()
    
    async def make_request(i):
        try:
            print(f"Bhumi: Starting request {i}")
            response = await bhumi_client.acompletion(
                model="gemini-1.5-flash-8b",  # Remove gemini/ prefix
                messages=[{"role": "user", "content": PROMPT}],
                api_key=GEMINI_KEY
            )
            print(f"Bhumi: Completed request {i}")
            metrics.success_count += 1
        except Exception as e:
            print(f"Bhumi Error: {str(e)}")
            metrics.error_count += 1
    
    # Create a fixed number of tasks
    tasks = []
    for i in range(MAX_CONCURRENT):
        tasks.append(asyncio.create_task(make_request(i)))
        print(f"Created task {i}")
    
    await asyncio.gather(*tasks)
    print("All tasks completed")
    return metrics

def plot_results(genai_metrics, bhumi_metrics):
    """Plot comparison graphs"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Request Times
    plt.subplot(2, 2, 1)
    plt.hist([genai_metrics.request_times, bhumi_metrics.request_times], 
             label=['Google GenAI', 'Bhumi'], bins=20, alpha=0.7)
    plt.title('Request Time Distribution')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Count')
    plt.legend()
    
    # Plot 2: Memory Usage Over Time
    plt.subplot(2, 2, 2)
    plt.plot(genai_metrics.timestamps, genai_metrics.memory_usage, 
             label='Google GenAI', alpha=0.7)
    plt.plot(bhumi_metrics.timestamps, bhumi_metrics.memory_usage, 
             label='Bhumi', alpha=0.7)
    plt.title('Memory Usage Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Memory Usage (MB)')
    plt.legend()
    
    # Plot 3: Throughput
    plt.subplot(2, 2, 3)
    throughput = [
        genai_metrics.success_count / TEST_DURATION,
        bhumi_metrics.success_count / TEST_DURATION
    ]
    plt.bar(['Google GenAI', 'Bhumi'], throughput)
    plt.title('Throughput (requests/second)')
    plt.ylabel('Requests per Second')
    
    # Plot 4: Success vs Error Rate
    plt.subplot(2, 2, 4)
    success_rates = [
        [genai_metrics.success_count, genai_metrics.error_count],
        [bhumi_metrics.success_count, bhumi_metrics.error_count]
    ]
    plt.bar(['Google GenAI', 'Bhumi'], 
            [sum(x) for x in success_rates], 
            label='Errors', alpha=0.7)
    plt.bar(['Google GenAI', 'Bhumi'],
            [x[0] for x in success_rates],
            label='Successes', alpha=0.7)
    plt.title('Success vs Error Count')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'gemini_stress_test_{timestamp}.png')
    print(f"\n📊 Results saved to gemini_stress_test_{timestamp}.png")
    
    # Print summary statistics
    print("\n📈 Summary Statistics:")
    print("Google GenAI:")
    print(f"  Total Requests: {genai_metrics.success_count + genai_metrics.error_count}")
    print(f"  Successful: {genai_metrics.success_count}")
    print(f"  Errors: {genai_metrics.error_count}")
    print(f"  Avg Response Time: {np.mean(genai_metrics.request_times):.2f}s")
    print(f"  Max Memory: {max(genai_metrics.memory_usage):.1f}MB")
    
    print("\nBhumi:")
    print(f"  Total Requests: {bhumi_metrics.success_count + bhumi_metrics.error_count}")
    print(f"  Successful: {bhumi_metrics.success_count}")
    print(f"  Errors: {bhumi_metrics.error_count}")
    print(f"  Avg Response Time: {np.mean(bhumi_metrics.request_times):.2f}s")
    print(f"  Max Memory: {max(bhumi_metrics.memory_usage):.1f}MB")

async def main():
    # Run tests sequentially
    print("Starting Google GenAI test...")
    genai_metrics = test_google_genai()
    
    print("Starting Bhumi test...")
    bhumi_metrics = await test_bhumi()
    
    plot_results(genai_metrics, bhumi_metrics)

if __name__ == "__main__":
    asyncio.run(main()) 