"""
Validation utilities for the Midjourney parser.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, TypeVar

from midjargon.engines.midjourney.constants import (
    VALID_NIJI_VERSIONS,
    VALID_VERSIONS,
)
from midjargon.engines.midjourney.parser.exceptions import ValidationError

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")


def validate_version_pattern(value: str) -> bool:
    """Validate version string pattern.

    Args:
        value: Version string to validate

    Returns:
        True if valid, False otherwise
    """
    if value.lower().startswith("niji"):
        parts = value.split()
        return len(parts) == 1 or (len(parts) > 1 and parts[1] in VALID_NIJI_VERSIONS)
    version = value[1:] if value.startswith("v") else value
    return version in VALID_VERSIONS


def validate_image_reference(value: str) -> bool:
    """Validate image reference URL or path.

    Args:
        value: Image reference to validate

    Returns:
        True if valid, False otherwise
    """
    return any(value.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".gif"))


class ValidatorRegistry:
    """Registry of validation functions."""

    _validators: ClassVar[dict[str, Callable[..., bool]]] = {
        "range": lambda v, mn, mx: mn <= v <= mx,
        "version": validate_version_pattern,
        "image_ref": validate_image_reference,
    }

    @classmethod
    def validate(cls, name: str, value: Any, *args: Any) -> bool:
        """Validate a value using the registered validator.

        Args:
            name: Name of the validator to use
            value: Value to validate
            *args: Additional arguments for the validator

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validator not found
        """
        validator = cls._validators.get(name)
        if not validator:
            msg = f"No validator found for {name}"
            raise ValidationError(msg)
        return validator(value, *args)

    @classmethod
    def register(cls, name: str, validator: Callable[..., bool]) -> None:
        """Register a new validator.

        Args:
            name: Name for the validator
            validator: Validation function
        """
        cls._validators[name] = validator
