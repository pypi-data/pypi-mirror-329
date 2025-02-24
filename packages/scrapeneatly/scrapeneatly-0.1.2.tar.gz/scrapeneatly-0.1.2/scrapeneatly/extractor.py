import json
import logging
from typing import Dict, Any, Type, Optional
from pydantic import BaseModel, Field, create_model
from .models import ExtractConfig
from .exceptions import LLMException
import aiohttp
import tiktoken
from openai import OpenAI
from .exceptions import ValidationError



logger = logging.getLogger(__name__)

class LLMExtractor:
    def __init__(self):
        """Initialize the LLM extractor"""
        self.openai_client = None
        self.api_key = None  # Initialize api_key

    def _initialize_client(self, config: ExtractConfig):
        """Initialize the appropriate client based on provider"""
        if config.provider == "openai":
            if not config.api_key:
                raise ValidationError("OpenAI API key is required")
            self.openai_client = OpenAI(api_key=config.api_key)
            self.api_key = config.api_key  # Set api_key for OpenAI
        elif config.provider == "openrouter":
            if not config.api_key:
                raise ValidationError("OpenRouter API key is required")
            self.api_key = config.api_key  # Set api_key for OpenRouter
            self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def _schema_to_pydantic(self, schema: Dict[str, Any]) -> Type[BaseModel]:
        """Convert JSON schema to Pydantic model"""
        if not schema.get('properties'):
            raise ValidationError("Schema must contain properties")

        properties = schema['properties']
        field_types = {}
        
        type_mapping = {
            'string': str,
            'number': float,
            'integer': int,
            'boolean': bool,
            'array': list,
            'object': dict
        }

        for field_name, field_def in properties.items():
            if 'type' not in field_def:
                raise ValidationError(f"Field {field_name} must have a type")
            if 'description' not in field_def:
                raise ValidationError(f"Field {field_name} must have a description")

            field_type = field_def.get('type')
            if field_type == 'array' and 'items' in field_def:
                item_type = field_def['items'].get('type')
                if item_type in type_mapping:
                    field_types[field_name] = (list[type_mapping[item_type]], ...)
                else:
                    field_types[field_name] = (list, ...)
            else:
                field_types[field_name] = (type_mapping.get(field_type, Any), ...)

        model_name = schema.get('title', 'DynamicModel')
        return create_model(model_name, **field_types)

    async def _truncate_content(self, content: str, model: str) -> str:
        """Intelligently truncate content to fit token limits"""
        try:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            token_count = len(encoding.encode(content))
            
            if token_count > 150000:
                breakpoint = content.rfind('>', 0, len(content) * 150000 // token_count)
                if breakpoint == -1:
                    breakpoint = len(content) * 150000 // token_count
                content = content[:breakpoint] + '</body></html>'
                
                logger.info(f"Content truncated from {token_count} to {len(encoding.encode(content))} tokens")
            
            return content
        except Exception as e:
            logger.warning(f"Error in token counting: {str(e)}")
            return content

    def _prepare_messages(self, content: str, config: ExtractConfig) -> list:
        """Prepare messages for the LLM"""
        messages = [
            {
                "role": "system",
                "content": config.system_prompt + " Please respond with only JSON - nothing else. Response format must be JSON."
            },
            {
                "role": "user",
                "content": content
            }
        ]

        if config.schema_prompt:
            messages.append({
                "role": "user",
                "content": f"Transform the above content into structured JSON output based on the following request: {config.schema_prompt}"
            })

        return messages

    def _prepare_response_format(self, config: ExtractConfig) -> Dict[str, Any]:
        """Prepare response format using schema from config"""
        if not config.schema_data or not config.schema_data.schema_definition:
            raise LLMException("Schema configuration is required but was not provided")
            
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "extract_data",
                "strict": True,
                "schema": config.schema_data.schema_definition,
                "required": ['artist_with_most_awards', 'band_with_most_awards']
            }

        }

    def _convert_json_schema_to_pydantic_fields(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Convert JSON schema properties to Pydantic field definitions"""
        properties = schema.get('properties', {})
        field_types = {}
        
        type_mapping = {
            'string': str,
            'number': float,
            'integer': int,
            'boolean': bool,
            'array': list,
            'object': dict
        }

        for field_name, field_def in properties.items():
            field_type = field_def.get('type')
            description = field_def.get('description', '')
            
            # Handle array types
            if field_type == 'array':
                items_type = field_def.get('items', {}).get('type', 'string')
                py_type = list[type_mapping.get(items_type, str)]
                field_types[field_name] = (py_type, Field(description=description))
            else:
                # Handle primitive types
                py_type = type_mapping.get(field_type, str)
                field_types[field_name] = (py_type, Field(description=description))

        return field_types

    def create_dynamic_model(self, schema: Dict[str, Any]) -> Type[BaseModel]:
        """
        Create a dynamic Pydantic model from a JSON schema.
        
        Args:
            schema (Dict[str, Any]): JSON schema definition
        
        Returns:
            Type[BaseModel]: Dynamically created Pydantic model
        """
        try:
            # Extract model name from schema or generate a default
            model_name = schema.get('title', 'DynamicModel')
            
            # Convert JSON schema to Pydantic field definitions
            fields = self._convert_json_schema_to_pydantic_fields(schema)
            
            # Create and return the dynamic model
            return create_model(
                model_name, 
                __base__=BaseModel,
                **fields
            )
        except Exception as e:
            logger.error(f"Failed to create dynamic model: {str(e)}")
            raise LLMException(f"Model creation failed: {str(e)}")

    async def extract_openai(self, content: str, config: ExtractConfig) -> Dict[str, Any]:
        """Extract structured data using OpenAI's parsing API"""
        try:
            if not self.openai_client:
                raise LLMException("OpenAI client not initialized. Please provide API key.")

            logger.info("Starting OpenAI extraction process...")
            content = await self._truncate_content(content, config.model)
            
            # Convert schema to Pydantic model
            pydantic_model = self.create_dynamic_model(config.schema_data.schema_definition)
            
            completion = self.openai_client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=self._prepare_messages(content, config),
                response_format=pydantic_model
            )

            parsed_data = completion.choices[0].message.parsed
            
            return {
                'extract': parsed_data.model_dump(),
                'usage': {
                    'prompt_tokens': completion.usage.prompt_tokens,
                    'completion_tokens': completion.usage.completion_tokens,
                    'total_tokens': completion.usage.total_tokens
                }
            }

        except Exception as e:
            logger.error(f"OpenAI extraction failed: {str(e)}")
            raise LLMException(f"Extraction failed: {str(e)}")

    async def extract_openrouter(self, content: str, config: ExtractConfig) -> Dict[str, Any]:
        """Extract structured data from HTML content using LLM"""
        try:
            logger.info("Starting extraction process...")
            
            # Truncate content if needed
            content = await self._truncate_content(content, config.model)
            response_format = self._prepare_response_format(config)
            # print()
            payload = {
                "model": config.model,
                "messages": self._prepare_messages(content, config),
                # "temperature": 0,
                "response_format": response_format,
                "provider": {
                    "require_parameters": True
                }
            }

            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise LLMException(f"API call failed with status {response.status}: {error_text}")
                    
                    data = await response.json()
                    # print(data)
            # Process response
            if data["choices"][0]["message"]["content"]:
                content = data["choices"][0]["message"]["content"].strip('`').strip()
                if content.startswith('json'):
                    content = content[4:].strip()

                try:
                    json_content = json.loads(content)
                    
                    # Handle array type schema unwrapping
                    if (config.schema_data and 
                        config.schema_data.schema_definition.get('type') == 'array' and
                        isinstance(json_content, dict) and
                        'items' in json_content):
                        json_content = json_content['items']
                    
                    return {
                        'extract': json_content,
                        'usage': {
                            'prompt_tokens': data["usage"]["prompt_tokens"],
                            'completion_tokens': data["usage"]["completion_tokens"],
                            'total_tokens': data["usage"]["total_tokens"]
                        }
                    }
                except json.JSONDecodeError as e:
                    logger.error(f"JSON Parse Error: {str(e)}")
                    raise LLMException(f"Failed to parse JSON response: {str(e)}")

            raise LLMException("Empty response from LLM")
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {str(e)}")
            raise LLMException(f"Extraction failed: {str(e)}")

    async def extract(self, content: str, config: ExtractConfig) -> Dict[str, Any]:
        """Main extract method that chooses the appropriate implementation"""
        try:
            self._initialize_client(config)
            if config.provider == "openai":
                return await self.extract_openai(content, config)
            else:
                return await self.extract_openrouter(content, config)
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            raise LLMException(f"Extraction failed: {str(e)}")   