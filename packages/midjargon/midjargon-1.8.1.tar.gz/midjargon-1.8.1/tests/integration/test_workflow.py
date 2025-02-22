"""Integration tests for complete midjargon workflow."""

from __future__ import annotations

import sys
from io import StringIO

import pytest

from midjargon import expand_midjargon_input, parse_midjargon_prompt_to_dict
from midjargon.cli.main import MidjargonCLI
from midjargon.engines.midjourney import MidjourneyPrompt, parse_midjourney_dict
from tests.cli.test_main import parse_json_output  # Added import for JSON parsing

# Test constants
ASPECT_WIDTH = 16
ASPECT_HEIGHT = 9
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
WEIRD_VALUE = 1000
SEED_VALUE = 12345
STOP_VALUE = 80
IMAGE_WEIGHT_VALUE = 2.0
QUALITY_VALUE = 1.0
CHARACTER_WEIGHT_VALUE = 100
STYLE_WEIGHT_VALUE = 200
STYLE_VERSION_VALUE = 2
REPEAT_VALUE = 3
PERMUTATION_COUNT_2X2 = 4  # 2 options x 2 options
PERMUTATION_COUNT_2X2X2 = 8  # 2 options x 2 options x 2 options


def process_prompt(prompt: str) -> list[MidjourneyPrompt]:
    """Process a prompt through the complete workflow."""
    # Step 1: Expand permutations
    expanded = expand_midjargon_input(prompt)

    # Step 2: Parse each expanded prompt to a dictionary
    midjargon_dicts = [parse_midjargon_prompt_to_dict(p) for p in expanded]

    # Step 3: Convert each dictionary to a MidjourneyPrompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]


def test_basic_workflow():
    """Test basic prompt workflow without permutations."""
    prompt = f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE}"
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "a beautiful landscape"
    assert result.aspect_width == ASPECT_WIDTH
    assert result.aspect_height == ASPECT_HEIGHT
    assert result.stylize == STYLIZE_VALUE


def test_permutation_workflow():
    """Test workflow with permutations."""
    prompt = f"a {{red, blue}} bird on a {{branch, rock}} --stylize {STYLIZE_VALUE}"
    results = process_prompt(prompt)

    assert len(results) == PERMUTATION_COUNT_2X2  # 2x2 permutations
    texts = {r.text for r in results}
    expected = {
        "a red bird on a branch",
        "a red bird on a rock",
        "a blue bird on a branch",
        "a blue bird on a rock",
    }
    assert texts == expected
    assert all(r.stylize == STYLIZE_VALUE for r in results)


def test_image_workflow():
    """Test workflow with image URLs."""
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    prompt = f"{' '.join(urls)} abstract fusion --iw {IMAGE_WEIGHT_VALUE}"
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "abstract fusion"
    assert len(result.image_prompts) == 2
    assert [p.url for p in result.image_prompts] == urls
    assert result.image_weight == IMAGE_WEIGHT_VALUE


def test_parameter_workflow():
    """Test workflow with various parameter types."""
    prompt = (
        "cyberpunk city --v 5.2 --style raw "
        f"--chaos {CHAOS_VALUE} --weird {WEIRD_VALUE} "
        f"--seed {SEED_VALUE} --stop {STOP_VALUE} "
        "--turbo --tile"
    )
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "cyberpunk city"
    assert result.version == "v5.2"
    assert result.style == "raw"
    assert result.chaos == CHAOS_VALUE
    assert result.weird == WEIRD_VALUE
    assert result.seed == SEED_VALUE
    assert result.stop == STOP_VALUE
    assert result.turbo is True
    assert result.tile is True


def test_new_parameters_workflow():
    """Test workflow with new parameter types."""
    prompt = (
        "portrait photo "
        f"--quality {QUALITY_VALUE} "
        f"--cw {CHARACTER_WEIGHT_VALUE} "
        f"--sw {STYLE_WEIGHT_VALUE} "
        f"--sv {STYLE_VERSION_VALUE} "
        f"--repeat {REPEAT_VALUE} "
        "--cref ref1.jpg ref2.jpg "
        "--sref style1.jpg style2.jpg "
        "--p custom_profile1 custom_profile2"
    )
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "portrait photo"
    assert result.quality == QUALITY_VALUE
    assert result.character_weight == CHARACTER_WEIGHT_VALUE
    assert result.style_weight == STYLE_WEIGHT_VALUE
    assert result.style_version == STYLE_VERSION_VALUE
    assert result.repeat == REPEAT_VALUE
    assert result.character_reference == ["ref1.jpg", "ref2.jpg"]
    assert result.style_reference == ["style1.jpg", "style2.jpg"]
    assert result.personalization == ["custom_profile1", "custom_profile2"]


