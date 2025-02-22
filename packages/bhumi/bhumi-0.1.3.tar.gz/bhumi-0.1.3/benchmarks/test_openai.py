import os
import json
from bhumi.client import OpenAIClient
import time
import requests
os.environ['OPENAI_API_KEY'] = "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"

os.environ['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = "gpt-4o-mini"

def test_direct_openai():
    """Test OpenAI API directly first"""
    print("\n🔍 Testing OpenAI API directly...")
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": "Write a haiku about coding"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status: {response.status_code}")
        print("Response:", response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

def test_openai():
    print("\n🚀 Testing OpenAI via Bhumi...")
    
    # Initialize queue with debug mode
    client = OpenAIClient(
        max_concurrent=1,
        provider="openai",
        model=MODEL,
        debug=True  
    )
    
    # Simple test prompt
    prompt = "Write a haiku about coding"
    
    # Prepare request
    request = {
        "_headers": {
            "Authorization": API_KEY
        },
        "model": MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    print(f"\nSending prompt: '{prompt}'")
    print(f"Request payload: {json.dumps(request, indent=2)}")
    
    # Submit request
    response = client.completion(json.dumps(request))
    
    # Wait for response
    start_time = time.time()
    while True:
        if response := queue.get_response():
            print("\nReceived response:")
            print("=" * 40)
            print(response)
            print("=" * 40)
            print(f"\nResponse time: {time.time() - start_time:.2f}s")
            break
        elif time.time() - start_time > 30:  # 30 second timeout
            print("❌ Timeout waiting for response")
            break
        time.sleep(0.1)

if __name__ == "__main__":
    # Test direct API call first
    test_direct_openai()
    
    # Then test via Bhumi
    test_openai() 