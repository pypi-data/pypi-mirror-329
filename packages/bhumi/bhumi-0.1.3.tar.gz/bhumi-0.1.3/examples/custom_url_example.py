from bhumi.client import OpenAIClient

# Use default URL
client = OpenAIClient(
    debug=True,
    model="gpt-4"
)

# Use custom URL
custom_client = OpenAIClient(
    debug=True,
    model="gpt-4",
    base_url="https://your-custom-endpoint.com/v1"
)

# The gpt-4o model will automatically use the sandbox URL
sandbox_client = OpenAIClient(
    debug=True,
    model="gpt-4o-mini"
) 