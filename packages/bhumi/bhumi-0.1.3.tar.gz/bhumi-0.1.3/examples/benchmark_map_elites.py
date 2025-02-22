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

dotenv.load_dotenv()

@dataclass
class BufferConfig:
    initial_size: int
    min_size: int
    max_size: int
    adjustment_factor: float
    
    def mutate(self, mutation_rate=0.2) -> 'BufferConfig':
        """Create a mutated copy of this config"""
        return BufferConfig(
            initial_size=int(self.initial_size * random.uniform(1-mutation_rate, 1+mutation_rate)),
            min_size=int(self.min_size * random.uniform(1-mutation_rate, 1+mutation_rate)),
            max_size=int(self.max_size * random.uniform(1-mutation_rate, 1+mutation_rate)),
            adjustment_factor=self.adjustment_factor * random.uniform(1-mutation_rate, 1+mutation_rate)
        )

class MapElitesBuffer:
    """MAP-Elites archive for buffer configurations"""
    def __init__(self, resolution: int = 10):
        self.resolution = resolution
        self.archive: Dict[Tuple[int, int], Tuple[BufferConfig, float]] = {}
        
    def add(self, config: BufferConfig, performance: float, response_length: int, chunk_count: int):
        """Add a configuration to the archive if it's better than existing"""
        # Discretize the behavior space
        length_bin = min(self.resolution-1, int(response_length / 1000))
        chunk_bin = min(self.resolution-1, chunk_count)
        behavior = (length_bin, chunk_bin)
        
        if behavior not in self.archive or performance > self.archive[behavior][1]:
            self.archive[behavior] = (config, performance)
    
    def get_elite(self, response_length: int, chunk_count: int) -> BufferConfig:
        """Get the best configuration for given characteristics"""
        length_bin = min(self.resolution-1, int(response_length / 1000))
        chunk_bin = min(self.resolution-1, chunk_count)
        behavior = (length_bin, chunk_bin)
        
        if behavior in self.archive:
            return self.archive[behavior][0]
        
        # Return nearest neighbor if exact match not found
        nearest = min(self.archive.keys(),
                     key=lambda k: abs(k[0]-length_bin) + abs(k[1]-chunk_bin),
                     default=None)
        return self.archive[nearest][0] if nearest else None

class DynamicBuffer:
    def __init__(self, config: BufferConfig):
        self.config = config
        self.current_size = config.initial_size
        self.chunk_history = []
        
    def adjust(self, chunk_size: int) -> int:
        """Adjust buffer size based on incoming chunk size"""
        self.chunk_history.append(chunk_size)
        
        recent_chunks = self.chunk_history[-5:]
        avg_chunk = statistics.mean(recent_chunks) if recent_chunks else chunk_size
        
        if avg_chunk > self.current_size * 0.8:
            self.current_size = min(
                self.config.max_size,
                int(self.current_size * self.config.adjustment_factor)
            )
        elif avg_chunk < self.current_size * 0.3:
            self.current_size = max(
                self.config.min_size,
                int(self.current_size / self.config.adjustment_factor)
            )
        
        return self.current_size

async def train_map_elites(prompts: List[str], generations: int = 10):
    """Train MAP-Elites archive with different buffer configurations"""
    map_elites = MapElitesBuffer()
    
    # Initial population
    configs = [
        BufferConfig(
            initial_size=random.randint(1024, 131072),
            min_size=random.randint(512, 4096),
            max_size=random.randint(65536, 262144),
            adjustment_factor=random.uniform(1.2, 2.0)
        ) for _ in range(10)
    ]
    
    for generation in range(generations):
        print(f"\nGeneration {generation+1}/{generations}")
        
        # Test each configuration
        for config in configs:
            buffer = DynamicBuffer(config)
            results = await benchmark_buffer(buffer, prompts)
            
            for result in results:
                map_elites.add(
                    config,
                    result["Throughput"],
                    result["Response Length"],
                    result["Num Chunks"]
                )
        
        # Create new population through mutation
        configs = [
            config.mutate()
            for config, _ in random.sample(list(map_elites.archive.values()), 10)
        ]
    
    return map_elites

async def benchmark_buffer(buffer: DynamicBuffer, prompts: List[str]):
    """Benchmark a single buffer configuration"""
    results = []
    api_key = os.getenv("OPENAI_API_KEY")
    
    for prompt in prompts:
        config = LLMConfig(
            api_key=api_key,
            model="openai/gpt-4o-mini",
            buffer_size=buffer.current_size
        )
        client = BaseLLMClient(config)
        
        start_time = time.perf_counter()
        response = await client.completion([
            {"role": "user", "content": prompt}
        ])
        elapsed = time.perf_counter() - start_time
        
        try:
            stats = json.loads(response["raw_response"]["text"])
            chunk_sizes = stats.get("chunk_sizes", [])
            
            for chunk_size in chunk_sizes:
                buffer.adjust(chunk_size)
            
            results.append({
                "Response Length": len(stats["text"]),
                "Num Chunks": len(chunk_sizes),
                "Avg Chunk Size": statistics.mean(chunk_sizes) if chunk_sizes else 0,
                "Buffer Size": buffer.current_size,
                "Response Time": elapsed,
                "Throughput": len(stats["text"]) / elapsed
            })
            
        except Exception as e:
            print(f"Error processing response: {e}")
    
    return results

def plot_map_elites(map_elites: MapElitesBuffer):
    """Visualize the MAP-Elites archive"""
    plt.figure(figsize=(12, 10))
    
    # Create performance matrix
    matrix = np.zeros((map_elites.resolution, map_elites.resolution))
    configs = np.zeros((map_elites.resolution, map_elites.resolution))
    
    for (x, y), (config, perf) in map_elites.archive.items():
        matrix[x, y] = perf
        configs[x, y] = config.initial_size
    
    # Plot performance heatmap
    sns.heatmap(matrix, cmap='viridis')
    plt.title("MAP-Elites Performance Landscape")
    plt.xlabel("Number of Chunks")
    plt.ylabel("Response Length (thousands of chars)")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f"benchmarks/plots/map_elites_{timestamp}.png"
    os.makedirs("benchmarks/plots", exist_ok=True)
    plt.savefig(plot_path, bbox_inches='tight')
    print(f"\n📈 Plot saved as: {plot_path}")

async def main():
    prompts = [
        "Write a one-sentence summary.",
        "Write a detailed paragraph about artificial intelligence.",
        "Explain quantum computing in detail.",
        "Write a short story about time travel.",
        "Describe the entire plot of Star Wars.",
        # Add more diverse prompts
    ]
    
    # Train MAP-Elites
    map_elites = await train_map_elites(prompts)
    plot_map_elites(map_elites)
    
    # Print best configurations
    print("\nBest configurations by response characteristics:")
    for (length_bin, chunk_bin), (config, perf) in map_elites.archive.items():
        print(f"\nResponse length ~{length_bin*1000} chars, {chunk_bin} chunks:")
        print(f"  Initial size: {config.initial_size}")
        print(f"  Min/Max: {config.min_size}/{config.max_size}")
        print(f"  Adjustment factor: {config.adjustment_factor:.2f}")
        print(f"  Performance: {perf:.0f} chars/s")

if __name__ == "__main__":
    asyncio.run(main()) 