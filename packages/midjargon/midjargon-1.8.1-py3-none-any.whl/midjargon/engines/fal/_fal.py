"""
fal.py

Provides functions to convert Midjourney prompts to Fal.ai format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict


def to_fal_dict(midjargon_dict: MidjargonDict) -> dict[str, Any]:
    """
    Convert a MidjargonDict to Fal.ai format.

    Args:
        midjargon_dict: Dictionary to convert.

    Returns:
        Dictionary in Fal.ai format.
    """
    result = {
        "prompt": midjargon_dict.get("text", ""),
        "negative_prompt": midjargon_dict.get("negative_prompt"),
        "width": 1024,  # Default width
        "height": 1024,  # Default height
        "num_inference_steps": 50,  # Default steps
        "guidance_scale": 7.5,  # Default guidance scale
        "seed": midjargon_dict.get("seed"),
    }

    # Handle aspect ratio
    if "aspect_width" in midjargon_dict and "aspect_height" in midjargon_dict:
        width = midjargon_dict["aspect_width"]
        height = midjargon_dict["aspect_height"]
        if isinstance(width, int) and isinstance(height, int):
            # Scale to maintain aspect ratio while keeping max dimension at 1024
            if width > height:
                result["width"] = 1024
                result["height"] = int(1024 * (height / width))
            else:
                result["height"] = 1024
                result["width"] = int(1024 * (width / height))

    # Handle other parameters
    if "chaos" in midjargon_dict:
        chaos = midjargon_dict["chaos"]
        if isinstance(chaos, int | float):
            result["guidance_scale"] = max(1.0, 15.0 - (chaos / 10))

    if "stop" in midjargon_dict:
        stop = midjargon_dict["stop"]
        if isinstance(stop, int | float):
            result["num_inference_steps"] = min(100, max(10, int(stop / 2)))

    return result
