"""Configuration management for KinderShield."""

import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration settings for KinderShield evaluations."""
    
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    default_provider: str = Field(default_factory=lambda: os.getenv("DEFAULT_PROVIDER", "dummy"))
    
    report_output_dir: str = Field(default_factory=lambda: os.getenv("REPORT_OUTPUT_DIR", "./reports"))
    generate_html_report: bool = Field(default_factory=lambda: os.getenv("GENERATE_HTML_REPORT", "true").lower() == "true")
    generate_svg_badge: bool = Field(default_factory=lambda: os.getenv("GENERATE_SVG_BADGE", "true").lower() == "true")
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()