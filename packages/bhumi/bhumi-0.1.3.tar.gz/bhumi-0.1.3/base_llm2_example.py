import asyncio
from bhumi.client import GroqClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use your actual API key
api_key = os.getenv("GROQ_API_KEY")

async def main():
    # Create Groq client
    client = GroqClient(
        api_key=api_key,
        model="mixtral-8x7b-32768",
        debug=True
    )
    
    # Test completion
    response = await client.completion([
        {"role": "user", "content": "Tell me a joke"}
    ])
    print(f"\nResponse: {response['text']}")
    
    # Test streaming
    print("\nStreaming response:")
    async for chunk in await client.completion([
        {"role": "user", "content": "Count to 5"}
    ], stream=True):
        print(chunk, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(main()) 