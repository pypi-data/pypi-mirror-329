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
from dataclasses import dataclass
from typing import Dict, List, Tuple
import random
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmark_map_elites_full import SystemConfig, FullMapElites, benchmark_system

dotenv.load_dotenv()

class SimpleBuffer:
    """Fixed size buffer"""
    def __init__(self, size: int):
        self.size = size
        
    def get_size(self) -> int:
        return self.size

class DynamicBuffer:
    """Original dynamic buffer implementation"""
    def __init__(self, initial_size=8192, min_size=1024, max_size=131072):
        self.current_size = initial_size
        self.min_size = min_size
        self.max_size = max_size
        self.chunk_history = []
        self.adjustment_factor = 1.5
        
    def get_size(self) -> int:
        return self.current_size
        
    def adjust(self, chunk_size):
        self.chunk_history.append(chunk_size)
        recent_chunks = self.chunk_history[-5:]
        avg_chunk = statistics.mean(recent_chunks) if recent_chunks else chunk_size
        
        if avg_chunk > self.current_size * 0.8:
            self.current_size = min(
                self.max_size,
                int(self.current_size * self.adjustment_factor)
            )
        elif avg_chunk < self.current_size * 0.3:
            self.current_size = max(
                self.min_size,
                int(self.current_size / self.adjustment_factor)
            )
        return self.current_size

async def benchmark_buffer_strategy(buffer_strategy, prompts: List[str], num_iterations: int = 3) -> Dict:
    """Benchmark a specific buffer strategy"""
    results = []
    errors = 0
    total_requests = 0
    
    if isinstance(buffer_strategy, str) and buffer_strategy == "map_elites":
        # Try multiple locations for the archive
        archive_paths = [
            "benchmarks/map_elites/archive_latest.json",
            os.path.join(os.path.dirname(__file__), "../benchmarks/map_elites/archive_latest.json"),
            "/Users/rachpradhan/bhumi/benchmarks/map_elites/archive_latest.json"
        ]
        
        for path in archive_paths:
            if os.path.exists(path):
                map_elites = FullMapElites.load(path)
                print(f"Loaded MAP-Elites archive from: {path}")
                break
        else:
            raise FileNotFoundError("Could not find MAP-Elites archive")
        
        # Get the best overall configuration
        best_config = max(map_elites.archive.values(), key=lambda x: x[1])[0]
        buffer_size = best_config.buffer_size
        
        # For adaptive behavior, we can also use the archive during runtime
        def get_adaptive_config(response_length: int, num_chunks: int) -> int:
            # Add debug prints
            print(f"\nAdapting buffer for response length: {response_length}, chunks: {num_chunks}")
            
            if elite_config := map_elites.get_elite(response_length, num_chunks):
                new_size = elite_config.buffer_size
                print(f"Found elite configuration with buffer size: {new_size}")
                # Don't allow huge jumps in buffer size
                if new_size > buffer_size * 2:
                    new_size = buffer_size * 2
                elif new_size < buffer_size / 2:
                    new_size = buffer_size / 2
                return int(new_size)
            
            print("No elite configuration found, using current buffer size")
            return buffer_size  # fallback to current
            
    else:
        buffer_size = buffer_strategy.get_size()
    
    client = BaseLLMClient(LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="openai/gpt-4o-mini",
        buffer_size=buffer_size,
        debug=True
    ), debug=True)
    
    start_time = time.perf_counter()
    print("\nStarting benchmark...")
    
    for iter_idx in range(num_iterations):
        print(f"\nIteration {iter_idx + 1}/{num_iterations}")
        for prompt_idx, prompt in enumerate(prompts):
            total_requests += 1
            print(f"\nProcessing prompt {prompt_idx + 1}/{len(prompts)}: {prompt[:50]}...")
            
            try:
                print("Sending request...")
                response = await client.completion([
                    {"role": "user", "content": prompt}
                ])
                print(f"Got response: {response}")
                
                if not isinstance(response, dict):
                    print(f"Unexpected response type: {type(response)}")
                    errors += 1
                    continue
                
                text = response.get("text", "")
                raw_response = response.get("raw_response", {})
                print(f"Text length: {len(text)}")
                print(f"Raw response: {raw_response}")
                
                if not text:
                    print(f"Empty response text. Full response: {response}")
                    errors += 1
                    continue
                
                if isinstance(buffer_strategy, DynamicBuffer):
                    old_size = buffer_strategy.get_size()
                    buffer_strategy.adjust(len(text))
                    new_size = buffer_strategy.get_size()
                    print(f"Adjusted buffer size: {old_size} -> {new_size}")
                elif isinstance(buffer_strategy, str) and buffer_strategy == "map_elites":
                    old_size = buffer_size
                    buffer_size = get_adaptive_config(
                        len(text),
                        1
                    )
                    print(f"MAP-Elites adjusted buffer: {old_size} -> {buffer_size}")
                
                results.append({
                    "response_size": len(text),
                    "num_chunks": 1,
                    "avg_chunk_size": len(text),
                    "buffer_size": buffer_size
                })
                print(f"Successfully processed response of length {len(text)}")
                
            except Exception as e:
                errors += 1
                print(f"\nError processing request:")
                print(f"Exception type: {type(e)}")
                print(f"Exception details: {str(e)}")
                if 'response' in locals():
                    print(f"Response type: {type(response)}")
                    if isinstance(response, dict):
                        print(f"Response keys: {response.keys()}")
                        print(f"Response content: {response}")
                import traceback
                traceback.print_exc()
    
    elapsed = time.perf_counter() - start_time
    
    print(f"\nBenchmark complete:")
    print(f"Total requests: {total_requests}")
    print(f"Successful responses: {len(results)}")
    print(f"Errors: {errors}")
    print(f"Time elapsed: {elapsed:.2f}s")
    
    if not results:
        return {
            "throughput": 0,
            "error_rate": 1.0,
            "avg_response_size": 0,
            "buffer_utilization": 0
        }
    
    return {
        "throughput": sum(r["response_size"] for r in results) / elapsed,
        "error_rate": errors / total_requests,
        "avg_response_size": statistics.mean(r["response_size"] for r in results),
        "buffer_utilization": statistics.mean(r["avg_chunk_size"] / r["buffer_size"] for r in results),
        "avg_chunks": statistics.mean(r["num_chunks"] for r in results),
        "avg_chunk_size": statistics.mean(r["avg_chunk_size"] for r in results)
    }

