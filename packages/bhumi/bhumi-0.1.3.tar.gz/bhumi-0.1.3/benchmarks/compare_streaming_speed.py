import asyncio
import time
import statistics
from bhumi.client import OpenAIClient
from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
from bhumi.utils import async_retry

api_key = "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"
MODEL = "gpt-4o-mini"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@async_retry(max_retries=3, initial_delay=0.1, logger=logger)
async def test_streaming():
    client = OpenAIClient(debug=False)
    start_time = time.time()
    full_response = ""
    first_token_time = None
    token_times: List[float] = []
    last_token_time = start_time
    
    async for chunk in client.astream_completion(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Write a story about a robot in exactly 500 words"}
        ],
        api_key=api_key
    ):
        current_time = time.time()
        if first_token_time is None:
            first_token_time = current_time - start_time
        
        token_times.append(current_time - last_token_time)
        last_token_time = current_time
        full_response += chunk
    
    total_time = time.time() - start_time
    return {
        "first_token": first_token_time if first_token_time is not None else total_time,
        "total_time": total_time,
        "response_length": len(full_response),
        "token_count": len(token_times),
        "avg_token_time": statistics.mean(token_times) if token_times else 0,
        "tokens_per_second": len(token_times) / total_time
    }

@async_retry(max_retries=3, initial_delay=0.1, logger=logger)
async def test_regular():
    client = OpenAIClient(debug=False)
    start_time = time.time()
    
    response = await client.acompletion(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Write a story about a robot in exactly 50 words"}
        ],
        api_key=api_key
    )
    
    total_time = time.time() - start_time
    return {
        "total_time": total_time,
        "response_length": len(response.text),
        "tokens_per_second": len(response.text) / total_time  # Approximate
    }

def plot_comparison(stream_stats: Dict, reg_stats: Dict, streaming_results: List[Dict], regular_results: List[Dict]):
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Streaming vs Regular Completion Performance', fontsize=16)
    
    # Plot 1: Time Comparison
    metrics = ['First Token', 'Total Time']
    times = [stream_stats['first_token'], stream_stats['total_time']]
    reg_times = [np.nan, reg_stats['total_time']]  # No first token time for regular
    
    x = np.arange(len(metrics))
    width = 0.35
    
    ax1.bar(x - width/2, times, width, label='Streaming')
    ax1.bar(x + width/2, reg_times, width, label='Regular')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Response Times')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics)
    ax1.legend()
    
    # Plot 2: Tokens per Second
    ax2.boxplot([
        [r['tokens_per_second'] for r in streaming_results],
        [r['tokens_per_second'] for r in regular_results]
    ], labels=['Streaming', 'Regular'])
    ax2.set_title('Tokens per Second Distribution')
    ax2.set_ylabel('Tokens/second')
    
    # Plot 3: Individual Run Times
    runs = range(1, len(streaming_results) + 1)
    ax3.plot(runs, [r['total_time'] for r in streaming_results], 'b-', label='Streaming')
    ax3.plot(runs, [r['total_time'] for r in regular_results], 'r-', label='Regular')
    ax3.set_xlabel('Run Number')
    ax3.set_ylabel('Total Time (seconds)')
    ax3.set_title('Total Time per Run')
    ax3.legend()
    
    # Plot 4: Token Timing Distribution (streaming only)
    token_times = [r['avg_token_time'] * 1000 for r in streaming_results]  # Convert to ms
    ax4.hist(token_times, bins=20)
    ax4.set_xlabel('Average Time per Token (ms)')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Token Timing Distribution (Streaming)')
    
    plt.tight_layout()
    plt.savefig('completion_comparison.png')
    plt.close()

async def main():
    runs = 2
    streaming_results = []
    regular_results = []
    
    print(f"\nRunning {runs} iterations of each method...")
    
    for i in range(runs):
        print(f"\nIteration {i+1}/{runs}")
        
        try:
            print("Testing streaming...", end=" ", flush=True)
            stream_result = await test_streaming()
            streaming_results.append(stream_result)
            print(f"Done! ({stream_result['token_count']} tokens, {stream_result['tokens_per_second']:.1f} tokens/sec)")
        except Exception as e:
            logger.error(f"Streaming test failed after retries: {e}")
            continue
        
        try:
            print("Testing regular...", end=" ", flush=True)
            reg_result = await test_regular()
            regular_results.append(reg_result)
            print(f"Done! (Length: {reg_result['response_length']} chars, {reg_result['tokens_per_second']:.1f} chars/sec)")
        except Exception as e:
            logger.error(f"Regular test failed after retries: {e}")
            continue
        
        await asyncio.sleep(1)
    
    if not streaming_results or not regular_results:
        logger.error("No successful results to analyze")
        return
        
    # Calculate statistics
    stream_stats = {
        "first_token": statistics.mean(r["first_token"] for r in streaming_results),
        "total_time": statistics.mean(r["total_time"] for r in streaming_results),
        "tokens_per_second": statistics.mean(r["tokens_per_second"] for r in streaming_results),
        "token_count": statistics.mean(r["token_count"] for r in streaming_results),
        "avg_token_time": statistics.mean(r["avg_token_time"] for r in streaming_results)
    }
    
    reg_stats = {
        "total_time": statistics.mean(r["total_time"] for r in regular_results),
        "tokens_per_second": statistics.mean(r["tokens_per_second"] for r in regular_results)
    }
    
    # Print detailed results
    print("\n=== Detailed Results ===")
    print("\nStreaming:")
    print(f"Time to first token: {stream_stats['first_token']:.3f}s")
    print(f"Average tokens per second: {stream_stats['tokens_per_second']:.1f}")
    print(f"Average time per token: {stream_stats['avg_token_time']*1000:.1f}ms")
    print(f"Total time: {stream_stats['total_time']:.3f}s")
    print(f"Average token count: {stream_stats['token_count']:.1f}")
    
    print("\nRegular:")
    print(f"Total time: {reg_stats['total_time']:.3f}s")
    print(f"Average chars per second: {reg_stats['tokens_per_second']:.1f}")
    
    # Calculate and print speedup ratios
    latency_speedup = reg_stats['total_time'] / stream_stats['first_token']
    throughput_ratio = stream_stats['tokens_per_second'] / reg_stats['tokens_per_second']
    total_time_ratio = reg_stats['total_time'] / stream_stats['total_time']
    
    print("\nSpeedup Analysis:")
    print(f"Latency speedup (time to first token): {latency_speedup:.1f}x faster")
    print(f"Throughput ratio: {throughput_ratio:.2f}x")
    print(f"Total time ratio: {total_time_ratio:.2f}x")
    
    # Create comparison table
    df = pd.DataFrame({
        'Metric': ['Time to first token', 'Total time', 'Tokens per second'],
        'Streaming': [
            f"{stream_stats['first_token']:.3f}s",
            f"{stream_stats['total_time']:.3f}s",
            f"{stream_stats['tokens_per_second']:.1f}"
        ],
        'Regular': [
            'N/A',
            f"{reg_stats['total_time']:.3f}s",
            f"{reg_stats['tokens_per_second']:.1f}"
        ]
    })
    
    print("\nComparison Table:")
    print(df.to_string(index=False))
    
    # Generate plots
    plot_comparison(stream_stats, reg_stats, streaming_results, regular_results)
    print("\nVisualization saved as 'completion_comparison.png'")

if __name__ == "__main__":
    asyncio.run(main()) 