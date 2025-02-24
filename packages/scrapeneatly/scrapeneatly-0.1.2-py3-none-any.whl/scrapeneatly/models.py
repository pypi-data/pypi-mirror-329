from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, validator
from urllib.parse import urlparse
from .exceptions import ValidationError

@dataclass
class MediaConfig:
    block_loading: bool = True
    preserve_urls: bool = True
    extract_srcsets: bool = True
    make_urls_absolute: bool = True

class SchemaConfig(BaseModel):
    type: str
    schema_definition: Dict[str, Any]
    name: Optional[str] = None
    strict: bool = True

    @validator('type')
    def validate_type(cls, v):
        if v not in ['object', 'array']:
            raise ValidationError('Schema type must be either "object" or "array"')
        return v

    @validator('schema_definition')
    def validate_schema_definition(cls, v):
        if not v.get('properties'):
            raise ValidationError('Schema must contain properties')
        for prop_name, prop_def in v['properties'].items():
            if not isinstance(prop_def, dict):
                raise ValidationError(f'Property {prop_name} definition must be a dictionary')
            if 'type' not in prop_def:
                raise ValidationError(f'Property {prop_name} must have a type')
            if 'description' not in prop_def:
                raise ValidationError(f'Property {prop_name} must have a description')
        return v
    
class ExtractConfig(BaseModel):
    system_prompt: str
    schema_prompt: Optional[str] = None
    schema_data: Optional[SchemaConfig] = None
    provider: str = "openai"
    api_key: Optional[str] = None
    model: Optional[str] = None  # Made optional since it's only needed for OpenRouter

    @validator('system_prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValidationError('System prompt cannot be empty')
        return v

    @validator('provider')
    def validate_provider(cls, v):
        if v not in ['openai', 'openrouter']:
            raise ValidationError('Provider must be either "openai" or "openrouter"')
        return v

    @validator('api_key')
    def validate_api_key(cls, v, values):
        if not v:
            raise ValidationError(f'API key must be provided for {values.get("provider", "selected provider")}')
        return v

    @validator('model')
    def validate_model(cls, v, values):
        provider = values.get('provider')
        if provider == 'openrouter':
            if not v:
                # Set default model for OpenRouter
                return "deepseek/deepseek-chat"
            return v
        # For OpenAI, model should be None
        if provider == 'openai' and v is not None:
            return None
        return v  

class ScrapeConfig(BaseModel):
    url: str
    wait_after_load: Optional[int] = 1000
    timeout: Optional[int] = 30000
    custom_headers: Optional[Dict[str, str]] = None
    check_selector: Optional[str] = None
    block_ads: bool = True
    media: Optional[MediaConfig] = Field(default_factory=MediaConfig)
    only_main_content: bool = True
    include_selectors: Optional[List[str]] = None
    exclude_selectors: Optional[List[str]] = None
    extract: Optional[ExtractConfig] = None
    headless: bool = True  # Added headless option with default True


    @validator('url')
    def validate_url(cls, v):
        try:
            result = urlparse(v)
            if all([result.scheme, result.netloc]):
                return v
            raise ValidationError('Invalid URL format')
        except Exception as e:
            raise ValidationError(f'Invalid URL: {str(e)}')