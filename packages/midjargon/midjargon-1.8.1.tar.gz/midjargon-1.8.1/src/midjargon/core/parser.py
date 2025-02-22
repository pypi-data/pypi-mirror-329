"""
parser.py

Provides a simple, permissive parser that converts an expanded prompt (a MidjargonPrompt string)
into a flat dictionary (MidjargonDict) with the following keys:
  - "images": list of image URLs (extracted from the beginning of the prompt)
  - "text": the main text of the prompt
  - Additional keys for any parameters found (keys without the '--' prefix)

This parser does not perform strict validation; it only tokenizes and groups values.
"""

from __future__ import annotations

import contextlib
import re
from typing import cast

from midjargon.core.parameters import parse_parameters
from midjargon.core.type_defs import MidjargonDict, MidjargonPrompt


def split_text_and_parameters(text: str) -> tuple[str, str]:
    """
    Split text into main text and parameters at first non-nested --.

    Args:
        text: The text to split.

    Returns:
        Tuple of (main_text, parameter_text).
        If no parameters are found, parameter_text will be empty.
    """
    i = 0
    depth = 0
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        elif (
            text[i : i + 2] == "--" and depth == 0 and (i == 0 or text[i - 1].isspace())
        ):
            return text[:i].strip(), text[i:]
        i += 1
    return text.strip(), ""


def parse_image_urls(tokens: list[str]) -> tuple[list[str], list[str]]:
    """
    Extract image URLs from the start of tokens.

    Args:
        tokens: List of tokens from prompt text.

    Returns:
        Tuple of (image_urls, remaining_tokens).
        Image URLs are extracted from the start of tokens until a non-URL token is found.
    """
    urls = []
    i = 0

    url_pattern = re.compile(
        r"^https?://[^\s/$.?#].[^\s]*\.(jpg|jpeg|png|gif|webp)$", re.IGNORECASE
    )

    # Extract URLs from start of tokens
    while i < len(tokens):
        token = tokens[i]
        if url_pattern.match(token):
            urls.append(token)
            i += 1
        else:
            break

    return urls, tokens[i:]


def parse_midjargon_prompt_to_dict(expanded_prompt: MidjargonPrompt) -> MidjargonDict:
    """
    Parse an expanded prompt into a dictionary format.
    Handles URL extraction and parameter parsing.

    Args:
        expanded_prompt: Expanded prompt string.

    Returns:
        Dictionary containing parsed prompt components.
    """
    # Extract URLs and text
    urls = []
    text_parts = []

    parts = expanded_prompt.split()
    for part in parts:
        if part.startswith(("http://", "https://")):
            urls.append(part)
        else:
            text_parts.append(part)

    # Join remaining parts as text, preserving original spacing
    text_part = " ".join(text_parts)

    # Find where parameters start (if any)
    param_part = ""
    if "--" in text_part:
        text_split = text_part.split("--", 1)
        text_part = text_split[0].strip()
        param_part = "--" + text_split[1]

    # Parse parameters using the consolidated parameter parsing logic
    params = parse_parameters(param_part) if param_part.startswith("--") else {}

    # Convert numeric values
    numeric_params = {
        "stylize": int,
        "chaos": int,
        "weird": int,
        "image_weight": float,
        "seed": int,
        "stop": int,
        "quality": float,
        "repeat": int,
        "character_weight": int,
        "style_weight": int,
        "style_version": int,
    }

    for param, converter in numeric_params.items():
        if param in params and params[param] is not None:
            with contextlib.suppress(ValueError, TypeError):
                params[param] = converter(params[param])

    # Build the dictionary according to the specification
    result = {
        "images": urls,
        "text": text_part,
        **params,  # Merge additional parameters directly into the dict
    }

    return cast(MidjargonDict, result)
