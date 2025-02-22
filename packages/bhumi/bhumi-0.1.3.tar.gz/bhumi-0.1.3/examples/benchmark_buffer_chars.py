import time
import asyncio
import statistics
from bhumi.base_client import BaseLLMClient, LLMConfig
import matplotlib.pyplot as plt
import os
from datetime import datetime

async def test_buffer_size(char_size: int, num_requests: int = 5) -> dict:
    """Test performance with a specific buffer size (in characters)"""
    config = LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="openai/gpt-4o-mini",
        buffer_size=char_size
    )
    client = BaseLLMClient(config)
    
    # Test prompt that will generate responses of different lengths
    prompts = [
        "Write a short sentence.",  # ~10-20 chars
        "Write a detailed paragraph about AI.",  # ~200-300 chars
        "Explain quantum computing in detail.",  # ~500-1000 chars
        "Write a short story about time travel.",  # ~1000-2000 chars
        "Describe the entire plot of Star Wars."  # ~3000-5000 chars
    ]
    
    times = []
    chars_processed = []
    
    for prompt in prompts:
        start = time.perf_counter()
        response = await client.completion([
            {"role": "user", "content": prompt}
        ])
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        chars_processed.append(len(response["text"]))
    
    return {
        "avg_time": statistics.mean(times),
        "throughput": sum(chars_processed) / sum(times),  # chars/second
        "response_sizes": chars_processed
    }

async def find_optimal_buffer():
    """Test different buffer sizes and plot results"""
    # Test buffer sizes from 100 to 10000 characters
    buffer_sizes = [
        100,    # 100 chars
        250,    # 250 chars
        500,    # 500 chars
        1000,   # 1K chars
        2500,   # 2.5K chars
        5000,   # 5K chars
        10000,  # 10K chars
    ]
    
    results = []
    for size in buffer_sizes:
        print(f"Testing buffer size: {size} characters")
        metrics = await test_buffer_size(size)
        results.append({
            "size": size,
            "metrics": metrics
        })
        
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Response Time
    plt.subplot(2, 1, 1)
    times = [r["metrics"]["avg_time"] for r in results]
    plt.semilogx(buffer_sizes, times, marker='o')
    plt.grid(True)
    plt.xlabel('Buffer Size (characters)')
    plt.ylabel('Average Response Time (seconds)')
    plt.title('Response Time vs Buffer Size')
    
    # Add size labels
    for size, time in zip(buffer_sizes, times):
        plt.annotate(f'{size}\n{time:.3f}s', 
                    (size, time), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center')
    
    # Plot 2: Throughput
    plt.subplot(2, 1, 2)
    throughput = [r["metrics"]["throughput"] for r in results]
    plt.semilogx(buffer_sizes, throughput, marker='o', color='green')
    plt.grid(True)
    plt.xlabel('Buffer Size (characters)')
    plt.ylabel('Throughput (chars/second)')
    plt.title('Processing Throughput vs Buffer Size')
    
    # Add throughput labels
    for size, thru in zip(buffer_sizes, throughput):
        plt.annotate(f'{size}\n{thru:.0f} c/s', 
                    (size, thru), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center')
    
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"benchmarks/plots/buffer_chars_benchmark_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_filename, bbox_inches='tight')
    print(f"\n📈 Plot saved as: {plot_filename}")
    
    # Find optimal size
    optimal_idx = throughput.index(max(throughput))
    optimal_size = buffer_sizes[optimal_idx]
    print(f"\nOptimal buffer size: {optimal_size} characters")
    print(f"Best throughput: {throughput[optimal_idx]:.0f} chars/second")

if __name__ == "__main__":
    asyncio.run(find_optimal_buffer()) 