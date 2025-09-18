"""Configuration management for KinderShield."""

import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration settings for KinderShield evaluations."""
    
    # API Keys
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    
    # Model Configuration
    model_provider: str = Field(default_factory=lambda: os.getenv("MODEL_PROVIDER", "dummy"))
    model_name: str = Field(default_factory=lambda: os.getenv("MODEL_NAME", "dummy-small"))
    
    # General Configuration
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    # Report Settings
    report_output_dir: str = Field(default_factory=lambda: os.getenv("REPORT_OUTPUT_DIR", "./reports"))
    generate_html_report: bool = Field(default_factory=lambda: os.getenv("GENERATE_HTML_REPORT", "true").lower() == "true")
    generate_svg_badge: bool = Field(default_factory=lambda: os.getenv("GENERATE_SVG_BADGE", "true").lower() == "true")
    
    # Backward compatibility
    @property
    def default_provider(self) -> str:
        """Backward compatibility property."""
        return self.model_provider
    
    def get_api_key_for_provider(self, provider: str) -> Optional[str]:
        """Get the appropriate API key for a given provider."""
        if provider.lower() == "openai":
            return self.openai_api_key
        elif provider.lower() == "anthropic":
            return self.anthropic_api_key
        else:
            return None  # Dummy provider doesn't need an API key
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()