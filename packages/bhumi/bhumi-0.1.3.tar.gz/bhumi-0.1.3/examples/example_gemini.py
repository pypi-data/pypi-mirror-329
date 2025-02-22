import asyncio
from bhumi.base_client import BaseLLMClient, LLMConfig
import os
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

async def main():
    # Configure for Gemini
    config = LLMConfig(
        api_key=api_key,
        model="gemini/gemini-1.5-flash-8b",  # Using provider/model format
        debug=True
    )
    
    # Create client
    client = BaseLLMClient(config, debug=True)
    
    # Test completion
    response = await client.completion([
        {"role": "user", "content": "Tell me a joke"}
    ])
    print("\nResponse:", response["text"])
    
    # Test streaming
    print("\nStreaming response:", flush=True)
    async for chunk in await client.completion([
        {"role": "user", "content": "Write a short story about a robot discovering emotions"}
    ], stream=True):
        print(chunk, end="", flush=True)  # Print chunks without newlines
    print()  # Add final newline

    # Test with system message and user interaction
    response = await client.completion([
        {"role": "system", "content": "You are a helpful AI assistant that speaks in rhyming verse"},
        {"role": "user", "content": "What's your favorite color and why?"}
    ])
    print(f"\nResponse with system message: {response['text']}")

if __name__ == "__main__":
    asyncio.run(main()) 