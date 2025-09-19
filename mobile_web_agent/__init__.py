"""
Mobile Web Agent - Autonomous coding agent for mobile-first web applications.

A modular, extensible coding agent with sub-agent delegation capabilities.
"""

from .core.agent import MobileWebAgent
from .main import main

__version__ = "1.0.0"
__all__ = ["MobileWebAgent", "main"]