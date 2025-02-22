"""
MamaSight: A package for analyzing UI elements and text in images.
"""

from .screen_parser import ScreenParser
from .version import __version__

__all__ = ["ScreenParser", "__version__"]