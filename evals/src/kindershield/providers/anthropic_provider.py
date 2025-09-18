"""Anthropic provider implementation."""

from typing import Optional
from .dummy_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic API provider for KinderShield evaluations."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-haiku-20240307", **kwargs):
        """Initialize the Anthropic provider."""
        self.api_key = api_key
        self.model = model
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using Anthropic API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 150),
                temperature=kwargs.get("temperature", 0.7),
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
        
        except ImportError:
            raise ImportError("anthropic package is required for Anthropic provider")
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")