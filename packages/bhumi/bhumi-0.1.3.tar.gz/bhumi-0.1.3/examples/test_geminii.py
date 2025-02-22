import asyncio
import os
import dotenv
from bhumi.base import LLMConfig, create_llm

dotenv.load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

async def main():
    # Just specify the model with provider prefix
    config = LLMConfig(
        api_key=API_KEY,
        model="gemini/gemini-pro",  # This automatically sets up Gemini API
        debug=True
    )
    
    # Factory creates the right client type
    client = create_llm(config)
    
    # Test regular completion
    print("\nTesting regular completion:")
    response = await client.completion([
        {"role": "user", "content": "Write a haiku about artificial intelligence"}
    ])
    print(f"\nResponse: {response['text']}")
    
    # Test streaming
    print("\nTesting streaming completion:")
    print("Streaming response:", end="", flush=True)
    async for chunk in await client.completion([
        {"role": "user", "content": "Count from 1 to 5 slowly"}
    ], stream=True):
        print(chunk, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(main()) 