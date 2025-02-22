import asyncio
import os
from bhumi.base_client import BaseLLMClient, LLMConfig
from typing import Dict
import json

# Simple mock weather tool that always returns 75 degrees
async def get_weather(location: str, unit: str = "f") -> str:
    return f"The weather in {location} is 75°{unit}"

# Test tool calling with different providers
async def test_provider(provider: str, model: str, api_key: str) -> Dict[str, str]:
    """Test tool calling with a specific provider"""
    config = LLMConfig(
        api_key=api_key,
        model=f"{provider}/{model}",
        debug=True
    )
    
    client = BaseLLMClient(config)
    
    # Register the weather tool
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
                    "enum": ["c", "f"],
                    "description": "Temperature unit (c for Celsius, f for Fahrenheit)"
                }
            },
            "required": ["location"],
            "additionalProperties": False
        }
    )
    
    # Test with different weather queries
    test_messages = [
        "What's the weather like in San Francisco?",
        "Tell me the temperature in New York City",
        "How hot is it in Miami right now?"
    ]
    
    results = {}
    for msg in test_messages:
        try:
            response = await client.completion([
                {"role": "user", "content": msg}
            ])
            results[msg] = response['text']
        except Exception as e:
            results[msg] = f"Error: {str(e)}"
    
    return results

async def main():
    # Provider configurations
    providers = {
        "openai": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        },
        "groq": {
            "model": "qwen-2.5-32b",
            "api_key": os.getenv("GROQ_API_KEY")
        },
        "sambanova": {
            "model": "Meta-Llama-3.1-8B-Instruct",
            "api_key": os.getenv("SAMBANOVA_API_KEY")
        }
    }
    
    # Test each provider
    all_results = {}
    for provider, config in providers.items():
        if config["api_key"]:
            print(f"\nTesting {provider.upper()}...")
            try:
                results = await test_provider(
                    provider=provider,
                    model=config["model"],
                    api_key=config["api_key"]
                )
                all_results[provider] = results
                
                # Print results nicely
                print(f"\n{provider.upper()} Results:")
                for query, response in results.items():
                    print(f"\nQuery: {query}")
                    print(f"Response: {response}")
                    
            except Exception as e:
                print(f"Error testing {provider}: {str(e)}")
        else:
            print(f"\nSkipping {provider} - no API key found")
    
    # Save results to file
    with open("tool_call_test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nResults saved to tool_call_test_results.json")

if __name__ == "__main__":
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    asyncio.run(main()) 