"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_prompts():
    """Return a dictionary of sample prompts for testing."""
    return {
        "basic": "a serene landscape --ar 16:9 --stylize 100",
        "with_image": "https://example.com/image.jpg mystical forest --chaos 20",
        "permutation": "a {red, blue} bird on a {flower, leaf} --ar 16:9",
        "multi_prompt": "mystical forest ::2 foggy mountains ::1 --chaos 20",
        "with_flags": "landscape photo --tile --no blur,cars",
        "escaped_commas": "a {red\\, blue, green} bird",
        "nested": "a {big {red, blue}, small green} bird",
        "multiple_images": "https://example.com/1.jpg https://example.com/2.jpg forest --iw 2",
    }


@pytest.fixture
def invalid_prompts():
    """Return a dictionary of invalid prompts for testing."""
    return {
        "empty": "",
        "only_params": "--ar 16:9",
        "unclosed_brace": "a {red, blue bird",
        "invalid_weight": "forest ::x mountains",
    }
