import time
import asyncio
import statistics
from bhumi.base_client import BaseLLMClient, LLMConfig
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json
import numpy as np
import seaborn as sns
import dotenv

dotenv.load_dotenv()

async def collect_chunk_stats(num_requests: int = 5) -> list:
    """Collect chunk size statistics from multiple requests"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
        
    config = LLMConfig(
        api_key=api_key,  # Make sure API key is set
        model="openai/gpt-4o-mini",
        buffer_size=131072  # 128KB
    )
    client = BaseLLMClient(config)
    
    # Test prompts of varying lengths
    prompts = [
        "Write a short sentence.",
        "Write a detailed paragraph about AI.",
        "Explain quantum computing in detail.",
        "Write a short story about time travel.",
        "Describe the entire plot of Star Wars."
    ]
    
    all_chunk_sizes = []
    
    for prompt in prompts:
        print(f"\nTesting prompt: {prompt[:30]}...")
        try:
            response = await client.completion([
                {"role": "user", "content": prompt}
            ])
            
            # The response is double-encoded, so we need to parse it twice
            try:
                stats = json.loads(response["raw_response"]["text"])
                print(f"\nParsed stats:")
                print(json.dumps(stats, indent=2))
                
                chunk_sizes = stats.get("chunk_sizes", [])
                if chunk_sizes:
                    all_chunk_sizes.extend(chunk_sizes)
                    print(f"Received {len(chunk_sizes)} chunks")
                    print(f"Average chunk size: {statistics.mean(chunk_sizes):.0f} bytes")
                    print(f"Min chunk: {min(chunk_sizes)} bytes")
                    print(f"Max chunk: {max(chunk_sizes)} bytes")
                else:
                    print("No chunks found in response")
            except json.JSONDecodeError as e:
                print(f"Error parsing stats: {e}")
                print("Raw text:", response["raw_response"]["text"])
        except Exception as e:
            print(f"Error making request: {e}")
            continue
    
    if not all_chunk_sizes:
        print("\nNo chunks collected across all requests!")
        return []
    
    return all_chunk_sizes

def plot_chunk_analysis(chunk_sizes: list):
    """Create detailed visualizations of chunk sizes"""
    if not chunk_sizes:
        print("No data to plot!")
        return
    
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Histogram of chunk sizes
    plt.subplot(2, 1, 1)
    sns.histplot(chunk_sizes, bins=50)
    plt.title("Distribution of Chunk Sizes")
    plt.xlabel("Chunk Size (bytes)")
    plt.ylabel("Frequency")
    
    # Add statistics annotations
    stats_text = (
        f"Mean: {statistics.mean(chunk_sizes):.0f} bytes\n"
        f"Median: {statistics.median(chunk_sizes):.0f} bytes\n"
        f"Std Dev: {statistics.stdev(chunk_sizes):.0f} bytes\n"
        f"Min: {min(chunk_sizes)} bytes\n"
        f"Max: {max(chunk_sizes)} bytes\n"
        f"Total Chunks: {len(chunk_sizes)}"
    )
    plt.text(0.95, 0.95, stats_text,
             transform=plt.gca().transAxes,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 2: Chunk sizes over sequence
    plt.subplot(2, 1, 2)
    plt.plot(chunk_sizes, marker='.')
    plt.title("Chunk Sizes Over Sequence")
    plt.xlabel("Chunk Number")
    plt.ylabel("Size (bytes)")
    plt.grid(True)
    
    # Add rolling average
    window = min(50, len(chunk_sizes))
    rolling_mean = np.convolve(chunk_sizes, 
                              np.ones(window)/window, 
                              mode='valid')
    plt.plot(range(window-1, len(chunk_sizes)), 
             rolling_mean, 
             'r-', 
             label=f'{window}-point moving average')
    plt.legend()
    
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"benchmarks/plots/chunk_analysis_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_filename, bbox_inches='tight')
    print(f"\n📈 Plot saved as: {plot_filename}")

async def main():
    chunk_sizes = await collect_chunk_stats()
    plot_chunk_analysis(chunk_sizes)

if __name__ == "__main__":
    asyncio.run(main()) 