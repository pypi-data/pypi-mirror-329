import time
import json
from bhumi.base_client import BaseLLMClient, LLMConfig
import statistics

def python_extract_text(response_str: str, provider: str) -> str:
    response = json.loads(response_str)
    if provider == "gemini":
        return response["candidates"][0]["content"]["parts"][0]["text"]
    elif provider in ("openai", "groq"):
        return response["choices"][0]["message"]["content"]
    elif provider == "anthropic":
        return response["content"][0]["text"]
    return response_str

def benchmark_extraction(num_iterations: int = 1000):
    config = LLMConfig(
        api_key="dummy",
        model="gemini/test",
        provider="gemini"
    )
    client = BaseLLMClient(config)
    
    # Sample responses
    responses = {
        "gemini": '{"candidates":[{"content":{"parts":[{"text":"Hello"}]}}]}',
        "openai": '{"choices":[{"message":{"content":"Hello"}}]}',
        "anthropic": '{"content":[{"text":"Hello"}]}'
    }

    results = {}
    for provider, response in responses.items():
        # Benchmark Python
        py_times = []
        for _ in range(num_iterations):
            start = time.perf_counter()
            python_extract_text(response, provider)
            py_times.append(time.perf_counter() - start)

        # Benchmark Rust
        rust_times = []
        for _ in range(num_iterations):
            start = time.perf_counter()
            client.core._extract_text_rust(response)
            rust_times.append(time.perf_counter() - start)

        results[provider] = {
            "python_avg": statistics.mean(py_times) * 1000,  # Convert to ms
            "rust_avg": statistics.mean(rust_times) * 1000,
            "speedup": statistics.mean(py_times) / statistics.mean(rust_times)
        }

    return results

if __name__ == "__main__":
    results = benchmark_extraction()
    print("\nText Extraction Benchmark Results:")
    print("----------------------------------")
    for provider, stats in results.items():
        print(f"\n{provider.title()}:")
        print(f"Python: {stats['python_avg']:.3f}ms")
        print(f"Rust:   {stats['rust_avg']:.3f}ms")
        print(f"Speedup: {stats['speedup']:.2f}x") 