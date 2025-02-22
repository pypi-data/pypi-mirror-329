"""
Core parser implementation for Midjourney engine.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from midjargon.engines.base import EngineParser
from midjargon.engines.midjourney.models import ImagePrompt, MidjourneyPrompt
from midjargon.engines.midjourney.parser.exceptions import ParameterValidationError
from midjargon.engines.midjourney.parser.parameters import ParameterHandler

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict


class MidjourneyParser(EngineParser[MidjourneyPrompt]):
    """Parser for Midjourney prompts."""

    def __init__(self) -> None:
        """Initialize parser."""
        self.param_handler = ParameterHandler()

    def _init_prompt_data(self) -> dict[str, Any]:
        """Initialize prompt data with default values."""
        return {
            "text": "",
            "image_prompts": [],
            "stylize": 100,
            "chaos": 0,
            "weird": 0,
            "image_weight": 1.0,
            "seed": None,
            "stop": 100,
            "aspect_width": 1,
            "aspect_height": 1,
            "aspect_ratio": "1:1",
            "style": None,
            "version": None,
            "personalization": False,
            "quality": 1.0,
            "character_reference": [],
            "character_weight": 100,
            "style_reference": [],
            "style_weight": None,
            "style_version": 2,
            "repeat": None,
            "turbo": False,
            "relax": False,
            "tile": False,
            "negative_prompt": None,
            "extra_params": {},
        }

    def _process_text_and_images(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process text and image components of the prompt."""
        # Process text
        text = midjargon_dict.get("text", "")
        if text is None:
            text = ""
        if isinstance(text, list):
            text = text[0] if text else ""
        if not isinstance(text, str):
            text = str(text)
        text = text.strip()
        if not text:
            msg = "Empty prompt"
            raise ValueError(msg)
        prompt_data["text"] = text

        # Process images
        images = midjargon_dict.get("images", [])
        if not isinstance(images, list):
            images = [str(images)] if images else []
        prompt_data["image_prompts"] = [ImagePrompt(url=str(url)) for url in images]

    def _process_aspect_ratio(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process aspect ratio parameters."""
        # Check both 'ar' and 'aspect' parameters
        value = midjargon_dict.get("ar") or midjargon_dict.get("aspect")
        if value is None:
            return

        if isinstance(value, list):
            value = value[0] if value else None
            if value is None:
                return

        # Handle value with additional parameters
        value_str = str(value)
        value_parts = value_str.split("--")
        aspect_value = value_parts[0].strip()

        try:
            width_str, height_str = aspect_value.split(":")
            width = int(width_str.strip())
            height = int(height_str.strip())
        except (ValueError, AttributeError) as e:
            msg = f"Invalid aspect ratio format: {aspect_value} - must be width:height"
            raise ValueError(msg) from e

        if width <= 0 or height <= 0:
            msg = f"Invalid aspect ratio: {aspect_value} - values must be positive"
            raise ValueError(msg)

        # Store both formats
        prompt_data["aspect_width"] = width
        prompt_data["aspect_height"] = height
        prompt_data["aspect_ratio"] = f"{width}:{height}"

        # Store decomposed values in extra_params for reference
        if "extra_params" not in prompt_data:
            prompt_data["extra_params"] = {}
        prompt_data["extra_params"]["aspect_width"] = str(width)
        prompt_data["extra_params"]["aspect_height"] = str(height)

    def _process_version(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process version parameter."""
        for name in ("niji", "version", "v"):
            if name not in midjargon_dict:
                continue

            value = midjargon_dict[name]
            if value is None:
                if name == "niji":
                    prompt_data["version"] = "niji"
                    return
                continue

            # If the key is 'niji', process accordingly
            if name == "niji":
                if isinstance(value, list):
                    value = value[0]
                stripped_value = value.strip()
                if stripped_value == "niji":
                    prompt_data["version"] = "niji"
                else:
                    prompt_data["version"] = f"niji {stripped_value}"
                return

            # For other keys, process as usual
            processed_value = self.param_handler.process(name, value)
            if processed_value is not None:
                # If the processed value starts with 'niji', assign directly, else add 'v' prefix
                if isinstance(
                    processed_value, str
                ) and processed_value.lstrip().lower().startswith("niji"):
                    prompt_data["version"] = processed_value.strip()
                else:
                    prompt_data["version"] = f"v{processed_value}"
                return

    def _process_style(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process style parameter."""
        if "style" in midjargon_dict:
            value = midjargon_dict["style"]
            if value is not None:
                if isinstance(value, list):
                    value = value[0] if value else None
                if value is not None:
                    prompt_data["style"] = str(value)

    def _process_personalization(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Handle personalization parameter."""
        # Check for both 'p' and 'personalization' keys
        p_value = midjargon_dict.get("p")
        personalization = midjargon_dict.get("personalization")

        # If both are present, personalization takes precedence
        value = personalization if personalization is not None else p_value

        # If no personalization parameter is present, set to False
        if (
            value is None
            and "p" not in midjargon_dict
            and "personalization" not in midjargon_dict
        ):
            prompt_data["personalization"] = False
            return

        # Handle flag-only case (when key exists but value is None or empty string)
        if value is None or value == "":
            prompt_data["personalization"] = True
            return

        # Handle empty list case
        if isinstance(value, list) and not value:
            prompt_data["personalization"] = False
            return

        # Handle list values
        if isinstance(value, list):
            # If list has one empty string, treat as flag
            if len(value) == 1 and value[0] == "":
                prompt_data["personalization"] = True
                return
            # Otherwise, keep each code as a separate item
            prompt_data["personalization"] = [str(v) for v in value]
            return

        # Handle string value
        if value == "":
            prompt_data["personalization"] = True
        else:
            prompt_data["personalization"] = [str(value)]

    def _process_references(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process reference parameters."""
        ref_map = {
            "character_reference": ["character_reference", "cref"],
            "style_reference": ["style_reference", "sref"],
        }

        for target, sources in ref_map.items():
            for source in sources:
                if source in midjargon_dict:
                    value = midjargon_dict[source]
                    if value:
                        prompt_data[target] = (
                            value if isinstance(value, list) else [value]
                        )
                    break

    def _process_numeric_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process numeric parameters."""
        numeric_params = {
            "stylize": ["s", "stylize"],
            "chaos": ["c", "chaos"],
            "weird": ["w", "weird"],
            "image_weight": ["iw", "image_weight"],
            "seed": ["seed"],
            "stop": ["stop"],
            "quality": ["q", "quality"],
            "character_weight": ["cw", "character_weight"],
            "style_weight": ["sw", "style_weight"],
            "style_version": ["sv", "style_version"],
            "repeat": ["r", "repeat"],
        }

        for target, sources in numeric_params.items():
            for source in sources:
                if source in midjargon_dict:
                    value = midjargon_dict[source]
                    try:
                        processed = self.param_handler.process(source, value)
                        if value is None:  # Explicitly set None values
                            prompt_data[target] = None
                        elif processed is not None:
                            prompt_data[target] = processed
                        break
                    except ParameterValidationError as e:
                        raise ValueError(str(e)) from e

    def _process_flag_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process flag parameters."""
        flag_params = {
            "turbo": ["turbo"],
            "relax": ["relax"],
            "tile": ["tile"],
        }

        for target, sources in flag_params.items():
            for source in sources:
                if source in midjargon_dict:
                    value = midjargon_dict[source]
                    try:
                        processed = self.param_handler.process(source, value)
                        if processed is not None:
                            prompt_data[target] = processed
                            break
                        if value is None:  # Handle flag parameters without values
                            prompt_data[target] = True
                            break
                    except ParameterValidationError as e:
                        raise ValueError(str(e)) from e

    def _process_negative_prompt(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process negative prompt parameter."""
        if "no" in midjargon_dict:
            value = midjargon_dict["no"]
            if isinstance(value, str):
                prompt_data["negative_prompt"] = value
            elif isinstance(value, list):
                prompt_data["negative_prompt"] = ", ".join(str(v) for v in value)

    def _process_extra_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process any extra parameters."""
        known_params = {
            "text",
            "images",
            "ar",
            "aspect",
            "version",
            "v",
            "niji",
            "style",
            "p",
            "personalization",
            "character_reference",
            "cref",
            "style_reference",
            "sref",
            "s",
            "stylize",
            "c",
            "chaos",
            "w",
            "weird",
            "iw",
            "image_weight",
            "seed",
            "stop",
            "q",
            "quality",
            "cw",
            "character_weight",
            "sw",
            "style_weight",
            "sv",
            "style_version",
            "r",
            "repeat",
            "turbo",
            "relax",
            "tile",
            "no",
        }

        extra_params = {}
        for key, value in midjargon_dict.items():
            if key not in known_params:
                if value is None:
                    extra_params[key] = None
                elif isinstance(value, list):
                    extra_params[key] = value
                else:
                    extra_params[key] = str(value)
        prompt_data["extra_params"] = extra_params

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt.

        Args:
            midjargon_dict: Dictionary to parse

        Returns:
            MidjourneyPrompt object

        Raises:
            ValueError: If parsing fails
        """
        prompt_data = self._init_prompt_data()

        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)

        # Process all other parameters
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_version(prompt_data, midjargon_dict)
        self._process_style(prompt_data, midjargon_dict)
        self._process_personalization(prompt_data, midjargon_dict)
        self._process_references(prompt_data, midjargon_dict)
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_negative_prompt(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)

        return MidjourneyPrompt(**prompt_data)

    def _format_numeric_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format numeric parameters for dictionary output.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary of formatted numeric parameters.
        """
        numeric_params = {
            "stylize": "s",
            "chaos": "c",
            "weird": "w",
            "image_weight": "iw",
            "seed": "seed",
            "stop": "stop",
            "quality": "q",
            "character_weight": "cw",
            "style_weight": "sw",
            "style_version": "sv",
            "repeat": "r",
        }

        result = {}
        for attr, param_name in numeric_params.items():
            value = getattr(prompt, attr)
            if value is not None:
                result[param_name] = str(value)
        return result

    def _format_version(self, version: str | None) -> dict[str, str]:
        """Format version parameter for dictionary output.

        Args:
            version: Version string.

        Returns:
            Dictionary with formatted version parameter.
        """
        if not version:
            return {}

        if version.lower().startswith("niji"):
            parts = version.split()
            return {"niji": parts[1] if len(parts) > 1 else ""}

        version_value = version[1:] if version.startswith("v") else version
        return {"v": version_value}

    def _format_flags(self, prompt: MidjourneyPrompt) -> dict[str, None]:
        """Format flag parameters for dictionary output.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary of flag parameters.
        """
        result = {}
        for flag in ("turbo", "relax", "tile"):
            if getattr(prompt, flag):
                result[flag] = None
        return result

    def _format_references(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format reference parameters for dictionary output.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary of reference parameters.
        """
        result = {}
        if prompt.character_reference:
            result["cref"] = prompt.character_reference
        if prompt.style_reference:
            result["sref"] = prompt.style_reference
        return result

    def _format_aspect_ratio(self, width: int, height: int) -> dict[str, str]:
        """Format aspect ratio parameter."""
        if width == 1 and height == 1:
            return {}
        return {
            "--ar": f"{width}:{height}",
            "--aspect_width": str(width),
            "--aspect_height": str(height),
        }

    def to_dict(self, prompt: MidjourneyPrompt) -> dict[str, Any]:
        """Convert prompt to dictionary format."""
        result = {
            "text": prompt.text,
            "image_prompts": [ip.url for ip in prompt.image_prompts],
            "stylize": prompt.stylize,
            "chaos": prompt.chaos,
            "weird": prompt.weird,
            "image_weight": prompt.image_weight,
            "seed": prompt.seed,
            "stop": prompt.stop,
            "aspect_width": prompt.aspect_width,
            "aspect_height": prompt.aspect_height,
            "aspect_ratio": f"{prompt.aspect_width}:{prompt.aspect_height}",
            "style": prompt.style,
            "version": prompt.version,
            "personalization": prompt.personalization,
            "quality": prompt.quality,
            "character_reference": prompt.character_reference,
            "character_weight": prompt.character_weight,
            "style_reference": prompt.style_reference,
            "style_weight": prompt.style_weight,
            "style_version": prompt.style_version,
            "repeat": prompt.repeat,
            "turbo": prompt.turbo,
            "relax": prompt.relax,
            "tile": prompt.tile,
            "negative_prompt": prompt.negative_prompt,
            "extra_params": {
                "aspect_width": str(prompt.aspect_width),
                "aspect_height": str(prompt.aspect_height),
                **prompt.extra_params,
            },
        }

        # Remove None values
        return {k: v for k, v in result.items() if v is not None}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt object.

        This is the implementation of the abstract method from EngineParser.

        Args:
            midjargon_dict: Dictionary to parse.

        Returns:
            MidjourneyPrompt object.

        Raises:
            ValueError: If data is invalid.
        """
        return self.parse_dict(midjargon_dict)
