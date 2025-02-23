"""
OwnerRez API Wrapper
~~~~~~~~~~~~~~~~~~~

A Python wrapper for the OwnerRez API.
"""

from .api import API
from .cli import main as cli

__version__ = "0.1.0"
__author__ = "Geody Moore"
__email__ = "geody.moore@gmail.com"

__all__ = ["API", "cli"]
