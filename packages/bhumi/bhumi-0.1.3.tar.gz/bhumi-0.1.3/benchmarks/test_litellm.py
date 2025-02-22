import asyncio
import os
import json
import time
import litellm
from bhumi import LLMQueue
import matplotlib.pyplot as plt
from datetime import datetime

# Set up API key
os.environ['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = "gpt-4o-mini"

# Test prompts
PROMPTS = [
    "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming",
    "Write a short story about a robot learning to code",
    "What is the capital of France?",
    "What is the capital of France?",
    "What is the capital of France?",
    "What is the capital of France?",
    "What is the capital of France?",
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
     "Write a haiku about coding",
    "Explain quantum computing in one sentence",
    "Tell me a short joke about programming"
]
def plot_results(litellm_results, litellm_async_results, bhumi_results):
    """Plot comparison graphs"""
    plt.figure(figsize=(12, 5))
    
    # Colors - matching the first file's scheme
    colors = {
        'LiteLLM\n(Sequential)': '#333333',
        'LiteLLM\n(Async)': '#666666',
        'Bhumi\n(Native)': '#90EE90'  # Light green/pastel
    }
    
    # Plot 1: Total Response Time
    plt.subplot(1, 2, 1)
    implementations = list(colors.keys())
    total_times = [
        litellm_results['total_time'], 
        litellm_async_results['total_time'],
        bhumi_results['total_time']
    ]
    
    bars = plt.bar(implementations, total_times, color=[colors[i] for i in implementations])
    plt.title('Total Response Time')
    plt.ylabel('Time (seconds)')
    for bar, val in zip(bars, total_times):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.2f}s', ha='center', va='bottom')
    
    # Plot 2: Throughput
    plt.subplot(1, 2, 2)
    throughput = [len(PROMPTS)/t for t in total_times]
    
    bars = plt.bar(implementations, throughput, color=[colors[i] for i in implementations])
    plt.title('Throughput')
    plt.ylabel('Requests/Second')
    for bar, val in zip(bars, throughput):
        plt.text(bar.get_x() + bar.get_width()/2, val, 
                f'{val:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_filename = f"openai_comparison_{timestamp}.png"
    plt.savefig(plot_filename)
    print(f"\n📈 Plot saved as: {plot_filename}")
def test_litellm():
    """Test OpenAI via LiteLLM"""
    print("\n🚀 Testing OpenAI via LiteLLM...")
    
    total_start = time.time()
    responses = []
    
    for prompt in PROMPTS:
        print(f"\nSending prompt: '{prompt}'")
        
        start_time = time.time()
        try:
            response = litellm.completion(
                model=f"openai/{MODEL}",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt}
                ],
                api_key=API_KEY
            )
            
            elapsed = time.time() - start_time
            responses.append((prompt, response.choices[0].message.content, elapsed))
            print(f"Response time: {elapsed:.2f}s")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
    
    total_time = time.time() - total_start
    print("\nLiteLLM Results:")
    print("=" * 60)
    for prompt, response, elapsed in responses:
        print(f"\nPrompt: {prompt}")
        print(f"Response time: {elapsed:.2f}s")
        print(f"Response: {response}")
    print("=" * 60)
    print(f"Total time for all requests: {total_time:.2f}s")
    
    return {
        'responses': responses,
        'total_time': total_time
    }

def test_bhumi():
    """Test OpenAI via Bhumi"""
    print("\n🚀 Testing OpenAI via Bhumi...")
    
    queue = LLMQueue(
        max_concurrent=60,  # Match number of prompts
        provider="openai",
        model=MODEL,
        debug=False
    )
    
    total_start = time.time()
    responses = {}
    request_times = {}
    
    # Submit all requests
    for i, prompt in enumerate(PROMPTS):
        request = {
            "_headers": {
                "Authorization": API_KEY
            },
            "model": MODEL,
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
        request_times[i] = time.time()
        queue.submit(json.dumps(request))
    
    # Collect responses
    while len(responses) < len(PROMPTS):
        if response := queue.get_response():
            idx = len(responses)
            elapsed = time.time() - request_times[idx]
            responses[idx] = (PROMPTS[idx], response, elapsed)
    
    total_time = time.time() - total_start

    
    return {
        'responses': responses,
        'total_time': total_time
    }

async def test_litellm_async():
    """Test OpenAI via LiteLLM with async/await"""
    print("\n🚀 Testing OpenAI via LiteLLM (Async)...")
    
    total_start = time.time()
    responses = []
    semaphore = asyncio.Semaphore(60)  # Match Bhumi's worker count
    
    async def process_prompt(prompt):
        async with semaphore:
            start_time = time.time()
            try:
                # Run LiteLLM in thread pool since it's synchronous
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: litellm.completion(
                        model=f"openai/{MODEL}",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant"},
                            {"role": "user", "content": prompt}
                        ],
                        api_key=API_KEY
                    )
                )
                elapsed = time.time() - start_time
                responses.append((prompt, response.choices[0].message.content, elapsed))
                print(f"Response time: {elapsed:.2f}s")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    # Create tasks for all prompts
    tasks = [process_prompt(prompt) for prompt in PROMPTS]
    await asyncio.gather(*tasks)
    
    total_time = time.time() - total_start
    print("\nLiteLLM Async Results:")
    print("=" * 60)
    for prompt, response, elapsed in sorted(responses, key=lambda x: PROMPTS.index(x[0])):
        print(f"\nPrompt: {prompt}")
        print(f"Response time: {elapsed:.2f}s")
        print(f"Response: {response}")
    print("=" * 60)
    print(f"Total time for all requests: {total_time:.2f}s")
    
    return {
        'responses': responses,
        'total_time': total_time
    }

if __name__ == "__main__":
    litellm_results = test_litellm()
    print("\n" + "=" * 80 + "\n")
    litellm_async_results = asyncio.run(test_litellm_async())
    print("\n" + "=" * 80 + "\n")
    bhumi_results = test_bhumi()
    
    # Plot comparison graphs
    plot_results(litellm_results, litellm_async_results, bhumi_results) 