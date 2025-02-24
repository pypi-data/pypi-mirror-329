import asyncio
from typing import Dict, Any, Optional
from .models import MediaConfig, ScrapeConfig, SchemaConfig, ExtractConfig
from .scraper import WebScraper
from .exceptions import ValidationError, LLMException

async def scrape_product(
    url: str,
    fields_to_extract: Dict[str, Dict[str, Any]],
    provider: str = "openai",
    api_key: str = None,
    model: Optional[str] = None,  # Optional model parameter
    system_prompt: Optional[str] = None,
    headless: bool = True,  # Added headless parameter
    wait_time: int = 1000
) -> Dict[str, Any]:
    """
    Scrape a product page and extract specified fields with type specifications.
    
    Args:
        url: The URL of the product page to scrape
        fields_to_extract: Dictionary of field names and their specifications
        provider: Either "openai" or "openrouter" (default: "openai")
        api_key: Your API key for the chosen provider
        model: Model to use for OpenRouter (ignored for OpenAI)
        system_prompt: Optional custom prompt for the LLM
        wait_time: Time to wait after page load in milliseconds
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if the scrape was successful
            - data: The extracted data if successful
            - usage: API usage information if successful
            - error: Error message if not successful
    """
    try:
        # Create schema configuration
        schema_data = {
            "type": "object",
            "schema_definition": {
                "properties": {
                    field_name: {
                        "type": field_spec.get("type", "string"),
                        "description": field_spec["description"],
                        **({"items": field_spec["items"]} if field_spec.get("type") == "array" else {}),
                        **({"properties": field_spec["properties"]} if field_spec.get("type") == "object" else {})
                    }
                    for field_name, field_spec in fields_to_extract.items()
                }
            }
        }
        
        schema = SchemaConfig(**schema_data)

        # Use default system prompt if none provided
        if not system_prompt:
            system_prompt = (
                "Extract the requested information from the web page. "
                "Be precise and ensure all requested fields are populated with "
                "accurate information from the page content. "
                "Follow the specified data types exactly."
            )

        # Create configuration
        config = ScrapeConfig(
            url=url,
            wait_after_load=wait_time,
            headless=headless,
            media=MediaConfig(
                block_loading=False,
                preserve_urls=True,
                extract_srcsets=True,
                make_urls_absolute=True
            ),
            extract=ExtractConfig(
                system_prompt=system_prompt,
                schema_data=schema,
                provider=provider,
                api_key=api_key,
                model=model if provider == "openrouter" else None  # Only set model for OpenRouter
            )
        )

        # Initialize and run scraper
        scraper = WebScraper()
        try:
            result = await scraper.scrape(config)
            return {
                "success": True,
                "data": result['extracted_data']['extract'],
                "usage": result['extracted_data']['usage']
            }
        finally:
            await scraper.cleanup()

    except ValidationError as e:
        return {
            "success": False,
            "error": f"Validation error: {str(e)}"
        }
    except LLMException as e:
        return {
            "success": False,
            "error": f"LLM error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
