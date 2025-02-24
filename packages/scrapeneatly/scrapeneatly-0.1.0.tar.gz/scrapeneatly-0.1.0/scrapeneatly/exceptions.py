from typing import List, Dict, Any, Optional
class ScraperException(Exception):
    """Base exception for scraper related errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class LLMException(Exception):
    """Base exception for LLM related errors"""
    def __init__(self, message: str, response: Optional[Any] = None):
        super().__init__(message)
        self.response = response

class ValidationError(Exception):
    """Exception for validation errors"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field

class LLMRefusalError(LLMException):
    """Exception for when LLM refuses to process content"""
    def __init__(self, refusal: str):
        super().__init__("LLM refused to extract the website's content")
        self.refusal = refusal