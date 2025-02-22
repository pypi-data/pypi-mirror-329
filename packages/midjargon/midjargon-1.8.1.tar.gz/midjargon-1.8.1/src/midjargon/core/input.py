"""
input.py

Contains functions for handling raw input.
Specifically, it expands all permutation expressions in a prompt without doing any parameter parsing/validation.
"""

from midjargon.core.permutations import (
    expand_text,
)

# reuse the existing expansion logic
from midjargon.core.type_defs import MidjargonInput, MidjargonList


def expand_midjargon_input(prompt: MidjargonInput) -> MidjargonList:
    """
    Expands a raw midjargon prompt string into a list of fully expanded prompt strings.

    Args:
        prompt: A raw MidjargonInput string that may contain permutation syntax (e.g. {red, blue}).

    Returns:
        A list of MidjargonPrompt strings with all permutation expressions resolved.
        Returns [""] for empty input.

    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    if not prompt.strip():
        return [""]

    # Handle escaped characters by temporarily replacing them
    # Use unique markers that won't appear in normal text
    replacements = {
        r"\{": "‹ESCAPED_OPEN›",
        r"\}": "‹ESCAPED_CLOSE›",
        r"\,": "‹ESCAPED_COMMA›",
    }
    processed = prompt
    for escaped, marker in replacements.items():
        processed = processed.replace(escaped, marker)

    # If the processed text, after stripping leading whitespace, starts with the escaped open marker,
    # remove any preceding characters so that the output starts with the literal brace.
    stripped = processed.lstrip()
    if stripped.startswith("‹ESCAPED_OPEN›"):
        index = processed.find("‹ESCAPED_OPEN›")
        processed = processed[index:]

    # Expand permutations
    expanded = expand_text(processed)

    # Restore escaped characters
    restored = []
    for input_text in expanded:
        modified_text = input_text
        for marker, original in {
            "‹ESCAPED_OPEN›": "{",
            "‹ESCAPED_CLOSE›": "}",
            "‹ESCAPED_COMMA›": ",",
        }.items():
            modified_text = modified_text.replace(marker, original)
        restored.append(modified_text)

    return restored
