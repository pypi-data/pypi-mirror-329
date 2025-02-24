# Web Scraper with LLM Extraction

A powerful and lightweight web scraping library with LLM extraction capabilities. This library combines web scraping with AI-powered content extraction using either OpenAI or OpenRouter APIs.

## Features

- Configurable web scraping with Playwright
- Support for both headless and visible browser modes
- Content cleaning and preprocessing
- LLM-based information extraction
- Support for both OpenAI and OpenRouter APIs
- Customizable schema definitions with type specifications:
  - String fields
  - Array fields
  - Object fields with nested properties
- Ad blocking and media handling
- Automatic handling of srcset attributes
- HTML minification support

## Installation

```bash
pip install aiohttp>=3.8.0
pip install beautifulsoup4>=4.9.3
pip install fake-useragent>=0.1.11
pip install playwright>=1.20.0
pip install pydantic>=2.0.0
pip install tiktoken>=0.3.0
pip install openai>=1.0.0
pip install lxml>=4.9.0
```

```bash
pip install scrapeneatly
```

## Quick Start

```python
import asyncio
from scrapeneatly import scrape_product

async def main():
    # Define what you want to extract
    fields = {
        "title": {
            "description": "Product title",
            "type": "string"
        },
        "images": {
            "description": "Product images",
            "type": "array",
            "items": {"type": "string"}
        }
    }

    result = await scrape_product(
        url="https://example.com/product",
        fields_to_extract=fields,
        provider="openai",  # or "openrouter"
        api_key="your-api-key",
        model="anthropic/claude-2"  # optional, for OpenRouter
    )

    if result["success"]:
        print(result["data"])

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

### Specifying Field Types

```python
fields = {
    "price": {
        "description": "Product price",
        "type": "string"
    },
    "variants": {
        "description": "Product variants",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "color": {"type": "string"},
                "size": {"type": "string"}
            }
        }
    }
}
```

### Using OpenRouter with Custom Model

```python
result = await scrape_product(
    url="your_url",
    fields_to_extract=fields,
    provider="openrouter",
    api_key="your-openrouter-key",
    model="google/gemini-2.0-flash-001"
)
```

### Using OpenAI models - Uses gpt4o - please don't specify the model

```python
result = await scrape_product(
    url="your_url",
    fields_to_extract=fields,
    provider="openai",
    api_key="your-openai-api-key",
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
