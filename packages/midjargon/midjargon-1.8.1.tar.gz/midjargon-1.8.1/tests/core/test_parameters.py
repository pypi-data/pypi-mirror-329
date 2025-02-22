"""Tests for parameter parsing functionality."""

import pytest

from midjargon.core.parameters import parse_parameters


def test_basic_parameter_parsing():
    """Test parsing of basic parameters."""
    param_str = "--ar 16:9 --stylize 100"
    params = parse_parameters(param_str)
    assert params["aspect"] == "16:9"
    assert params["stylize"] == "100"


def test_flag_parameters():
    """Test parsing of flag parameters (without values)."""
    param_str = "--tile --turbo --relax"
    params = parse_parameters(param_str)
    assert params["tile"] is None
    assert params["turbo"] is None
    assert params["relax"] is None


def test_parameter_with_multiple_values():
    """Test parsing parameters that accept multiple values."""
    param_str = "--no blur,cars,watermark"
    params = parse_parameters(param_str)
    assert params["no"] == "blur,cars,watermark"


def test_parameter_with_spaces():
    """Test parsing parameters with values containing spaces."""
    param_str = '--style "raw photo" --seed 123456'
    params = parse_parameters(param_str)
    assert params["style"] == "raw photo"
    assert params["seed"] == "123456"


def test_mixed_parameters():
    """Test parsing a mix of different parameter types."""
    param_str = '--ar 16:9 --tile --no blur,cars --style "raw photo"'
    params = parse_parameters(param_str)
    assert params["aspect"] == "16:9"
    assert params["tile"] is None
    assert params["no"] == "blur,cars"
    assert params["style"] == "raw photo"


def test_shorthand_parameters():
    """Test parsing of shorthand parameter names."""
    param_str = "--s 100 --c 50 --w 1000 --iw 2.0 --q 1.0"
    params = parse_parameters(param_str)
    assert params["stylize"] == "100"
    assert params["chaos"] == "50"
    assert params["weird"] == "1000"
    assert params["image_weight"] == "2.0"
    assert params["quality"] == "1.0"


def test_niji_version_parameter():
    """Test parsing of niji version parameter."""
    # Test basic niji
    params = parse_parameters("--niji")
    assert params["version"] == "niji"

    # Test niji with version
    params = parse_parameters("--niji 6")
    assert params["version"] == "niji 6"


def test_version_parameter():
    """Test parsing of version parameter."""
    # Test v parameter
    params = parse_parameters("--v 5.2")
    assert params["version"] == "5.2"


def test_personalization_parameter():
    """Test parsing of personalization parameter."""
    # Test basic p parameter
    params = parse_parameters("--p")
    assert params["personalization"] is None  # Flag without value is None

    # Test p parameter with value
    params = parse_parameters("--p custom")
    assert params["personalization"] == ["custom"]

    # Test p parameter with multiple values
    params = parse_parameters("--p custom1 custom2")
    assert params["personalization"] == ["custom1", "custom2"]

    # Test personalization parameter with value
    params = parse_parameters("--personalization custom")
    assert params["personalization"] == ["custom"]

    # Test personalization parameter with multiple values
    params = parse_parameters("--personalization custom1 custom2")
    assert params["personalization"] == ["custom1", "custom2"]


def test_reference_parameters():
    """Test parsing of reference parameters."""
    param_str = "--cref img1.jpg img2.jpg --sref style1.jpg style2.jpg"
    params = parse_parameters(param_str)
    assert params["character_reference"] == ["img1.jpg", "img2.jpg"]
    assert params["style_reference"] == ["style1.jpg", "style2.jpg"]


def test_parameter_order():
    """Test that parameter order is preserved in output."""
    param_str = "--seed 123 --ar 16:9 --chaos 20 --tile"
    params = parse_parameters(param_str)
    keys = list(params.keys())
    assert keys == ["seed", "aspect", "chaos", "tile"]


def test_invalid_parameters():
    """Test handling of invalid parameter formats."""
    with pytest.raises(ValueError, match="Empty parameter name"):
        parse_parameters("--")  # Empty parameter name

    with pytest.raises(ValueError, match="Missing value for parameter"):
        parse_parameters("--ar")  # Missing required value

    with pytest.raises(ValueError, match="Parameter name cannot start with dash"):
        parse_parameters("ar 16:9")  # Missing -- prefix

    with pytest.raises(ValueError, match="Missing value for parameter"):
        parse_parameters("--v")  # Missing version value


