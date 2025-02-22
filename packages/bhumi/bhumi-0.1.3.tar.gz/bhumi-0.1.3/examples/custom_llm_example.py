import asyncio
from bhumi.base import LLMConfig
from bhumi.providers.openai_provider import OpenAILLM

async def main():
    config = LLMConfig(
        api_key="your-api-key",
        base_url="https://api.openai.com/v1",
        model="gpt-4",
        organization="your-org-id",  # optional
        debug=True
    )
    
    llm = OpenAILLM(config)
    
    # Regular completion
    response = await llm.completion([
        {"role": "user", "content": "Tell me a joke"}
    ])
    print(f"Regular response: {response['text']}")
    
    # Streaming completion
    print("\nStreaming response:")
    async for chunk in llm.completion([
        {"role": "user", "content": "Tell me a joke"}
    ], stream=True):
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main()) 