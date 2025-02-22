import asyncio
import os
from bhumi.base_client import BaseLLMClient, LLMConfig
from dotenv import load_dotenv

# Simple mock weather tool
async def get_weather(location: str, unit: str = "f") -> str:
    return f"The weather in {location} is 75°{unit}"

async def main():
    # Load environment variables
    load_dotenv()
    
    # Configure for your chosen provider
    provider = "openai"  # Change to "groq" or "sambanova"
    model = "gpt-4"      # Change to appropriate model
    
    # Get API key based on provider
    api_key_map = {
        "openai": "OPENAI_API_KEY",
        "groq": "GROQ_API_KEY",
        "sambanova": "SAMBANOVA_API_KEY"
    }
    
    api_key = os.getenv(api_key_map[provider])
    if not api_key:
        raise ValueError(f"No API key found for {provider}")
    
    # Create client
    config = LLMConfig(
        api_key=api_key,
        model=f"{provider}/{model}",
        debug=True
    )
    
    client = BaseLLMClient(config)
    
    # Register weather tool
    client.register_tool(
        name="get_weather",
        func=get_weather,
        description="Get the current weather for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["c", "f"]
                }
            },
            "required": ["location"]
        }
    )
    
    # Test the tool
    test_queries = [
        "What's the weather like in San Francisco?",
        "Tell me the temperature in New York City",
        "I'm planning a trip to Miami, how's the weather there?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = await client.completion([
                {"role": "user", "content": query}
            ])
            print(f"Response: {response['text']}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 