import os
import asyncio
from bhumi.client import OpenAIClient

api_key = "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"
MODEL = "gpt-4o-mini"  # Updated to mini model

async def test_openai():
    """Test OpenAI client with a simple prompt"""
    print("\n🚀 Testing OpenAI client...")
    
    # Initialize client with debug mode
    client = OpenAIClient(debug=True)
    
    # Simple test prompt
    prompt = "Write a haiku about coding"
    
    # Send request
    response = await client.acompletion(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        api_key=api_key
    )
    
    print("\n✨ Response:")
    # CompletionResponse now has .text and .raw_response
    print("Text response:", response.text)
    print("\nRaw response:", response.raw_response)

    # Test streaming
    print("\n🌊 Testing streaming...")
    async for chunk in client.astream_completion(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        api_key=api_key
    ):
        print(chunk, end="", flush=True)
    print()  # Final newline

if __name__ == "__main__":
    asyncio.run(test_openai()) 