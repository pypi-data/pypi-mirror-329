"""
Midjourney engine for midjargon.
"""

from midjargon.engines.midjourney.models import ImagePrompt, MidjourneyPrompt
from midjargon.engines.midjourney.parser import MidjourneyParser

# Create a default parser instance
_parser = MidjourneyParser()

# Export the parse_dict function from the default parser
parse_midjourney_dict = _parser.parse_dict

__all__ = [
    "ImagePrompt",
    "MidjourneyParser",
    "MidjourneyPrompt",
    "parse_midjourney_dict",
]