def test_weighted_prompts_workflow():
    """Test workflow with weighted prompts."""
    prompt = "cyberpunk city::2 neon lights::1"
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]
    assert result.text == "cyberpunk city::2 neon lights::1"


def test_error_workflow():
    """Test error handling in workflow."""
    # Test empty prompt
    with pytest.raises(ValueError, match="Empty prompt"):
        process_prompt("")

    # Test whitespace-only prompt
    with pytest.raises(ValueError, match="Empty prompt"):
        process_prompt("   ")

    # Test invalid parameter value - raises ValueError
    with pytest.raises(ValueError, match=r"Invalid numeric value for stylize: 2000"):
        process_prompt(f"photo --stylize {STYLIZE_VALUE * 20}")

    # Test invalid image URL - treated as extra parameter
    results = process_prompt("photo --image not_a_url")
    assert len(results) == 1
    assert len(results[0].image_prompts) == 0
    assert results[0].extra_params.get("image") == "not_a_url"


def test_complex_workflow():
    """Test workflow with multiple features combined."""
    prompt = (
        "https://example.com/img1.jpg https://example.com/img2.jpg "
        "a {vintage, modern} {portrait, landscape} "
        "with {warm, cool} tones "
        f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} "
        f"--chaos {CHAOS_VALUE} --v 5.2 --style raw "
        f"--quality {QUALITY_VALUE} --cw {CHARACTER_WEIGHT_VALUE} "
        "--turbo"
    )
    results = process_prompt(prompt)

    # 2x2x2 = 8 permutations
    assert len(results) == PERMUTATION_COUNT_2X2X2

    # Check common attributes
    for result in results:
        assert len(result.image_prompts) == 2
        assert result.aspect_width == ASPECT_WIDTH
        assert result.aspect_height == ASPECT_HEIGHT
        assert result.stylize == STYLIZE_VALUE
        assert result.chaos == CHAOS_VALUE
        assert result.version == "v5.2"
        assert result.style == "raw"
        assert result.quality == QUALITY_VALUE
        assert result.character_weight == CHARACTER_WEIGHT_VALUE
        assert result.turbo is True

    # Check text variations
    texts = {r.text for r in results}
    assert len(texts) == PERMUTATION_COUNT_2X2X2  # All combinations are unique


def test_permutations_with_parameters():
    """Test permutations with parameters are handled correctly."""
    prompt = "smooth edges {, --p} --s {75, 300}"
    results = process_prompt(prompt)

    assert len(results) == 4  # Should have 4 permutations

    # Convert results to set of tuples for easier comparison
    result_tuples = {
        (r.text.strip(), bool(r.personalization), r.stylize) for r in results
    }

    # Expected combinations
    expected = {
        ("smooth edges", False, 75),
        ("smooth edges", False, 300),
        ("smooth edges", True, 75),
        ("smooth edges", True, 300),
    }

    assert result_tuples == expected


def test_permutations_with_flag_parameters():
    """Test permutations with flag parameters (no value) are handled correctly."""
    prompt = "photo {, --tile} {, --turbo}"
    results = process_prompt(prompt)

    assert len(results) == 4  # Should have 4 permutations

    # Convert results to set of tuples for easier comparison
    result_tuples = {(r.text.strip(), r.tile is True, r.turbo is True) for r in results}

    # Expected combinations
    expected = {
        ("photo", False, False),
        ("photo", False, True),
        ("photo", True, False),
        ("photo", True, True),
    }

    assert result_tuples == expected


def test_permutations_with_complex_parameters():
    """Test permutations with complex parameter combinations."""
    prompt = "portrait {modern, vintage} {, --p custom} --ar {1:1, 16:9} --s 100"
    results = process_prompt(prompt)

    assert len(results) == 8  # Should have 8 permutations (2 x 2 x 2)

    # Convert results to set of tuples for easier comparison
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


def test_cli_mj_command():
    """Test Midjourney prompt conversion using CLI."""
    cli = MidjargonCLI()
    prompt = "a serene landscape --ar 16:9 --stylize 100"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.mj(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["text"] == "a serene landscape"
    assert data["stylize"] == 100
    assert data["aspect_ratio"] == "16:9"


def test_cli_fal_command():
    """Test Fal.ai prompt conversion using CLI."""
    cli = MidjargonCLI()
    prompt = "a serene landscape --ar 16:9 --stylize 100"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.fal(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["prompt"] == "a serene landscape"
    assert data["stylize"] == 100
    assert data["aspect_ratio"] == "16:9"


def test_cli_perm_command():
    """Test permutation expansion using CLI."""
    cli = MidjargonCLI()
    prompt = "a {red, blue} bird on a {branch, rock}"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.perm(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 4
    assert "a red bird on a branch" in data
    assert "a red bird on a rock" in data
    assert "a blue bird on a branch" in data
    assert "a blue bird on a rock" in data
