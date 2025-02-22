"""
Parameter handling for the Midjourney parser.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar

from midjargon.engines.midjourney.constants import (
    CHAOS_RANGE,
    CHARACTER_WEIGHT_RANGE,
    DEFAULT_CHAOS,
    DEFAULT_CHARACTER_WEIGHT,
    DEFAULT_IMAGE_WEIGHT,
    DEFAULT_QUALITY,
    DEFAULT_STOP,
    DEFAULT_STYLE_VERSION,
    DEFAULT_STYLIZE,
    DEFAULT_WEIRD,
    IMAGE_WEIGHT_RANGE,
    QUALITY_RANGE,
    REPEAT_RANGE,
    SEED_RANGE,
    STOP_RANGE,
    STYLE_VERSION_RANGE,
    STYLE_WEIGHT_RANGE,
    STYLIZE_RANGE,
    WEIRD_RANGE,
)
from midjargon.engines.midjourney.parser.exceptions import ParameterValidationError
from midjargon.engines.midjourney.parser.validation import ValidatorRegistry

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")


@dataclass(frozen=True)
class ParameterConfig:
    """Configuration for a parameter."""

    name: str
    handler: Callable[[str], Any]
    validator: Callable[[Any], bool]
    default: Any
    aliases: list[str] = field(default_factory=list)
    range: tuple[float, float] | None = None


def handle_integer(value: str) -> int:
    """Convert string value to integer.

    Args:
        value: String value to convert

    Returns:
        Integer value

    Raises:
        ValueError: If conversion fails
    """
    return int(float(value))


def handle_float(value: str) -> float:
    """Convert string value to float.

    Args:
        value: String value to convert

    Returns:
        Float value

    Raises:
        ValueError: If conversion fails
    """
    return float(value)


class ParameterHandler:
    """Handler for parameter processing."""

    def __init__(self) -> None:
        """Initialize parameter handler."""
        self.validators = ValidatorRegistry()
        self._init_parameter_configs()
        self.flag_params = {
            "turbo",
            "relax",
            "tile",
            "p",
            "personalization",
        }

    def _init_parameter_configs(self) -> None:
        """Initialize parameter configurations."""
        self.configs: dict[str, ParameterConfig] = {
            "stylize": ParameterConfig(
                name="stylize",
                handler=handle_integer,
                validator=lambda v: self.validators.validate(
                    "range", v, *STYLIZE_RANGE
                ),
                default=DEFAULT_STYLIZE,
                aliases=["s"],
                range=STYLIZE_RANGE,
            ),
            "chaos": ParameterConfig(
                name="chaos",
                handler=handle_integer,
                validator=lambda v: self.validators.validate("range", v, *CHAOS_RANGE),
                default=DEFAULT_CHAOS,
                aliases=["c"],
                range=CHAOS_RANGE,
            ),
            "weird": ParameterConfig(
                name="weird",
                handler=handle_integer,
                validator=lambda v: self.validators.validate("range", v, *WEIRD_RANGE),
                default=DEFAULT_WEIRD,
                aliases=["w"],
                range=WEIRD_RANGE,
            ),
            "image_weight": ParameterConfig(
                name="image_weight",
                handler=handle_float,
                validator=lambda v: self.validators.validate(
                    "range", v, *IMAGE_WEIGHT_RANGE
                ),
                default=DEFAULT_IMAGE_WEIGHT,
                aliases=["iw"],
                range=IMAGE_WEIGHT_RANGE,
            ),
            "quality": ParameterConfig(
                name="quality",
                handler=handle_float,
                validator=lambda v: self.validators.validate(
                    "range", v, *QUALITY_RANGE
                ),
                default=DEFAULT_QUALITY,
                aliases=["q"],
                range=QUALITY_RANGE,
            ),
            "character_weight": ParameterConfig(
                name="character_weight",
                handler=handle_float,
                validator=lambda v: self.validators.validate(
                    "range", v, *CHARACTER_WEIGHT_RANGE
                ),
                default=DEFAULT_CHARACTER_WEIGHT,
                aliases=["cw"],
                range=CHARACTER_WEIGHT_RANGE,
            ),
            "style_weight": ParameterConfig(
                name="style_weight",
                handler=handle_float,
                validator=lambda v: self.validators.validate(
                    "range", v, *STYLE_WEIGHT_RANGE
                ),
                default=None,
                aliases=["sw"],
                range=STYLE_WEIGHT_RANGE,
            ),
            "style_version": ParameterConfig(
                name="style_version",
                handler=handle_integer,
                validator=lambda v: self.validators.validate(
                    "range", v, *STYLE_VERSION_RANGE
                ),
                default=DEFAULT_STYLE_VERSION,
                aliases=["sv"],
                range=STYLE_VERSION_RANGE,
            ),
            "repeat": ParameterConfig(
                name="repeat",
                handler=handle_integer,
                validator=lambda v: self.validators.validate("range", v, *REPEAT_RANGE),
                default=None,
                aliases=["r"],
                range=REPEAT_RANGE,
            ),
            "seed": ParameterConfig(
                name="seed",
                handler=handle_integer,
                validator=lambda v: self.validators.validate("range", v, *SEED_RANGE),
                default=None,
                range=SEED_RANGE,
            ),
            "stop": ParameterConfig(
                name="stop",
                handler=handle_integer,
                validator=lambda v: self.validators.validate("range", v, *STOP_RANGE),
                default=DEFAULT_STOP,
                range=STOP_RANGE,
            ),
        }

    def process(self, param_name: str, raw_value: Any) -> Any:
        """Process a parameter value.

        Args:
            param_name: Name of the parameter
            raw_value: Raw value to process

        Returns:
            Processed value

        Raises:
            ParameterValidationError: If validation fails
        """
        # Handle flag parameters
        if param_name in self.flag_params:
            if raw_value is None:
                return True
            return bool(raw_value)

        # Get parameter config
        config = self._get_config(param_name)
        if not config:
            return raw_value

        # Handle None values
        if raw_value is None:
            return None

        try:
            # Convert value
            value = config.handler(str(raw_value))
        except ValueError as e:
            msg = f"Invalid numeric value: {e!s}"
            raise ParameterValidationError(param_name, str(raw_value), msg) from e

        # Validate value
        if not config.validator(value):
            if config.range:
                msg = f"Invalid numeric value for {param_name}: {raw_value} - Value must be between {config.range[0]} and {config.range[1]}"
            else:
                msg = f"Invalid numeric value for {param_name}: {raw_value}"
            raise ParameterValidationError(param_name, str(raw_value), msg)

        return value

    def _get_config(self, param_name: str) -> ParameterConfig | None:
        """Get parameter configuration.

        Args:
            param_name: Name of the parameter

        Returns:
            Parameter configuration or None if not found
        """
        # Check direct name match
        if param_name in self.configs:
            return self.configs[param_name]

        # Check aliases
        for config in self.configs.values():
            if param_name in config.aliases:
                return config

        return None

    def get_default(self, param_name: str) -> Any:
        """Get default value for a parameter.

        Args:
            param_name: Name of the parameter

        Returns:
            Default value for the parameter
        """
        config = self._get_config(param_name)
        return config.default if config else None
