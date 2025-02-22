import asyncio
from bhumi.base_client import BaseLLMClient, LLMConfig

# Groq configuration
api_key = "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"  # Replace with your Groq API key
MODEL = "mixtral-8x7b-32768"  # or "llama2-70b-4096"

async def main():
    # Configure Groq client
    config = LLMConfig(
        api_key=api_key,
        base_url="https://api.groq.com/v1",
        model=MODEL,
        # provider="groq",
        debug=True
    )
    
    client = BaseLLMClient(config, debug=True)
    
    # Test both regular and streaming completion
    prompt = "Write a short story about a time-traveling robot. Make it exactly 100 words."
    
    print("\nTesting regular completion:")
    response = await client.completion([
        {"role": "user", "content": prompt}
    ])
    print(f"\nRegular response: {response['text']}")
    
    print("\nTesting streaming completion:")
    print("Streaming response:", end="", flush=True)
    async for chunk in client.completion([
        {"role": "user", "content": prompt}
    ], stream=True):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Compare response times
    print("\nComparing response times:")
    
    # Regular completion timing
    start_time = asyncio.get_event_loop().time()
    await client.completion([
        {"role": "user", "content": "Tell me a quick joke"}
    ])
    regular_time = asyncio.get_event_loop().time() - start_time
    print(f"Regular completion time: {regular_time:.2f}s")
    
    # Streaming completion timing
    start_time = asyncio.get_event_loop().time()
    first_token_time = None
    async for chunk in client.completion([
        {"role": "user", "content": "Tell me a quick joke"}
    ], stream=True):
        if first_token_time is None:
            first_token_time = asyncio.get_event_loop().time() - start_time
    stream_total_time = asyncio.get_event_loop().time() - start_time
    
    print(f"Streaming first token: {first_token_time:.2f}s")
    print(f"Streaming total time: {stream_total_time:.2f}s")
    print(f"Streaming is {regular_time/first_token_time:.1f}x faster to first token")

if __name__ == "__main__":
    asyncio.run(main()) 