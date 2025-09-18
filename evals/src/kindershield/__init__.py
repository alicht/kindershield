"""KinderShield: AI safety evaluation framework for child-appropriate content."""

__version__ = "0.1.0"
__author__ = "KinderShield Team"
__email__ = "info@kindershield.org"

from .config import Config
from .runner import Runner

__all__ = ["Config", "Runner"]