def plot_comparison(results: Dict[str, List[Dict]]):
    """Create comparison visualizations"""
    plt.figure(figsize=(15, 12))
    
    # Convert results to DataFrame
    df = pd.DataFrame([
        {
            "Strategy": strategy,
            **metric
        }
        for strategy, metrics in results.items()
        for metric in metrics
    ])
    
    # Plot 1: Throughput comparison
    plt.subplot(2, 2, 1)
    sns.boxplot(data=df, x="Strategy", y="throughput")
    plt.title("Throughput Comparison")
    plt.ylabel("Characters per Second")
    
    # Plot 2: Error rates
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df, x="Strategy", y="error_rate")
    plt.title("Error Rate Comparison")
    plt.ylabel("Error Rate")
    
    # Plot 3: Buffer utilization
    plt.subplot(2, 2, 3)
    sns.boxplot(data=df, x="Strategy", y="buffer_utilization")
    plt.title("Buffer Utilization")
    plt.ylabel("Utilization Ratio")
    
    # Plot 4: Response size vs throughput
    plt.subplot(2, 2, 4)
    for strategy in df["Strategy"].unique():
        strategy_data = df[df["Strategy"] == strategy]
        plt.scatter(
            strategy_data["avg_response_size"],
            strategy_data["throughput"],
            label=strategy,
            alpha=0.6
        )
    plt.title("Response Size vs Throughput")
    plt.xlabel("Response Size (chars)")
    plt.ylabel("Throughput (chars/s)")
    plt.legend()
    
    plt.tight_layout()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f"benchmarks/plots/buffer_comparison_full_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_path, bbox_inches='tight')
    print(f"\n📈 Plot saved as: {plot_path}")
    
    # Save detailed results
    csv_path = f"benchmarks/results/buffer_comparison_full_{timestamp}.csv"
    os.makedirs("benchmarks/results", exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"📊 Detailed results saved as: {csv_path}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    summary = df.groupby("Strategy").agg({
        "throughput": ["mean", "std"],
        "error_rate": ["mean", "std"],
        "buffer_utilization": ["mean", "std"]
    }).round(3)
    print(summary)

async def run_benchmark(strategy_name: str, config: SystemConfig, prompts: List[str]) -> Dict:
    print(f"\nRunning benchmark for {strategy_name}")
    try:
        metrics = await benchmark_system(config, prompts)
        print(f"\nBenchmark results for {strategy_name}:")
        print(f"Response: {metrics}")
        return metrics
    except Exception as e:
        print(f"\nError in benchmark {strategy_name}:")
        print(f"Exception type: {type(e)}")
        print(f"Exception details: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "throughput": 0,
            "error_rate": 1.0,
            "concurrent_requests": config.max_concurrent,
            "avg_response_size": 0
        }

async def main():
    # Use same diverse prompts as MAP-Elites training
    prompts = [
        # Tiny responses
        "Hi!",
        "Yes.",
        "List 3 colors.",
        "Count to five.",
        "Write one word.",
        
        # Small responses
        "Write a tweet.",
        "Explain what is AI.",
        "Write a haiku.",
        "List 10 fruits.",
        "Define quantum.",
        
        # Medium responses
        "Write a short story.",
        "Explain how a car works.",
        "Write a product review.",
        "List 50 numbers.",
        
        # Large responses
        "Write a technical spec.",
        "Explain quantum physics.",
        "Write a research summary.",
        "List 200 prime numbers.",
        
        # Huge responses
        "Write a detailed essay.",
        "Explain the history of AI.",
        "Write a full story.",
        "Generate a large dataset."
    ]
    
    strategies = {
        "Fixed (128KB)": SimpleBuffer(131072),
        "Dynamic": DynamicBuffer(),
        "MAP-Elites": "map_elites"
    }
    
    # Keep runs small but test all prompt types
    num_runs = 2  # Reduced from 3 since we have more prompts
    num_iterations = 1  # Single iteration per prompt is enough for comparison
    
    # Run all strategies and their iterations in parallel
    tasks = []
    for name, strategy in strategies.items():
        for run in range(num_runs):
            tasks.append((name, strategy, run))
    
    print(f"\nRunning {len(tasks)} benchmarks in parallel...")
    print(f"Testing each strategy with {len(prompts)} diverse prompts")
    
    results = {}
    
    # Create and gather all tasks
    benchmark_tasks = [
        benchmark_buffer_strategy(strategy, prompts)
        for name, strategy, _ in tasks
    ]
    
    # Run all benchmarks concurrently
    metrics_list = await asyncio.gather(*benchmark_tasks)
    
    # Organize results by strategy
    for (name, _, _), metrics in zip(tasks, metrics_list):
        if name not in results:
            results[name] = []
        results[name].append(metrics)
        
        # Print progress
        print(f"{name} - Throughput: {metrics['throughput']:.0f} chars/s, "
              f"Error rate: {metrics['error_rate']:.2%}")
    
    plot_comparison(results)

if __name__ == "__main__":
    asyncio.run(main()) 