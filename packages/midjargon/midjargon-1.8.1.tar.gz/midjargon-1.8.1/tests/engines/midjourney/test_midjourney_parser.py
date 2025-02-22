"""Tests for Midjourney parser."""

from typing import TYPE_CHECKING

import pytest

from midjargon.engines.midjourney import MidjourneyParser

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict

# Test constants
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
WEIRD_VALUE = 1000
SEED_VALUE = 12345
STOP_VALUE = 80
IMAGE_WEIGHT_VALUE = 2.0
VERSION_NUMBER = "5.2"
DEFAULT_STYLIZE = 100
QUALITY_VALUE = 1.5
CHARACTER_WEIGHT_VALUE = 50
STYLE_WEIGHT_VALUE = 500
STYLE_VERSION_VALUE = 3
REPEAT_VALUE = 5


def test_numeric_parameters():
    """Test parsing of numeric parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "stylize": str(STYLIZE_VALUE),
            "seed": str(SEED_VALUE),
            "chaos": str(CHAOS_VALUE),
        }
    )

    assert prompt.text == "a photo"
    assert prompt.stylize == STYLIZE_VALUE
    assert prompt.seed == SEED_VALUE
    assert prompt.chaos == CHAOS_VALUE


def test_style_parameters():
    """Test parsing of style parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict({"text": "a photo", "style": "raw", "v": VERSION_NUMBER})

    assert prompt.text == "a photo"
    assert prompt.style == "raw"
    assert prompt.version == f"v{VERSION_NUMBER}"


def test_aspect_ratio():
    """Test parsing of aspect ratio."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict({"text": "a photo", "aspect": "16:9"})

    assert prompt.text == "a photo"
    assert prompt.aspect_width == 16
    assert prompt.aspect_height == 9


def test_image_prompts():
    """Test parsing of image prompts."""
    parser = MidjourneyParser()
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    prompt = parser.parse_dict({"text": "a fusion", "images": urls})

    assert prompt.text == "a fusion"
    assert len(prompt.image_prompts) == 2
    assert [p.url for p in prompt.image_prompts] == urls


def test_extra_parameters():
    """Test handling of unknown parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "unknown": "value",
            "flag": None,
        }
    )

    assert prompt.text == "a photo"
    assert prompt.extra_params == {"unknown": "value", "flag": None}


def test_parameter_conversion():
    """Test parameter value conversion."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "stylize": str(STYLIZE_VALUE),
            "seed": str(SEED_VALUE),
            "iw": str(IMAGE_WEIGHT_VALUE),
        }
    )

    assert prompt.text == "a photo"
    assert prompt.stylize == STYLIZE_VALUE
    assert prompt.seed == SEED_VALUE
    assert prompt.image_weight == IMAGE_WEIGHT_VALUE


def test_invalid_values():
    """Test handling of invalid parameter values."""
    parser = MidjourneyParser()

    # Invalid aspect ratio - now accepts any value
    result = parser.parse_dict({"text": "a photo", "aspect": "999:999"})
    assert result.aspect_width == 999
    assert result.aspect_height == 999

    # Invalid numeric value - raises ValueError
    with pytest.raises(ValueError, match=r"Invalid numeric value for stylize: 1001"):
        parser.parse_dict({"text": "a photo", "stylize": "1001"})

    # Invalid image URL - treated as extra parameter
    result = parser.parse_dict({"text": "a photo", "image": "not_a_url"})
    assert len(result.image_prompts) == 0
    assert result.extra_params.get("image") == "not_a_url"


def test_parameter_ranges():
    """Test parameter value range validation."""
    parser = MidjourneyParser()

    # Test maximum values
    with pytest.raises(ValueError, match=r"Invalid numeric value for stylize: 2000"):
        parser.parse_dict({"text": "a photo", "stylize": "2000"})

    # Test minimum values
    with pytest.raises(ValueError, match=r"Invalid numeric value for chaos: -1"):
        parser.parse_dict({"text": "a photo", "chaos": "-1"})


def test_empty_values():
    """Test handling of empty values."""
    parser = MidjourneyParser()

    # Empty text
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": ""})

    # Empty image list
    prompt = parser.parse_dict({"text": "a photo", "images": []})
    assert prompt.text == "a photo"
    assert not prompt.image_prompts

    # None values
    prompt = parser.parse_dict({"text": "a photo", "stylize": None})
    assert prompt.text == "a photo"
    assert prompt.stylize is None


def test_niji_parameter():
    """Test parsing of niji parameter."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "niji": "6",
        }
    )

    assert prompt.text == "a photo"
    assert prompt.version == "niji 6"


