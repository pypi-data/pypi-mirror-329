import asyncio
from bhumi.base_client import BaseLLMClient, LLMConfig

# Custom LLM configuration (example: self-hosted Llama model)
api_key = "custom_key_123"  # Could be any authentication token
MODEL = "llama-2-70b"  # Example model name

async def main():
    # Example 1: Self-hosted Llama
    llama_config = LLMConfig(
        api_key=api_key,
        base_url="http://localhost:8000/v1",  # Local server
        model=MODEL,
        provider="custom",  # Custom provider
        headers={
            "X-Custom-Header": "value",  # Additional headers if needed
        },
        debug=True
    )
    
    llama_client = BaseLLMClient(llama_config, debug=True)
    
    # Example 2: Together.ai API
    together_config = LLMConfig(
        api_key="tok_somekey",
        base_url="https://api.together.xyz/v1",
        model="togethercomputer/llama-2-70b",
        provider="custom",
        debug=True
    )
    
    together_client = BaseLLMClient(together_config, debug=True)
    
    # Example 3: Anthropic-compatible API
    claude_config = LLMConfig(
        api_key="custom_claude_key",
        base_url="https://custom-claude-api.com/v1",
        model="claude-3-opus",
        provider="custom",
        headers={
            "anthropic-version": "2024-01-01",  # Custom API version
        },
        debug=True
    )
    
    claude_client = BaseLLMClient(claude_config, debug=True)
    
    # Test with different prompts for each provider
    clients = {
        "Local Llama": llama_client,
        "Together.ai": together_client,
        "Custom Claude": claude_client
    }
    
    for name, client in clients.items():
        print(f"\nTesting {name}:")
        try:
            # Regular completion
            print("\nRegular completion:")
            response = await client.completion([
                {"role": "user", "content": "What's your model name?"}
            ])
            print(f"Response: {response['text']}")
            
            # Streaming completion
            print("\nStreaming completion:")
            print("Response: ", end="", flush=True)
            async for chunk in client.completion([
                {"role": "user", "content": "Count from 1 to 5 slowly."}
            ], stream=True):
                print(chunk, end="", flush=True)
                await asyncio.sleep(0.1)  # Simulate slower streaming for demo
            print("\n")
            
            # Test with system message
            print("\nWith system message:")
            response = await client.completion([
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "What kind of assistant are you?"}
            ])
            print(f"Response: {response['text']}")
            
        except Exception as e:
            print(f"Error testing {name}: {str(e)}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(main()) 