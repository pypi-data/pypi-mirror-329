"""
Functions for converting MidjargonDict to Fal.ai API format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias, cast

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict

# Type alias for Fal.ai API dict format
FalDict: TypeAlias = dict[str, Any]


def _convert_aspect_ratio(d: dict | FalDict | MidjargonDict) -> dict:
    """Convert aspect ratio parameter to Fal.ai format."""
    result = d.copy()
    if "aspect" in result:
        result["aspect_ratio"] = result.pop("aspect")
    return result


def _convert_image_prompts(d: dict | FalDict | MidjargonDict) -> dict:
    """Convert image prompts to Fal.ai format."""
    result = d.copy()
    if "images" in result and isinstance(result["images"], list) and result["images"]:
        result["image_url"] = result["images"][0]
        if len(result["images"]) > 1:
            result["_"] = cast(Any, {"images": result["images"][1:]})
        del result["images"]
    return result


def _convert_text_prompt(d: dict | FalDict | MidjargonDict) -> dict:
    """Convert text prompt to Fal.ai format."""
    result = d.copy()
    if "text" in result:
        result["prompt"] = result.pop("text")
    return result


def _convert_numeric_values(d: dict | FalDict | MidjargonDict) -> dict:
    """Convert numeric values to appropriate types."""
    result: dict[str, Any] = d.copy()
    for key, value in result.items():
        if isinstance(value, str):
            if value.isdigit():
                result[key] = int(value)
            elif value.replace(".", "").isdigit():
                result[key] = float(value)
    return result


def to_fal_dict(d: dict | FalDict | MidjargonDict) -> FalDict:
    """
    Convert a MidjargonDict to Fal.ai API format.

    Args:
        d: Dictionary to convert.

    Returns:
        Dictionary in Fal.ai API format.
    """
    result = d.copy()
    for conversion_step in (
        _convert_numeric_values,
        _convert_aspect_ratio,
        _convert_image_prompts,
        _convert_text_prompt,
    ):
        result = conversion_step(result)
    return result