def test_multiple_permutations():
    """Test handling of multiple permutations."""
    parser = MidjourneyParser()

    # Test with parameter permutations
    input_dicts = [
        {"text": "smooth edges", "stylize": "75"},
        {"text": "smooth edges", "stylize": "300"},
        {"text": "smooth edges", "stylize": "75", "personalization": None},
        {"text": "smooth edges", "stylize": "300", "personalization": None},
    ]

    results = [parser.parse_dict(d) for d in input_dicts]
    assert len(results) == 4

    # Verify each permutation is handled correctly
    result_tuples = {(r.text.strip(), r.stylize, r.personalization) for r in results}

    expected = {
        ("smooth edges", 75, False),
        ("smooth edges", 300, False),
        ("smooth edges", 75, True),
        ("smooth edges", 300, True),
    }

    assert result_tuples == expected

    # Test with flag permutations
    input_dicts = [
        {"text": "photo"},
        {"text": "photo", "tile": None},
        {"text": "photo", "turbo": None},
        {"text": "photo", "tile": None, "turbo": None},
    ]

    results = [parser.parse_dict(d) for d in input_dicts]
    assert len(results) == 4

    # Verify each permutation is handled correctly
    result_tuples = {(r.text.strip(), r.tile is True, r.turbo is True) for r in results}

    expected = {
        ("photo", False, False),
        ("photo", True, False),
        ("photo", False, True),
        ("photo", True, True),
    }

    assert result_tuples == expected


def test_personalization_parameter():
    """Test parsing of personalization parameter."""
    parser = MidjourneyParser()

    # Test flag without value - should be True
    prompt = parser.parse_dict({"text": "a photo", "p": None})
    assert prompt.personalization is True

    # Test flag with empty string - should be True
    prompt = parser.parse_dict({"text": "a photo", "p": ""})
    assert prompt.personalization is True

    # Test with string value - should be list with one item
    prompt = parser.parse_dict({"text": "a photo", "p": "custom"})
    assert prompt.personalization == ["custom"]

    # Test with list value - should keep list
    prompt = parser.parse_dict({"text": "a photo", "p": ["custom1", "custom2"]})
    assert prompt.personalization == ["custom1", "custom2"]

    # Test with empty list - should be False
    prompt = parser.parse_dict({"text": "a photo", "p": []})
    assert prompt.personalization is False

    # Test without personalization - should be False
    prompt = parser.parse_dict({"text": "a photo"})
    assert prompt.personalization is False


