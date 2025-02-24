# test.py
import asyncio
from .core import scrape_product

async def main():
    # Define the fields you want to extract with their types
    fields = {
        "description": {
            "description": "Description of the product",
            "type": "string"
        },
        "title": {
            "description": "Title of the product",
            "type": "string"
        },
        "product_image_urls": {
            "description": "Unique image URLs of the product",
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
    
    # Test with OpenRouter and specific model
    result = await scrape_product(
        url="https://www.knncalcutta.com/collections/crewnecks-hoodies/products/bluetooth-hoodie",
        fields_to_extract=fields,
        provider="openai",
        headless=True,
        api_key="sk-BJ1KdTa8zbA7JbvBy5_CUwY3OY4PZc_8UDSkF_MlA-T3BlbkFJn__E7fK8l5YGrUwsP_D2ewwGWe5pxRqJdq9_Db5voA",
        model="",  # Specify the model here
        system_prompt="From this information, please extract the data of the title of the product, description of the product and a list of the image URLs"
    )
    
    if result["success"]:
        print("\nSuccessfully extracted data:")
        print("\nData:")
        for field, value in result["data"].items():
            print(f"{field}: {value}")
        print("\nAPI Usage:", result["usage"])
    else:
        print("\nError occurred:", result["error"])

if __name__ == "__main__":
    asyncio.run(main())