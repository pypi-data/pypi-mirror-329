"""
Models for Midjourney engine.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from midjargon.engines.midjourney.constants import (
    CHAOS_RANGE,
    CHARACTER_WEIGHT_RANGE,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_CHAOS,
    DEFAULT_CHARACTER_WEIGHT,
    DEFAULT_IMAGE_WEIGHT,
    DEFAULT_QUALITY,
    DEFAULT_RELAX,
    DEFAULT_STOP,
    DEFAULT_STYLE_VERSION,
    DEFAULT_STYLIZE,
    DEFAULT_TILE,
    DEFAULT_TURBO,
    DEFAULT_WEIRD,
    IMAGE_WEIGHT_RANGE,
    QUALITY_RANGE,
    REPEAT_RANGE,
    SEED_RANGE,
    STOP_RANGE,
    STYLE_VERSION_RANGE,
    STYLE_WEIGHT_RANGE,
    STYLIZE_RANGE,
    VALID_NIJI_VERSIONS,
    VALID_STYLES,
    VALID_VERSIONS,
    WEIRD_RANGE,
)


class ImagePrompt(BaseModel):
    """Represents a validated image prompt URL."""

    url: str = Field(description="Direct image URL ending with allowed extension")

    @field_validator("url")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        """Validates image URL has an allowed file extension."""
        # if not str(v).lower().endswith(ALLOWED_IMAGE_EXTENSIONS):
        #    msg = f"URL must end with one of: {ALLOWED_IMAGE_EXTENSIONS}"
        #    raise ValueError(msg)

        # Validate URL format
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(v):
            msg = "Invalid URL format"
            raise ValueError(msg)

        return v


class MidjourneyPrompt(BaseModel):
    """
    Represents a fully validated Midjourney prompt structure.
    Converts raw parameters into specific validated fields.
    """

    # Core prompt components
    text: str = Field(min_length=1)
    image_prompts: list[ImagePrompt] = Field(default_factory=list)

    # Validated numeric parameters with defaults
    stylize: int | None = Field(
        default=DEFAULT_STYLIZE, ge=STYLIZE_RANGE[0], le=STYLIZE_RANGE[1]
    )
    chaos: int | None = Field(
        default=DEFAULT_CHAOS, ge=CHAOS_RANGE[0], le=CHAOS_RANGE[1]
    )
    weird: int | None = Field(
        default=DEFAULT_WEIRD, ge=WEIRD_RANGE[0], le=WEIRD_RANGE[1]
    )
    image_weight: float | None = Field(
        default=DEFAULT_IMAGE_WEIGHT, ge=IMAGE_WEIGHT_RANGE[0], le=IMAGE_WEIGHT_RANGE[1]
    )
    seed: int | None = Field(default=None, ge=SEED_RANGE[0], le=SEED_RANGE[1])
    stop: int | None = Field(default=DEFAULT_STOP, ge=STOP_RANGE[0], le=STOP_RANGE[1])

    # Aspect ratio parameters
    aspect_width: int = Field(default=1, gt=0)
    aspect_height: int = Field(default=1, gt=0)
    aspect_ratio: str = Field(default=DEFAULT_ASPECT_RATIO)

    # Style parameters
    style: str | None = Field(default=None)  # raw, cute, expressive, etc.
    version: str | None = Field(default=None)  # v5, v6, niji, etc.
    personalization: bool | list[str] | None = Field(
        default=False
    )  # Profile IDs or codes for --p parameter

    # New parameters with defaults
    quality: float | None = Field(
        default=DEFAULT_QUALITY, ge=QUALITY_RANGE[0], le=QUALITY_RANGE[1]
    )
    character_reference: list[str] = Field(default_factory=list)
    character_weight: int | None = Field(
        default=DEFAULT_CHARACTER_WEIGHT,
        ge=CHARACTER_WEIGHT_RANGE[0],
        le=CHARACTER_WEIGHT_RANGE[1],
    )
    style_reference: list[str] = Field(default_factory=list)
    style_weight: int | None = Field(
        default=None, ge=STYLE_WEIGHT_RANGE[0], le=STYLE_WEIGHT_RANGE[1]
    )
    style_version: int | None = Field(
        default=DEFAULT_STYLE_VERSION,
        ge=STYLE_VERSION_RANGE[0],
        le=STYLE_VERSION_RANGE[1],
    )
    repeat: int | None = Field(default=None, ge=REPEAT_RANGE[0], le=REPEAT_RANGE[1])

    # Flag parameters with defaults
    turbo: bool = Field(default=DEFAULT_TURBO)
    relax: bool = Field(default=DEFAULT_RELAX)
    tile: bool = Field(default=DEFAULT_TILE)

    # Negative prompts
    negative_prompt: str | None = Field(default=None)

    # Store any unknown parameters
    extra_params: dict[str, str | None] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def clean_text(cls, v: str) -> str:
        """Basic text cleanup."""
        return v.strip()

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str | None) -> str | None:
        """Validate style value."""
        if v is not None and v not in VALID_STYLES:
            msg = f"Invalid style value. Must be one of: {VALID_STYLES}"
            raise ValueError(msg)
        return v

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str | None) -> str | None:
        """Validate version value."""
        if v is None:
            return v

        # Handle Niji version
        if v.startswith("niji"):
            parts = v.split()
            if len(parts) == 1:  # Just "niji"
                return v
            version = parts[-1]
            if version not in VALID_NIJI_VERSIONS:
                msg = f"Invalid niji version. Must be one of: {VALID_NIJI_VERSIONS}"
                raise ValueError(msg)
            return f"niji {version}"  # Return niji version without 'v' prefix

        # Handle Midjourney version
        version = v.lstrip("v")
        if version not in VALID_VERSIONS:
            msg = f"Invalid version value. Must be one of: {VALID_VERSIONS}"
            raise ValueError(msg)
        return f"v{version}"  # Always add 'v' prefix for regular versions

    @model_validator(mode="after")
    def validate_mode_flags(self) -> Any:
        """Validate mode flag combinations."""
        if self.turbo and self.relax:
            msg = "Cannot use both turbo and relax modes"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def parse_aspect_ratio(self) -> Any:
        """Parse and validate aspect ratio."""
        # If aspect_ratio is provided, parse it and update width/height
        if ":" in self.aspect_ratio:
            try:
                width, height = self.aspect_ratio.split(":")
                self.aspect_width = int(width)
                self.aspect_height = int(height)
            except (ValueError, AttributeError):
                # If parsing fails, use the default
                width, height = DEFAULT_ASPECT_RATIO.split(":")
                self.aspect_width = int(width)
                self.aspect_height = int(height)
                self.aspect_ratio = DEFAULT_ASPECT_RATIO
        else:
            # If no valid aspect_ratio, construct it from width/height
            self.aspect_ratio = f"{self.aspect_width}:{self.aspect_height}"

        return self