def test_complex_permutations():
    """Test handling of complex parameter permutations."""
    parser = MidjourneyParser()

    # Test with multiple parameter types
    input_dicts: list[MidjargonDict] = [
        {
            "text": "portrait modern",
            "aspect": "1:1",
            "stylize": "100",
            "images": [],
        },
        {
            "text": "portrait modern",
            "aspect": "16:9",
            "stylize": "100",
            "images": [],
        },
        {
            "text": "portrait modern",
            "aspect": "1:1",
            "stylize": "100",
            "personalization": "custom",
            "images": [],
        },
        {
            "text": "portrait modern",
            "aspect": "16:9",
            "stylize": "100",
            "personalization": "custom",
            "images": [],
        },
        {
            "text": "portrait vintage",
            "aspect": "1:1",
            "stylize": "100",
            "images": [],
        },
        {
            "text": "portrait vintage",
            "aspect": "16:9",
            "stylize": "100",
            "images": [],
        },
        {
            "text": "portrait vintage",
            "aspect": "1:1",
            "stylize": "100",
            "personalization": "custom",
            "images": [],
        },
        {
            "text": "portrait vintage",
            "aspect": "16:9",
            "stylize": "100",
            "personalization": "custom",
            "images": [],
        },
    ]

    results = [parser.parse_dict(d) for d in input_dicts]
    assert len(results) == 8

    # Verify each permutation is handled correctly
    result_tuples = {
        (
            r.text.strip(),
            r.personalization[0]
            if isinstance(r.personalization, list)
            else r.personalization,
            f"{r.aspect_width}:{r.aspect_height}",
            r.stylize,
        )
        for r in results
    }

    expected = {
        ("portrait modern", False, "1:1", 100),
        ("portrait modern", False, "16:9", 100),
        ("portrait modern", "custom", "1:1", 100),
        ("portrait modern", "custom", "16:9", 100),
        ("portrait vintage", False, "1:1", 100),
        ("portrait vintage", False, "16:9", 100),
        ("portrait vintage", "custom", "1:1", 100),
        ("portrait vintage", "custom", "16:9", 100),
    }

    assert result_tuples == expected


def test_new_parameters():
    """Test parsing of new parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "quality": str(QUALITY_VALUE),
            "character_weight": str(CHARACTER_WEIGHT_VALUE),
            "style_weight": str(STYLE_WEIGHT_VALUE),
            "style_version": str(STYLE_VERSION_VALUE),
            "repeat": str(REPEAT_VALUE),
        }
    )

    assert prompt.text == "a photo"
    assert prompt.quality == QUALITY_VALUE
    assert prompt.character_weight == CHARACTER_WEIGHT_VALUE
    assert prompt.style_weight == STYLE_WEIGHT_VALUE
    assert prompt.style_version == STYLE_VERSION_VALUE
    assert prompt.repeat == REPEAT_VALUE


def test_new_parameter_validation():
    """Test validation of new parameters."""
    parser = MidjourneyParser()

    # Test invalid quality value
    with pytest.raises(ValueError, match=r"Invalid numeric value for quality: 5"):
        parser.parse_dict({"text": "a photo", "quality": "5"})

    # Test invalid character weight value
    with pytest.raises(
        ValueError, match=r"Invalid numeric value for character_weight: 2000"
    ):
        parser.parse_dict({"text": "a photo", "character_weight": "2000"})

    # Test invalid style weight value
    with pytest.raises(
        ValueError, match=r"Invalid numeric value for style_weight: 5000"
    ):
        parser.parse_dict({"text": "a photo", "style_weight": "5000"})

    # Test invalid style version value
    with pytest.raises(
        ValueError, match=r"Invalid numeric value for style_version: 20"
    ):
        parser.parse_dict({"text": "a photo", "style_version": "20"})

    # Test invalid repeat value
    with pytest.raises(ValueError, match=r"Invalid numeric value for repeat: 200"):
        parser.parse_dict({"text": "a photo", "repeat": "200"})


def test_edge_cases():
    """Test handling of edge cases in Midjourney parser."""
    parser = MidjourneyParser()

    # Test empty prompt
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": ""})

    # Test prompt with only spaces
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": "   "})

    # Test prompt with special characters
    prompt = parser.parse_dict({"text": "a photo with special characters !@#$%^&*()"})
    assert prompt.text == "a photo with special characters !@#$%^&*()"

    # Test prompt with long text
    long_text = "a" * 1000
    prompt = parser.parse_dict({"text": long_text})
    assert prompt.text == long_text

    # Test prompt with mixed types in extra parameters - all should be converted to strings
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "extra1": "123",
            "extra2": "45.67",
            "extra3": "true",
            "extra4": None,
            "extra5": "item1",  # Changed from list to string
        }
    )
    assert prompt.extra_params["extra1"] == "123"
    assert prompt.extra_params["extra2"] == "45.67"
    assert prompt.extra_params["extra3"] == "true"
    assert prompt.extra_params["extra4"] is None
    assert prompt.extra_params["extra5"] == "item1"
