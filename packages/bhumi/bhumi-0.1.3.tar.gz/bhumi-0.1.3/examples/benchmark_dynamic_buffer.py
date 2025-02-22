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
import pandas as pd
import dotenv

dotenv.load_dotenv()

class DynamicBuffer:
    def __init__(self, initial_size=8192, min_size=1024, max_size=131072):
        self.current_size = initial_size
        self.min_size = min_size
        self.max_size = max_size
        self.chunk_history = []
        self.adjustment_factor = 1.5  # For exponential growth/shrink
        
    def adjust(self, chunk_size):
        """Adjust buffer size based on incoming chunk size"""
        self.chunk_history.append(chunk_size)
        
        # Use recent history to determine trend
        recent_chunks = self.chunk_history[-5:]
        avg_chunk = statistics.mean(recent_chunks) if recent_chunks else chunk_size
        
        # If chunks are consistently larger, grow buffer
        if avg_chunk > self.current_size * 0.8:
            self.current_size = min(
                self.max_size,
                int(self.current_size * self.adjustment_factor)
            )
        # If chunks are consistently smaller, shrink buffer
        elif avg_chunk < self.current_size * 0.3:
            self.current_size = max(
                self.min_size,
                int(self.current_size / self.adjustment_factor)
            )
        
        return self.current_size

async def benchmark_buffers(prompts):
    """Compare fixed vs dynamic buffer sizes"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    results = []
    buffer_types = {
        "Fixed (128KB)": 131072,
        "Fixed (8KB)": 8192,
        "Dynamic": DynamicBuffer()
    }
    
    for prompt in prompts:
        print(f"\nTesting prompt: {prompt[:50]}...")
        
        for buffer_name, buffer in buffer_types.items():
            buffer_size = buffer if isinstance(buffer, int) else buffer.current_size
            
            config = LLMConfig(
                api_key=api_key,
                model="openai/gpt-4o-mini",
                buffer_size=buffer_size
            )
            client = BaseLLMClient(config)
            
            start_time = time.perf_counter()
            response = await client.completion([
                {"role": "user", "content": prompt}
            ])
            elapsed = time.perf_counter() - start_time
            
            # Extract chunk sizes
            try:
                stats = json.loads(response["raw_response"]["text"])
                chunk_sizes = stats.get("chunk_sizes", [])
                
                if isinstance(buffer, DynamicBuffer):
                    for chunk_size in chunk_sizes:
                        buffer_size = buffer.adjust(chunk_size)
                
                results.append({
                    "Buffer Type": buffer_name,
                    "Prompt Length": len(prompt),
                    "Response Length": len(stats["text"]),
                    "Num Chunks": len(chunk_sizes),
                    "Avg Chunk Size": statistics.mean(chunk_sizes) if chunk_sizes else 0,
                    "Buffer Size": buffer_size,
                    "Response Time": elapsed,
                    "Throughput": len(stats["text"]) / elapsed
                })
                
                print(f"{buffer_name}:")
                print(f"  Response time: {elapsed:.3f}s")
                print(f"  Throughput: {len(stats['text']) / elapsed:.0f} chars/s")
                print(f"  Buffer size: {buffer_size} bytes")
                print(f"  Chunks: {len(chunk_sizes)}")
                
            except Exception as e:
                print(f"Error processing response: {e}")
    
    return pd.DataFrame(results)

def plot_results(df):
    """Create visualizations comparing buffer strategies"""
    plt.figure(figsize=(15, 15))
    
    # Plot 1: Response times
    plt.subplot(3, 1, 1)
    sns.boxplot(data=df, x="Buffer Type", y="Response Time")
    plt.title("Response Time by Buffer Type")
    plt.ylabel("Time (seconds)")
    
    # Plot 2: Throughput
    plt.subplot(3, 1, 2)
    sns.boxplot(data=df, x="Buffer Type", y="Throughput")
    plt.title("Throughput by Buffer Type")
    plt.ylabel("Characters per Second")
    
    # Plot 3: Buffer Size vs Response Length
    plt.subplot(3, 1, 3)
    for buffer_type in df["Buffer Type"].unique():
        data = df[df["Buffer Type"] == buffer_type]
        plt.scatter(data["Response Length"], data["Buffer Size"], 
                   label=buffer_type, alpha=0.6)
    plt.xlabel("Response Length (chars)")
    plt.ylabel("Buffer Size (bytes)")
    plt.title("Buffer Size vs Response Length")
    plt.legend()
    
    plt.tight_layout()
    
    # Additional analysis
    print("\nDetailed Analysis:")
    for buffer_type in df["Buffer Type"].unique():
        data = df[df["Buffer Type"] == buffer_type]
        print(f"\n{buffer_type}:")
        print(f"  Avg chunks per response: {data['Num Chunks'].mean():.1f}")
        print(f"  Avg chunk size: {data['Avg Chunk Size'].mean():.0f} bytes")
        print(f"  Buffer utilization: {(data['Avg Chunk Size'] / data['Buffer Size']).mean()*100:.1f}%")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save plot
    plot_path = f"benchmarks/plots/buffer_comparison_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_path, bbox_inches='tight')
    print(f"\n📈 Plot saved as: {plot_path}")
    
    # Save detailed results
    csv_path = f"benchmarks/results/buffer_comparison_{timestamp}.csv"
    os.makedirs("benchmarks/results", exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"📊 Detailed results saved as: {csv_path}")

async def main():
    prompts = [
        "Write a one-sentence summary.",  # Very short
        "Write a detailed paragraph about artificial intelligence.",  # Medium
        "Explain quantum computing in detail.",  # Long
        "Write a short story about time travel.",  # Very long
        "Describe the entire plot of Star Wars.",  # Extra long
        # Add more prompts of varying lengths
    ]
    
    results_df = await benchmark_buffers(prompts)
    plot_results(results_df)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    summary = results_df.groupby("Buffer Type").agg({
        "Response Time": ["mean", "std"],
        "Throughput": ["mean", "std"]
    }).round(3)
    print(summary)

if __name__ == "__main__":
    asyncio.run(main()) 