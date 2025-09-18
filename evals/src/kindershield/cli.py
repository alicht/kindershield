#!/usr/bin/env python3
"""CLI module interface for KinderShield using the main CLI commands."""

import sys
from pathlib import Path

# Add the project root to Python path so we can import the main CLI
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import and expose the main CLI functions
from eval_cli import app

if __name__ == "__main__":
    app()