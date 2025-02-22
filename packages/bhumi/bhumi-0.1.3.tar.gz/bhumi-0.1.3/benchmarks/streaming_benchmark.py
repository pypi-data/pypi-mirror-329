import asyncio
import time
from openai import AsyncOpenAI
from bhumi.client import OpenAIClient
import statistics
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict

os.environ["OPENAI_API_KEY"] = "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"
api_key = "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"

async def benchmark_native_openai_batch(api_key: str, messages_list: List[list], runs: int = 5):
    client = AsyncOpenAI(api_key=api_key)
    batch_times = []
    ttfts = []
    token_times = []

    for _ in range(runs):
        start_time = time.time()
        first_tokens = [False] * len(messages_list)
        token_counts = [0] * len(messages_list)
        last_token_times = [start_time] * len(messages_list)

        # Create tasks for all requests in the batch
        tasks = [
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True
            )
            for messages in messages_list
        ]
        
        # Start all requests concurrently
        streams = await asyncio.gather(*tasks)
        
        # Process streams concurrently
        async def process_stream(stream, idx):
            async for chunk in stream:
                current_time = time.time()
                if not first_tokens[idx]:
                    first_tokens[idx] = True
                    ttfts.append(current_time - start_time)
                
                if chunk.choices[0].delta.content:
                    token_counts[idx] += 1
                    token_times.append(current_time - last_token_times[idx])
                    last_token_times[idx] = current_time

        await asyncio.gather(*[process_stream(stream, i) for i, stream in enumerate(streams)])
        batch_times.append(time.time() - start_time)

    return {
        "ttft_avg": statistics.mean(ttfts),
        "ttft_std": statistics.stdev(ttfts),
        "token_time_avg": statistics.mean(token_times),
        "token_time_std": statistics.stdev(token_times),
        "batch_time_avg": statistics.mean(batch_times),
        "batch_time_std": statistics.stdev(batch_times),
        "throughput": len(messages_list) / statistics.mean(batch_times)
    }

async def benchmark_bhumi_batch(api_key: str, messages_list: List[list], runs: int = 5):
    client = OpenAIClient(debug=True, max_concurrent=len(messages_list))
    batch_times = []
    ttfts = []
    token_times = []

    for _ in range(runs):
        start_time = time.time()
        first_tokens = [False] * len(messages_list)
        token_counts = [0] * len(messages_list)
        last_token_times = [start_time] * len(messages_list)

        # Create tasks for all requests in the batch
        async def process_request(messages, idx):
            async for chunk in client.astream_completion(
                model="gpt-4o-mini",
                messages=messages,
                api_key=api_key
            ):
                current_time = time.time()
                if not first_tokens[idx]:
                    first_tokens[idx] = True
                    ttfts.append(current_time - start_time)
                
                token_counts[idx] += 1
                token_times.append(current_time - last_token_times[idx])
                last_token_times[idx] = current_time

        # Process all requests concurrently
        await asyncio.gather(*[
            process_request(messages, i) 
            for i, messages in enumerate(messages_list)
        ])
        
        batch_times.append(time.time() - start_time)

    return {
        "ttft_avg": statistics.mean(ttfts),
        "ttft_std": statistics.stdev(ttfts),
        "token_time_avg": statistics.mean(token_times),
        "token_time_std": statistics.stdev(token_times),
        "batch_time_avg": statistics.mean(batch_times),
        "batch_time_std": statistics.stdev(batch_times),
        "throughput": len(messages_list) / statistics.mean(batch_times)
    }

def plot_results(all_native_results: Dict[int, dict], all_bhumi_results: Dict[int, dict]):
    batch_sizes = list(all_native_results.keys())
    metrics = ['ttft_avg', 'token_time_avg', 'batch_time_avg', 'throughput']
    titles = ['Time to First Token (s)', 'Time per Token (ms)', 'Total Batch Time (s)', 'Throughput (req/s)']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Benchmark Results: Native vs Bhumi', fontsize=16)
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx // 2, idx % 2]
        
        x = np.arange(len(batch_sizes))
        width = 0.35
        
        native_values = [all_native_results[size][metric] for size in batch_sizes]
        bhumi_values = [all_bhumi_results[size][metric] for size in batch_sizes]
        
        if metric == 'token_time_avg':
            # Convert to milliseconds
            native_values = [v * 1000 for v in native_values]
            bhumi_values = [v * 1000 for v in bhumi_values]
        
        rects1 = ax.bar(x - width/2, native_values, width, label='Native')
        rects2 = ax.bar(x + width/2, bhumi_values, width, label='Bhumi')
        
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels([f'Batch {size}' for size in batch_sizes])
        ax.legend()
        
        # Add value labels on top of bars
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=0)
        
        autolabel(rects1)
        autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png')
    plt.close()

async def main():
    # Create multiple different prompts for batch testing
    base_messages = [
        [{"role": "user", "content": "Write a story about a robot in exactly 100 words"}],
        [{"role": "user", "content": "Write a story about an AI in exactly 100 words"}],
        [{"role": "user", "content": "Write a story about a computer in exactly 100 words"}],
        [{"role": "user", "content": "Write a story about a cyborg in exactly 100 words"}],
        [{"role": "user", "content": "Write a story about an android in exactly 100 words"}]
    ]
    
    batch_sizes = [1, 2, 5]
    
    all_native_results = {}
    all_bhumi_results = {}
    
    for batch_size in batch_sizes:
        messages_list = base_messages[:batch_size]
        
        print(f"\n=== Testing Batch Size: {batch_size} ===")
        
        print("\nBenchmarking Native OpenAI Client...")
        native_results = await benchmark_native_openai_batch(api_key, messages_list)
        all_native_results[batch_size] = native_results
        
        print("\nBenchmarking Bhumi Client...")
        bhumi_results = await benchmark_bhumi_batch(api_key, messages_list)
        all_bhumi_results[batch_size] = bhumi_results

        print(f"\nResults for Batch Size {batch_size}:")
        print("\nNative OpenAI Client:")
        print(f"Time to First Token: {native_results['ttft_avg']:.3f}s ± {native_results['ttft_std']:.3f}s")
        print(f"Time per Token: {native_results['token_time_avg']*1000:.2f}ms ± {native_results['token_time_std']*1000:.2f}ms")
        print(f"Total Batch Time: {native_results['batch_time_avg']:.3f}s ± {native_results['batch_time_std']:.3f}s")
        print(f"Throughput: {native_results['throughput']:.2f} requests/second")

        print("\nBhumi Client:")
        print(f"Time to First Token: {bhumi_results['ttft_avg']:.3f}s ± {bhumi_results['ttft_std']:.3f}s")
        print(f"Time per Token: {bhumi_results['token_time_avg']*1000:.2f}ms ± {bhumi_results['token_time_std']*1000:.2f}ms")
        print(f"Total Batch Time: {bhumi_results['batch_time_avg']:.3f}s ± {bhumi_results['batch_time_std']:.3f}s")
        print(f"Throughput: {bhumi_results['throughput']:.2f} requests/second")

    # Create visualization
    plot_results(all_native_results, all_bhumi_results)
    print("\nBenchmark visualization saved as 'benchmark_results.png'")

if __name__ == "__main__":
    asyncio.run(main()) 