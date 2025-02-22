import asyncio
import time
import numpy as np
import matplotlib.pyplot as plt
from groq import AsyncGroq
from bhumi.base_client import BaseLLMClient, LLMConfig
import os
from dotenv import load_dotenv
import pandas as pd
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize clients
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
bhumi_config = LLMConfig(
    api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768",
    debug=False
)
bhumi_client = BaseLLMClient(bhumi_config)

# Smaller set of test prompts
BATCH_PROMPTS = [
    "What is the capital of France?",
    "What is the capital of Japan?",
    "What is the capital of Brazil?",
    "What is the capital of Australia?"
]

async def process_native_groq_sequential(prompts: List[str]) -> Dict:
    """Process prompts sequentially using native Groq"""
    start_time = time.time()
    responses = []
    total_tokens = 0
    
    for prompt in prompts:
        completion = await groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        responses.append(completion)
        total_tokens += completion.usage.total_tokens
    
    end_time = time.time()
    total_time = end_time - start_time
    
    return {
        "total_time": total_time,
        "total_tokens": total_tokens,
        "tokens_per_second": total_tokens / total_time,
        "responses": len(responses)
    }

async def process_bhumi_batch(prompts: List[str]) -> Dict:
    """Process prompts in batch using Bhumi"""
    start_time = time.time()
    
    messages = [{"role": "user", "content": prompt} for prompt in prompts]
    
    responses = await asyncio.gather(*[
        bhumi_client.completion([msg]) for msg in messages
    ])
    
    end_time = time.time()
    total_time = end_time - start_time
    
    total_tokens = sum(r.get('usage', {}).get('total_tokens', 0) for r in responses)
    
    return {
        "total_time": total_time,
        "total_tokens": total_tokens,
        "tokens_per_second": total_tokens / total_time,
        "responses": len(responses)
    }

async def run_batch_benchmark(batch_sizes: List[int] = [1, 2, 4], n_runs: int = 2):
    results = []
    
    for batch_size in batch_sizes:
        print(f"\nTesting batch size: {batch_size}")
        prompts = BATCH_PROMPTS[:batch_size]
        
        for implementation in ["Native Groq (Sequential)", "Bhumi (Batch)"]:
            print(f"Testing {implementation}...")
            
            for run in range(n_runs):
                print(f"Run {run + 1}/{n_runs}")
                try:
                    if implementation == "Native Groq (Sequential)":
                        metrics = await process_native_groq_sequential(prompts)
                    else:
                        metrics = await process_bhumi_batch(prompts)
                    
                    results.append({
                        "implementation": implementation,
                        "batch_size": batch_size,
                        "run": run + 1,
                        **metrics
                    })
                    
                    # Add small delay between runs to avoid rate limits
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"Error in {implementation} run {run + 1}: {e}")
                    continue
    
    return pd.DataFrame(results)

def plot_batch_results(df: pd.DataFrame):
    # Set basic style
    plt.rcParams['figure.figsize'] = [12, 5]
    plt.rcParams['figure.dpi'] = 300
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    # Plot 1: Total Time vs Batch Size
    for impl in df['implementation'].unique():
        data = df[df['implementation'] == impl]
        ax1.plot(data['batch_size'], data['total_time'], 
                marker='o', label=impl, linestyle='-')
    
    ax1.set_title('Processing Time vs Batch Size')
    ax1.set_ylabel('Total Time (seconds)')
    ax1.set_xlabel('Batch Size')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Tokens per Second vs Batch Size
    for impl in df['implementation'].unique():
        data = df[df['implementation'] == impl]
        ax2.plot(data['batch_size'], data['tokens_per_second'], 
                marker='o', label=impl, linestyle='-')
    
    ax2.set_title('Throughput vs Batch Size')
    ax2.set_ylabel('Tokens per Second')
    ax2.set_xlabel('Batch Size')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('groq_batch_benchmark_results.png')
    plt.close()
    
    # Calculate summary statistics
    summary = df.groupby(['implementation', 'batch_size']).agg({
        'total_time': ['mean', 'std'],
        'tokens_per_second': ['mean', 'std']
    }).round(3)
    
    # Calculate speedup ratios
    batch_sizes = df['batch_size'].unique()
    speedup_ratios = []
    
    for batch_size in batch_sizes:
        native_time = df[
            (df['implementation'] == "Native Groq (Sequential)") & 
            (df['batch_size'] == batch_size)
        ]['total_time'].mean()
        
        bhumi_time = df[
            (df['implementation'] == "Bhumi (Batch)") & 
            (df['batch_size'] == batch_size)
        ]['total_time'].mean()
        
        speedup = native_time / bhumi_time
        speedup_ratios.append({
            'batch_size': batch_size,
            'speedup_ratio': speedup
        })
    
    speedup_df = pd.DataFrame(speedup_ratios)
    
    return summary, speedup_df

async def main():
    print("Starting batch processing benchmark...")
    print("Using model: mixtral-8x7b-32768")
    
    results_df = await run_batch_benchmark()
    summary, speedup = plot_batch_results(results_df)
    
    print("\nBenchmark Summary:")
    print(summary)
    print("\nSpeedup Ratios (Bhumi vs Native):")
    print(speedup)
    print("\nResults have been saved to groq_batch_benchmark_results.png")

if __name__ == "__main__":
    asyncio.run(main()) 