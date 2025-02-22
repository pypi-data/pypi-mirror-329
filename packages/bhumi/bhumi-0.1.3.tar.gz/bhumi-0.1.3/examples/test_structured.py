import asyncio
from bhumi.base_client import BaseLLMClient, LLMConfig
from pydantic import BaseModel, Field
from typing import List, Optional
import os

# Simple product schema
class ProductInfo(BaseModel):
    """Product information with a simple structure.
    Example:
    {
        "name": "MacBook Pro",
        "category": "electronics",
        "description": "High-performance laptop",
        "price": 1299.99,
        "in_stock": true,
        "stock_count": 42
    }
    """
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price in USD")
    in_stock: bool = Field(..., description="Whether the product is in stock")
    stock_count: int = Field(..., description="Number of units in stock")

async def main():
    config = LLMConfig(
        api_key=os.getenv("GROQ_API_KEY"),
        model="groq/deepseek-r1-distill-qwen-32b",
        debug=True
    )
    
    client = BaseLLMClient(config)
    client.set_structured_output(ProductInfo)
    
    test_queries = [
        "Tell me about the MacBook Pro laptop",
        "What's the pricing for a leather sofa?",
        "Give me basic information about the Python Programming book"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = await client.completion([
                {"role": "system", "content": """You are a product information assistant.
                    ALWAYS return product information in this EXACT format:
                    {
                        "name": "Product Name",
                        "category": "Category",
                        "description": "Description",
                        "price": 99.99,
                        "in_stock": true,
                        "stock_count": 42
                    }"""},
                {"role": "user", "content": query}
            ])
            
            if hasattr(response, 'think'):
                print("\nReasoning:")
                print(response.think)
                
                try:
                    # Extract JSON from the response if needed
                    output = response._output
                    if "<response>" in output:
                        output = output[output.find("<response>")+10:output.find("</response>")]
                    if "```" in output:
                        output = output[output.find("{"): output.rfind("}")+1]
                    
                    # Parse into Pydantic model
                    data = ProductInfo.model_validate_json(output)
                    
                    # Show individual fields
                    print("\nProduct Information:")
                    print(f"Name: {data.name}")
                    print(f"Category: {data.category}")
                    print(f"Description: {data.description}")
                    print(f"Price: ${data.price:.2f}")
                    print(f"In Stock: {data.in_stock}")
                    print(f"Stock Count: {data.stock_count}")
                    
                except Exception as e:
                    print(f"\nFailed to parse structured data: {e}")
                    print("\nRaw Response:")
                    print(response)
            else:
                print("\nResponse:")
                print(response["text"])
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    asyncio.run(main()) 