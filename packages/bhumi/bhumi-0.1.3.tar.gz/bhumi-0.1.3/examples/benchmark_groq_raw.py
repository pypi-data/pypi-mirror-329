import time
import asyncio
import numpy as np
from groq import AsyncGroq
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# Test prompts of varying lengths
SHORT_PROMPT = "What is the capital of France?"

MEDIUM_PROMPT = """
Explain the process of photosynthesis in detail, including the light-dependent 
and light-independent reactions. How do plants convert sunlight into energy? 
What are the main products of photosynthesis?
"""

LONG_PROMPT = """
Write a comprehensive analysis of the major themes in George Orwell's '1984', 
including discussions of surveillance, totalitarianism, and the manipulation of 
truth. How do these themes relate to modern society? Provide specific examples 
from the book and draw parallels to contemporary issues. Additionally, analyze 
the significance of the novel's ending and its implications for the overall 
message of the work. Consider the role of language and the concept of 'doublethink' 
in the narrative. How does Orwell's use of language contribute to the dystopian 
atmosphere of the novel? Finally, discuss the relevance of '1984' in today's 
digital age and its warnings about privacy and governmental control.
"""

async def measure_completion(
    prompt: str,
    model: str = "mixtral-8x7b-32768",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Dict:
    """Measure completion metrics for a single prompt."""
    
    start_time = time.time()
    
    completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    end_time = time.time()
    
    latency = end_time - start_time
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens
    tokens_per_second = total_tokens / latency
    
    return {
        "latency": latency,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "tokens_per_second": tokens_per_second,
        "response": completion.choices[0].message.content
    }

async def run_benchmark(n_runs: int = 3):
    """Run benchmark across different prompt lengths."""
    
    models = [
        "mixtral-8x7b-32768",
        "llama-3.1-8b-instant",
        "gemma2-9b-it"
    ]
    
    prompts = {
        "short": SHORT_PROMPT,
        "medium": MEDIUM_PROMPT,
        "long": LONG_PROMPT
    }
    
    results = {}
    
    for model in models:
        print(f"\nBenchmarking {model}...")
        model_results = {}
        
        for prompt_type, prompt in prompts.items():
            print(f"\nTesting {prompt_type} prompt...")
            runs = []
            
            for i in range(n_runs):
                print(f"Run {i + 1}/{n_runs}")
                try:
                    result = await measure_completion(prompt, model=model)
                    runs.append(result)
                    print(f"Latency: {result['latency']:.2f}s, "
                          f"Tokens/s: {result['tokens_per_second']:.2f}")
                except Exception as e:
                    print(f"Error in run {i + 1}: {e}")
                    continue
            
            if runs:
                avg_latency = np.mean([r["latency"] for r in runs])
                avg_tokens_per_second = np.mean([r["tokens_per_second"] for r in runs])
                
                model_results[prompt_type] = {
                    "average_latency": avg_latency,
                    "average_tokens_per_second": avg_tokens_per_second,
                    "input_tokens": runs[0]["input_tokens"],
                    "output_tokens": runs[0]["output_tokens"],
                    "sample_response": runs[0]["response"][:200] + "..."  # First 200 chars
                }
        
        results[model] = model_results
    
    return results

def print_results(results: Dict):
    """Print benchmark results in a formatted way."""
    
    print("\n=== GROQ BENCHMARK RESULTS ===\n")
    
    for model, model_results in results.items():
        print(f"\nModel: {model}")
        print("=" * (len(model) + 8))
        
        for prompt_type, metrics in model_results.items():
            print(f"\n{prompt_type.upper()} PROMPT:")
            print(f"Average Latency: {metrics['average_latency']:.2f} seconds")
            print(f"Average Tokens/s: {metrics['average_tokens_per_second']:.2f}")
            print(f"Input Tokens: {metrics['input_tokens']}")
            print(f"Output Tokens: {metrics['output_tokens']}")
            print("\nSample Response:")
            print(metrics['sample_response'])
            print("-" * 80)

async def main():
    results = await run_benchmark()
    print_results(results)

if __name__ == "__main__":
    asyncio.run(main()) 