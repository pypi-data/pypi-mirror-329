"""
midjargon.engines.base
~~~~~~~~~~~~~~~~~~~

Base engine interface for midjargon.

This module provides the abstract base class that all engine parsers must implement.
Engine parsers are responsible for converting between the generic MidjargonDict format
and engine-specific prompt types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict

# Type variable for engine-specific prompt type, must be a Pydantic model
T = TypeVar("T", bound=BaseModel)


class EngineParser(ABC, Generic[T]):
    """
    Base class for engine-specific parsers.

    Each engine parser is responsible for:
    1. Converting MidjargonDict to engine-specific prompt types
    2. Validating parameters according to engine rules
    3. Converting engine-specific prompts back to dictionaries

    Type Parameters:
        T: The engine-specific prompt type (must be a Pydantic model)
    """

    @abstractmethod
    def parse_dict(self, midjargon_dict: MidjargonDict) -> T:
        """
        Parse a MidjargonDict into a validated BasePrompt.

        Args:
            midjargon_dict: Dictionary from basic parser or a raw prompt string.

        Returns:
            Validated BasePrompt.

        Raises:
            ValueError: If the prompt text is empty or if validation fails.
        """
        if not isinstance(midjargon_dict, dict):
            midjargon_dict = {"text": str(midjargon_dict)}

        if not midjargon_dict:
            msg = "Empty prompt"
            raise ValueError(msg)

        text_value = midjargon_dict.get("text")
        if text_value is None:
            msg = "Empty prompt"
            raise ValueError(msg)

        text = (
            (text_value[0] if text_value else "")
            if isinstance(text_value, list)
            else str(text_value)
        )

        if not text.strip():
            msg = "Empty prompt"
            raise ValueError(msg)

        return self._parse_dict(midjargon_dict)

    @abstractmethod
    def _parse_dict(self, midjargon_dict: MidjargonDict) -> T:
        """
        Internal method to parse dictionary into model.
        Should be implemented by subclasses.
        """
        msg = "Not implemented"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_dict(self, prompt: T) -> dict[str, Any]:
        """
        Convert a prompt model back to a dictionary.
        Should be implemented by subclasses.
        """
        msg = "Not implemented"
        raise NotImplementedError(msg)

    def validate(self, prompt: T) -> bool:
        """
        Validate an engine-specific prompt.

        By default, this uses Pydantic validation. Override this method
        to implement additional engine-specific validation rules.

        Args:
            prompt: Engine-specific prompt to validate.

        Returns:
            True if the prompt is valid, False otherwise.

        Raises:
            ValueError: If validation fails with specific error messages.
        """
        # Basic Pydantic validation
        prompt.model_validate(prompt.model_dump())
        return True
