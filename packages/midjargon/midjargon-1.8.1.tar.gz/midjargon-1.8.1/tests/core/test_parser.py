"""Tests for prompt parsing functionality."""

from midjargon.core.parser import parse_midjargon_prompt_to_dict

# Test constants
ASPECT_RATIO = "16:9"
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
IMAGE_URL = "https://example.com/image.jpg"


def test_basic_prompt_parsing():
    """Test basic prompt parsing."""
    prompt = "a beautiful landscape --ar 16:9 --stylize 100"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a beautiful landscape"
    assert result["aspect"] == ASPECT_RATIO
    assert result["stylize"] == STYLIZE_VALUE


def test_prompt_with_image_url():
    """Test prompt parsing with image URL."""
    prompt = f"{IMAGE_URL} a mystical forest --chaos 50"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a mystical forest"
    assert result["images"] == [IMAGE_URL]
    assert result["chaos"] == CHAOS_VALUE


def test_prompt_with_multiple_image_urls():
    """Test prompt parsing with multiple image URLs."""
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    prompt = f"{image_urls[0]} {image_urls[1]} a serene landscape --stylize 100"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a serene landscape"
    assert result["images"] == image_urls
    assert result["stylize"] == STYLIZE_VALUE


def test_prompt_with_parameters():
    """Test prompt parsing with various parameters."""
    prompt = "a futuristic city --ar 16:9 --stylize 100 --chaos 50"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a futuristic city"
    assert result["aspect"] == ASPECT_RATIO
    assert result["stylize"] == STYLIZE_VALUE
    assert result["chaos"] == CHAOS_VALUE


def test_prompt_with_empty_parameters():
    """Test prompt parsing with empty parameters."""
    prompt = "a landscape photo --tile --no blur,cars"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a landscape photo"
    assert result["tile"] is None
    assert result["no"] == "blur,cars"


def test_prompt_with_escaped_characters():
    """Test prompt parsing with escaped characters."""
    prompt = r"a \{red, blue\} bird"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == r"a \{red, blue\} bird"


def test_prompt_with_nested_permutations():
    """Test prompt parsing with nested permutations."""
    prompt = "a {big {red, blue}, small green} bird"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a {big {red, blue}, small green} bird"


def test_prompt_with_unmatched_braces():
    """Test prompt parsing with unmatched braces."""
    prompt = "a {red, blue bird"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a {red, blue bird"


def test_prompt_with_empty_permutation():
    """Test prompt parsing with empty permutation options."""
    prompt = "a {} bird"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a {} bird"


def test_prompt_with_whitespace_handling():
    """Test prompt parsing with various whitespace patterns."""
    prompt = "a {  red  ,  blue  } bird"
    result = parse_midjargon_prompt_to_dict(prompt)
    assert result["text"] == "a { red , blue } bird"
