"""OpenAI provider implementation."""

from typing import Optional
from .dummy_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI API provider for KinderShield evaluations."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo", **kwargs):
        """Initialize the OpenAI provider."""
        self.api_key = api_key
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenAI API."""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 150),
                temperature=kwargs.get("temperature", 0.7),
            )
            
            return response.choices[0].message.content.strip()
        
        except ImportError:
            raise ImportError("openai package is required for OpenAI provider")
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")