def test_parse_parameters():
    """Test parse_parameters function to verify parameter parsing."""
    param_str = "--ar 16:9 --stylize 100"
    params = parse_parameters(param_str)
    assert params["aspect"] == "16:9"
    assert params["stylize"] == "100"

    param_str = "--tile --turbo --relax"
    params = parse_parameters(param_str)
    assert params["tile"] is None
    assert params["turbo"] is None
    assert params["relax"] is None

    param_str = "--no blur,cars,watermark"
    params = parse_parameters(param_str)
    assert params["no"] == "blur,cars,watermark"

    param_str = '--style "raw photo" --seed 123456'
    params = parse_parameters(param_str)
    assert params["style"] == "raw photo"
    assert params["seed"] == "123456"

    param_str = '--ar 16:9 --tile --no blur,cars --style "raw photo"'
    params = parse_parameters(param_str)
    assert params["aspect"] == "16:9"
    assert params["tile"] is None
    assert params["no"] == "blur,cars"
    assert params["style"] == "raw photo"

    param_str = "--s 100 --c 50 --w 1000 --iw 2.0 --q 1.0"
    params = parse_parameters(param_str)
    assert params["stylize"] == "100"
    assert params["chaos"] == "50"
    assert params["weird"] == "1000"
    assert params["image_weight"] == "2.0"
    assert params["quality"] == "1.0"

    params = parse_parameters("--niji")
    assert params["version"] == "niji"

    params = parse_parameters("--niji 6")
    assert params["version"] == "niji 6"

    params = parse_parameters("--v 5.2")
    assert params["version"] == "5.2"

    params = parse_parameters("--p")
    assert params["personalization"] is None  # Flag without value is None

    params = parse_parameters("--p custom")
    assert params["personalization"] == ["custom"]

    params = parse_parameters("--personalization custom")
    assert params["personalization"] == ["custom"]

    param_str = "--cref img1.jpg img2.jpg --sref style1.jpg style2.jpg"
    params = parse_parameters(param_str)
    assert params["character_reference"] == ["img1.jpg", "img2.jpg"]
    assert params["style_reference"] == ["style1.jpg", "style2.jpg"]

    param_str = "--seed 123 --ar 16:9 --chaos 20 --tile"
    params = parse_parameters(param_str)
    keys = list(params.keys())
    assert keys == ["seed", "aspect", "chaos", "tile"]

    with pytest.raises(ValueError, match="Empty parameter name"):
        parse_parameters("--")  # Empty parameter name

    with pytest.raises(ValueError, match="Missing value for parameter"):
        parse_parameters("--ar")  # Missing required value

    with pytest.raises(ValueError, match="Parameter name cannot start with dash"):
        parse_parameters("ar 16:9")  # Missing -- prefix

    with pytest.raises(ValueError, match="Missing value for parameter"):
        parse_parameters("--v")  # Missing version value


def test_flag_parameters_handling():
    """Test handling of flag parameters in parse_parameters."""
    param_str = "--tile --turbo --relax --video --remix"
    params = parse_parameters(param_str)
    assert params["tile"] is None
    assert params["turbo"] is None
    assert params["relax"] is None
    assert params["video"] is None
    assert params["remix"] is None

    param_str = "--p"
    params = parse_parameters(param_str)
    assert params["personalization"] is None  # Flag without value is None

    param_str = "--p custom"
    params = parse_parameters(param_str)
    assert params["personalization"] == ["custom"]

    param_str = "--personalization custom"
    params = parse_parameters(param_str)
    assert params["personalization"] == ["custom"]


def test_special_seed_values():
    """Test handling of special seed values."""
    # Test random seed
    params = parse_parameters("--seed random")
    assert params["seed"] == "random"

    # Test numeric seed
    params = parse_parameters("--seed 12345")
    assert params["seed"] == "12345"


def test_reference_url_handling():
    """Test handling of URLs in reference parameters."""
    # Test character reference with quoted URL containing spaces
    params = parse_parameters('--cref "https://example.com/image with spaces.jpg"')
    assert params["character_reference"] == [
        "https://example.com/image with spaces.jpg"
    ]

    # Test style reference with quoted URL containing spaces
    params = parse_parameters('--sref "https://example.com/style with spaces.jpg"')
    assert params["style_reference"] == ["https://example.com/style with spaces.jpg"]

    # Test character reference with single URL (no quotes)
    params = parse_parameters("--cref https://example.com/image.jpg")
    assert params["character_reference"] == ["https://example.com/image.jpg"]

    # Test style reference with single URL (no quotes)
    params = parse_parameters("--sref https://example.com/style.jpg")
    assert params["style_reference"] == ["https://example.com/style.jpg"]


def test_niji_version_handling():
    """Test handling of niji version parameter."""
    # Test basic niji flag
    params = parse_parameters("--niji")
    assert params["version"] == "niji"

    # Test niji with version
    params = parse_parameters("--niji 5")
    assert params["version"] == "niji 5"

    # Test niji with version in permutation
    params = parse_parameters("--niji 6")
    assert params["version"] == "niji 6"

    # Ensure no 'v' prefix is added
    version = str(params["version"])  # Convert to string to use startswith
    assert not version.startswith("v")
