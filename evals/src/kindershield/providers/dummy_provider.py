"""Dummy provider for testing and development."""

from typing import List, Dict, Any
from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Base class for AI providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the AI provider."""
        pass


class DummyProvider(BaseProvider):
    """Dummy provider that returns predefined responses for testing."""
    
    def __init__(self, **kwargs):
        """Initialize the dummy provider."""
        self.responses = {
            "safe": "This is a safe response appropriate for children.",
            "unsafe": "This response contains inappropriate content.",
            "math": "2 + 2 = 4",
            "reading": "The cat sat on the mat.",
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a dummy response based on prompt keywords."""
        prompt_lower = prompt.lower()
        
        if "math" in prompt_lower:
            return self.responses["math"]
        elif "read" in prompt_lower:
            return self.responses["reading"]
        elif "unsafe" in prompt_lower or "inappropriate" in prompt_lower:
            return self.responses["unsafe"]
        else:
            return self.responses["safe"]