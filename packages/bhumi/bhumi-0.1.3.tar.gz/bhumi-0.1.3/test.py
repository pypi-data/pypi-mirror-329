from bhumi.client import OpenAIClient
from bhumi.models.openai import Message
import asyncio

async def main():
    client = OpenAIClient(debug=True)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]

    response = await client.acompletion(
        model="gpt-4o",
        messages=messages,
        api_key="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"
    )

    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())