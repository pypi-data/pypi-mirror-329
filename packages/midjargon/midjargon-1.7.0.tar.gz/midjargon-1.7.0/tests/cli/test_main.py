#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest", "rich"]
# ///

"""Tests for CLI functionality."""

import json
import re
import sys
from io import StringIO
from typing import Any

import pytest
from rich.console import Console

from midjargon.cli.main import MidjargonCLI

# Test constants
ASPECT_WIDTH = 16
ASPECT_HEIGHT = 9
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
IMAGE_PROMPTS_COUNT = 2
PERMUTATION_COUNT_2X2 = 4  # 2 options x 2 options

ANSI_ESCAPE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")


def parse_json_output(output_stream: StringIO) -> Any:
    """Parse JSON output from the CLI, removing ANSI escape sequences if any."""
    output_stream.seek(0)
    output = output_stream.getvalue()
    # Remove ANSI escape sequences
    output = ANSI_ESCAPE.sub("", output)
    output = output.strip()
    if not output:
        msg = "No JSON found in output"
        raise ValueError(msg)
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        msg = "No JSON found in output"
        raise ValueError(msg) from e


@pytest.fixture
def cli():
    """Fixture to provide CLI instance."""
    return MidjargonCLI()


def test_basic_prompt(cli):
    """Test basic prompt processing."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json(
            f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT}",
            json_output=True,
        )
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["text"] == "a beautiful landscape"
    assert data["aspect"] == f"{ASPECT_WIDTH}:{ASPECT_HEIGHT}"


def test_permutations(cli):
    """Test permutation processing."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.perm("a {red, blue} bird", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 2
    texts = set(data)
    assert texts == {"a red bird", "a blue bird"}


def test_raw_output(cli):
    """Test raw output mode."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json(f"a photo --stylize {STYLIZE_VALUE}", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["text"] == "a photo"
    assert data["stylize"] == STYLIZE_VALUE


def test_json_output_formatting(cli):
    """Test JSON output formatting."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("a photo", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["text"] == "a photo"
    assert "images" in data


def test_invalid_input(cli):
    """Test handling of invalid input."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
        assert data["text"] == ""


def test_parameter_validation(cli):
    """Test parameter validation."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json(
            f"a photo --stylize {STYLIZE_VALUE * 20}", json_output=True
        )  # Over max
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
        assert data["stylize"] == STYLIZE_VALUE * 20  # Now accepts any value


def test_image_url_handling(cli):
    """Test handling of image URLs."""
    url = "https://example.com/image.jpg"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json(f"{url} a fusion", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["text"] == "a fusion"
    assert len(data["images"]) == 1
    assert data["images"][0] == url


def test_no_color_output(cli):
    """Test no-color output mode."""
    Console(force_terminal=False)
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("a photo", json_output=True, no_color=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["text"] == "a photo"


def test_complex_prompt(cli):
    """Test complex prompt with multiple features."""
    prompt = (
        "https://example.com/img1.jpg https://example.com/img2.jpg "
        "a {red, blue} bird on a {branch, rock} "
        f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} --chaos {CHAOS_VALUE}"
    )
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == PERMUTATION_COUNT_2X2
    for prompt in data:
        assert len(prompt["images"]) == IMAGE_PROMPTS_COUNT
        assert prompt["stylize"] == STYLIZE_VALUE
        assert prompt["chaos"] == CHAOS_VALUE
        assert prompt["aspect"] == f"{ASPECT_WIDTH}:{ASPECT_HEIGHT}"


def test_personalization_parameter(cli):
    """Test personalization parameter handling in different forms."""
    # Test flag form (--p)
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("a photo --p", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["personalization"] is None  # Flag parameters should be None

    # Test with code (--p CODE1)
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("a photo --p CODE1", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["personalization"] == ["CODE1"]

    # Test with multiple codes (--p "CODE1 CODE2")
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json('a photo --p "CODE1 CODE2"', json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["personalization"] == ["CODE1", "CODE2"]


def test_numeric_range_permutations(cli):
    """Test handling of numeric parameters in permutations."""
    # Test stylize parameter range
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("a photo --s {75, 300}", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 2
    stylize_values = {prompt["stylize"] for prompt in data}
    assert stylize_values == {75, 300}

    # Test multiple numeric parameters
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("a photo --s {75, 300} --c {0, 50}", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 4  # 2x2 combinations
    stylize_values = {prompt["stylize"] for prompt in data}
    chaos_values = {prompt["chaos"] for prompt in data}
    assert stylize_values == {75, 300}
    assert chaos_values == {0, 50}


def test_nested_parameter_permutations(cli):
    """Test handling of nested permutations with parameters."""
    # Test personalization with nested options
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("smooth edges {, --p {, CODE1}} --s {75, 300}", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 6  # 3x2 combinations (no --p, empty --p, --p CODE1) x (75, 300)

    # Verify all combinations
    variants = [
        (None, 75),  # No --p, stylize 75
        (None, 300),  # No --p, stylize 300
        (True, 75),  # Empty --p, stylize 75
        (True, 300),  # Empty --p, stylize 300
        (["CODE1"], 75),  # --p with code, stylize 75
        (["CODE1"], 300),  # --p with code, stylize 300
    ]
    for prompt in data:
        assert prompt["text"] == "smooth edges"
        assert (prompt.get("personalization"), prompt["stylize"]) in variants

    # Test more complex nested permutations
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.json("smooth edges {, --p {, CODE1 CODE2}} --s {75, 300}", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 6  # 3x2 combinations

    # Verify all combinations
    variants = [
        (None, 75),  # No --p, stylize 75
        (None, 300),  # No --p, stylize 300
        (True, 75),  # Empty --p, stylize 75
        (True, 300),  # Empty --p, stylize 300
        (["CODE1", "CODE2"], 75),  # --p with codes, stylize 75
        (["CODE1", "CODE2"], 300),  # --p with codes, stylize 300
    ]
    for prompt in data:
        assert prompt["text"] == "smooth edges"
        assert (prompt.get("personalization"), prompt["stylize"]) in variants


def test_mj_command(cli):
    """Test Midjourney prompt conversion."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.mj("a serene landscape --ar 16:9 --stylize 100", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)  # Changed from list to dict
    assert data["text"] == "a serene landscape"
    assert data["stylize"] == 100
    assert data["aspect_ratio"] == "16:9"


def test_fal_command(cli):
    """Test Fal.ai prompt conversion."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.fal("a serene landscape --ar 16:9 --stylize 100", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, dict)
    assert data["prompt"] == "a serene landscape"
    assert data["aspect_ratio"] == "16:9"
    assert data["stylize"] == 100


def test_perm_command(cli):
    """Test permutation expansion."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.perm("a {red, blue} bird on a {branch, rock}", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 4
    expected = [
        "a red bird on a branch",
        "a red bird on a rock",
        "a blue bird on a branch",
        "a blue bird on a rock",
    ]
    assert set(data) == set(expected)
