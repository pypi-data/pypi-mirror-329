import asyncio
from bhumi.client import GeminiClient
from bhumi.models.gemini import GeminiRequest, Content, Part

# API key for Gemini
API_KEY = "your-gemini-api-key"

async def test_gemini():
    """Test Gemini client with different types of requests"""
    print("\n🚀 Testing Gemini client...")
    
    # Initialize client
    client = GeminiClient(
        max_concurrent=1,
        model="gemini-pro",
        debug=True
    )
    
    # Test 1: Simple text generation
    print("\n📝 Testing text generation...")
    text_response = await client.acompletion(
        model="gemini-pro",
        messages=[
            {
                "role": "user",
                "content": "Write a haiku about coding in Python"
            }
        ],
        api_key=API_KEY
    )
    print("\nHaiku response:")
    print(text_response.text)
    
    # Test 2: Multi-part request with system prompt
    print("\n🔄 Testing multi-part request...")
    multi_response = await client.acompletion(
        model="gemini-pro",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful coding assistant"
            },
            {
                "role": "user",
                "content": "Explain list comprehensions in Python with an example"
            }
        ],
        api_key=API_KEY
    )
    print("\nCoding explanation:")
    print(multi_response.text)
    
    # Test 3: Request with generation config
    print("\n⚙️ Testing with generation config...")
    config_request = GeminiRequest(
        contents=[
            Content(
                parts=[{"text": "Generate a creative story about a programmer"}]
            )
        ],
        generation_config={
            "temperature": 0.9,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 200
        }
    )
    
    config_response = await client.acompletion(
        model="gemini-pro",
        request=config_request,
        api_key=API_KEY
    )
    print("\nCreative story:")
    print(config_response.text)
    
    # Test 4: Image analysis (requires gemini-pro-vision)
    print("\n🖼️ Testing image analysis...")
    image_data = "base64_encoded_image_data..."  # Replace with actual image data
    image_request = GeminiRequest(
        contents=[
            Content(
                parts=[
                    {"text": "What do you see in this image?"},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            )
        ]
    )
    
    try:
        image_response = await client.acompletion(
            model="gemini-pro-vision",
            request=image_request,
            api_key=API_KEY
        )
        print("\nImage analysis:")
        print(image_response.text)
    except Exception as e:
        print(f"Image analysis error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini()) 