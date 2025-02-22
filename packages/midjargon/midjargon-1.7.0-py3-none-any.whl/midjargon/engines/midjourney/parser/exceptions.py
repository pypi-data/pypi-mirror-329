"""
Custom exceptions for the Midjourney parser.
"""


class ParserError(Exception):
    """Base parser exception."""


class ValidationError(ParserError):
    """Validation-related errors."""


class ParameterValidationError(ValidationError):
    """Specific parameter validation failure."""

    def __init__(self, param_name: str, value: str, reason: str) -> None:
        """Initialize parameter validation error.

        Args:
            param_name: Name of the parameter that failed validation
            value: Invalid value
            reason: Reason for validation failure
        """
        self.param_name = param_name
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid value for {param_name}: {value} - {reason}")
