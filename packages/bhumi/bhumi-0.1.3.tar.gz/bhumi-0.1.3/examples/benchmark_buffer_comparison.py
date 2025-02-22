import time
import asyncio
import statistics
from bhumi.base_client import BaseLLMClient, LLMConfig
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd

async def test_both_buffers(prompt: str, byte_size: int = 131072, char_size: int = 10000) -> dict:
    """Test both byte-based and character-based buffering"""
    
    # Test byte-based buffering
    byte_config = LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="openai/gpt-4o-mini",
        buffer_size=byte_size
    )
    byte_client = BaseLLMClient(byte_config)
    
    # Test character-based buffering
    char_config = LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="openai/gpt-4o-mini",
        buffer_size=char_size
    )
    char_client = BaseLLMClient(char_config)
    
    # Run tests
    results = {}
    for name, client in [("Byte-based", byte_client), ("Character-based", char_client)]:
        start = time.perf_counter()
        response = await client.completion([
            {"role": "user", "content": prompt}
        ])
        elapsed = time.perf_counter() - start
        
        results[name] = {
            "time": elapsed,
            "response_length": len(response["text"]),
            "throughput": len(response["text"]) / elapsed
        }
    
    return results

async def run_comparison():
    """Run comprehensive comparison between buffering methods"""
    
    # Test prompts of varying lengths/complexity
    prompts = [
        ("Short", "Write a one-sentence summary of AI."),
        ("Medium", "Write a detailed paragraph explaining quantum computing."),
        ("Long", "Write a comprehensive essay about the history of computing."),
        ("Complex", "Write a technical analysis of modern neural network architectures."),
        ("Very Long", "Write a detailed story about a time traveler visiting different technological eras.")
    ]
    
    all_results = []
    
    for prompt_type, prompt in prompts:
        print(f"\nTesting {prompt_type} prompt...")
        results = await test_both_buffers(prompt)
        
        # Add results to collection
        for method, metrics in results.items():
            all_results.append({
                "Prompt Type": prompt_type,
                "Method": method,
                "Response Time (s)": metrics["time"],
                "Response Length": metrics["response_length"],
                "Throughput (chars/s)": metrics["throughput"]
            })
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(all_results)
    
    # Create comparison plots
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Response Times
    plt.subplot(2, 1, 1)
    for method in ["Byte-based", "Character-based"]:
        data = df[df["Method"] == method]
        plt.plot(data["Prompt Type"], data["Response Time (s)"], 
                marker='o', label=method)
    
    plt.title("Response Time Comparison")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    
    # Plot 2: Throughput
    plt.subplot(2, 1, 2)
    for method in ["Byte-based", "Character-based"]:
        data = df[df["Method"] == method]
        plt.plot(data["Prompt Type"], data["Throughput (chars/s)"], 
                marker='o', label=method)
    
    plt.title("Throughput Comparison")
    plt.ylabel("Characters per Second")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
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
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("\nAverage Response Times:")
    for method in ["Byte-based", "Character-based"]:
        avg_time = df[df["Method"] == method]["Response Time (s)"].mean()
        print(f"{method}: {avg_time:.3f}s")
    
    print("\nAverage Throughput:")
    for method in ["Byte-based", "Character-based"]:
        avg_throughput = df[df["Method"] == method]["Throughput (chars/s)"].mean()
        print(f"{method}: {avg_throughput:.0f} chars/s")

if __name__ == "__main__":
    asyncio.run(run_comparison()) 