import asyncio
from bhumi.client import OpenAIClient

async def test_streaming():
    client = OpenAIClient(debug=True)
    
    async for chunk in client.astream_completion(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Write a story about a robot"}
        ],
        api_key="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"
    ):
        print(chunk, end="", flush=True)
    print()  # Final newline

if __name__ == "__main__":
    asyncio.run(test_streaming()) 