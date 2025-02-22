"""
midjargon.core
~~~~~~~~~~~~~

Core functionality for prompt parsing and manipulation.

This module provides the base classes and utilities for:
- Prompt parsing and validation
- Parameter handling and normalization
- Text manipulation and splitting
- Type definitions for the midjargon package

The core module is engine-agnostic and provides the foundation for
specific engine implementations (like Midjourney).
"""

from midjargon.core.input import expand_midjargon_input
from midjargon.core.parameters import ParamDict, ParamName, ParamValue, parse_parameters
from midjargon.core.parser import parse_midjargon_prompt_to_dict
from midjargon.core.permutations import expand_text
from midjargon.core.type_defs import (
    MidjargonDict,
    MidjargonInput,
    MidjargonList,
    MidjargonPrompt,
)

__all__ = [
    "MidjargonDict",
    # Type definitions
    "MidjargonInput",
    "MidjargonList",
    "MidjargonPrompt",
    "ParamDict",
    "ParamName",
    "ParamValue",
    # Core functions
    "expand_midjargon_input",
    "expand_text",
    "parse_midjargon_prompt_to_dict",
    "parse_parameters",
]
