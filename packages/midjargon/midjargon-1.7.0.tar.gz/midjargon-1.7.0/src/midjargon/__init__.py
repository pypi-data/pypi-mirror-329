"""
midjargon

A Python library for parsing and manipulating Midjourney prompts.
"""

from importlib import metadata

from midjargon.core import (
    MidjargonDict,
    MidjargonInput,
    MidjargonList,
    MidjargonPrompt,
    expand_midjargon_input,
    parse_midjargon_prompt_to_dict,
)
from midjargon.engines.midjourney import MidjourneyPrompt, parse_midjourney_dict

__version__ = metadata.version(__name__)

__all__ = [
    "MidjargonDict",
    # Core types
    "MidjargonInput",
    "MidjargonList",
    "MidjargonPrompt",
    # Midjourney-specific
    "MidjourneyPrompt",
    # Core functions
    "expand_midjargon_input",
    "parse_midjargon_prompt_to_dict",
    "parse_midjourney_dict",
]
