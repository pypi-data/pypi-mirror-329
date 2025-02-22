import asyncio
from bhumi.base_client import BaseLLMClient, LLMConfig
from pydantic import BaseModel, Field
from typing import Literal, List, Dict
import os
import json
import random
from datetime import datetime

# Define the schema as a Pydantic model
class WeatherRequest(BaseModel):
    """Weather request parameters"""
    location: str = Field(..., description="The location to get the weather for")
    unit: Literal["F", "C"] = Field(..., description="The unit to return the temperature in")

class WeatherCall(BaseModel):
    """Record of a weather function call"""
    location: str
    unit: Literal["F", "C"]
    temperature: float
    timestamp: float
    response: str

class WeatherCallSummary(BaseModel):
    """Summary of all weather function calls"""
    total_calls: int
    calls: List[WeatherCall]
    timestamp: datetime = Field(default_factory=datetime.now)

# Track function calls
function_calls: List[WeatherCall] = []

# Mock weather function with random temperatures and logging
async def get_weather(location: str, unit: str) -> str:
    """Get weather for a location"""
    base_temp = random.randint(0, 100)  # Random base temp in F
    temp = base_temp if unit == "F" else round((base_temp - 32) * 5/9)  # Convert to C if needed
    result = f"The temperature in {location} is {temp}°{unit}"
    
    # Log the function call with Pydantic model
    call = WeatherCall(
        location=location,
        unit=unit,
        temperature=temp,
        timestamp=asyncio.get_event_loop().time(),
        response=result
    )
    function_calls.append(call)
    
    print(f"\n>>> Function get_weather() was called:")
    print(call.model_dump_json(indent=2))
    
    return result

async def main():
    # Clear previous function calls
    function_calls.clear()
    
    config = LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="openai/gpt-4o-mini",
        debug=True
    )
    
    client = BaseLLMClient(config)
    
    # Register tool with manual schema like test_tool_calls.py
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
                    "enum": ["F", "C"],
                    "description": "Temperature unit (F for Fahrenheit, C for Celsius)"
                }
            },
            "required": ["location"],
            "additionalProperties": False
        }
    )
    
    test_queries = [
        "What's the weather like in San Francisco?",
        "Tell me the temperature in London in Celsius",
        "How hot is it in Miami right now?",
        "What's the temperature in Tokyo in F?"
    ]
    
    for query in test_queries:
        print(f"\n\nQuery: {query}")
        try:
            response = await client.completion([
                {"role": "user", "content": query}
            ])
            
            # Print raw response for debugging
            print("\nRaw Response:")
            print(json.dumps(response, indent=2))
            
            # Check for tool/function calls in different possible locations
            if "tool_calls" in response:
                print("\nTool Calls Found:")
                for call in response["tool_calls"]:
                    print_function_call(call["function"])
            elif "raw_response" in response and "choices" in response["raw_response"]:
                choice = response["raw_response"]["choices"][0]
                if "message" in choice and "function_call" in choice["message"]:
                    print("\nFunction Call Found:")
                    print_function_call(choice["message"]["function_call"])
                else:
                    print("\nNo function call in message:", json.dumps(choice["message"], indent=2))
            
            print("\nFinal Response:")
            print(response["text"])
            
        except Exception as e:
            print(f"Error: {e}")

    # Create and print summary using Pydantic
    summary = WeatherCallSummary(
        total_calls=len(function_calls),
        calls=function_calls
    )
    
    print("\nFunction Call Summary (JSON):")
    print(summary.model_dump_json(indent=2))
    
    # Save summary to file
    with open("weather_call_summary.json", "w") as f:
        f.write(summary.model_dump_json(indent=2))
    print("\nSummary saved to weather_call_summary.json")

def print_function_call(func):
    """Helper to print and validate function calls"""
    print("\nFunction Call:")
    print(json.dumps(func, indent=2))
    
    try:
        args = WeatherRequest.model_validate_json(func["arguments"])
        print(f"\nValidated Arguments:")
        print(f"Location: {args.location}")
        print(f"Unit: {args.unit}")
    except Exception as e:
        print(f"Schema validation error: {e}")

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    asyncio.run(main()) 