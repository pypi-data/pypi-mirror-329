"""
OwnerRez API Wrapper
~~~~~~~~~~~~~~~~~~~

A Python wrapper for the OwnerRez API.
"""

from .api import API
from .cli import main as cli

__version__ = "0.2.0"
__author__ = "Geody Moore"
__author_email__ = "geody.moore@gmail.com"
__description__ = "A Python wrapper for the OwnerRez API"

__all__ = ["API", "cli"]
