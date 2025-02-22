"""Tests for input handling."""

from midjargon.core.input import expand_midjargon_input

# Test constants
PERMUTATION_COUNT_2 = 2  # Single permutation with 2 options
PERMUTATION_COUNT_3 = 3  # Single permutation with 3 options


def test_basic_input():
    """Test basic input without permutations."""
    result = expand_midjargon_input("a simple prompt")
    assert len(result) == 1
    assert result[0] == "a simple prompt"


def test_single_permutation():
    """Test input with a single permutation."""
    result = expand_midjargon_input("a {red, blue} bird")
    assert len(result) == PERMUTATION_COUNT_2
    assert "a red bird" in result
    assert "a blue bird" in result


def test_empty_input():
    """Test empty input handling."""
    result = expand_midjargon_input("")
    assert len(result) == 1
    assert result[0] == ""


def test_multiple_permutations():
    """Test input with multiple permutations."""
    result = expand_midjargon_input("a {red, blue, green} bird")
    assert len(result) == PERMUTATION_COUNT_3
    assert "a red bird" in result
    assert "a blue bird" in result
    assert "a green bird" in result


def test_nested_permutations():
    """Test input with nested permutations."""
    result = expand_midjargon_input("a {red {cat, dog}, blue bird}")
    assert len(result) == PERMUTATION_COUNT_3
    assert "a red cat" in result
    assert "a red dog" in result
    assert "a blue bird" in result


def test_escaped_braces():
    """Test input with escaped braces."""
    result = expand_midjargon_input(r"a \{red, blue\} bird")
    assert len(result) == 1
    assert result[0] == "a {red, blue} bird"


def test_escaped_commas():
    """Test input with escaped commas."""
    result = expand_midjargon_input(r"a {red\, blue, green} bird")
    assert len(result) == PERMUTATION_COUNT_2
    assert "a red, blue bird" in result
    assert "a green bird" in result


def test_unmatched_braces():
    """Test input with unmatched braces."""
    result = expand_midjargon_input("a {red, blue bird")
    assert len(result) == 1
    assert result[0] == "a {red, blue bird"


def test_empty_permutation():
    """Test input with empty permutation options."""
    result = expand_midjargon_input("a {} bird")
    assert len(result) == 1
    assert result[0] == "a bird"


def test_whitespace_handling():
    """Test input with various whitespace patterns."""
    result = expand_midjargon_input("a {  red  ,  blue  } bird")
    assert len(result) == PERMUTATION_COUNT_2
    assert "a red bird" in result
    assert "a blue bird" in result


def test_expand_midjargon_input():
    """Test expand_midjargon_input function to verify prompt expansion."""
    result = expand_midjargon_input("a {red, blue} bird")
    assert len(result) == 2
    assert "a red bird" in result
    assert "a blue bird" in result

    result = expand_midjargon_input("a {red, blue, green} bird")
    assert len(result) == 3
    assert "a red bird" in result
    assert "a blue bird" in result
    assert "a green bird" in result

    result = expand_midjargon_input("a {red {cat, dog}, blue bird}")
    assert len(result) == 3
    assert "a red cat" in result
    assert "a red dog" in result
    assert "a blue bird" in result


def test_handling_escaped_characters():
    """Test handling of escaped characters in expand_midjargon_input."""
    result = expand_midjargon_input(r"a \{red, blue\} bird")
    assert len(result) == 1
    assert result[0] == "a {red, blue} bird"

    result = expand_midjargon_input(r"a {red\, blue, green} bird")
    assert len(result) == 2
    assert "a red, blue bird" in result
    assert "a green bird" in result

    result = expand_midjargon_input(r"a {red, blue\} bird")
    assert len(result) == 1
    assert result[0] == "a {red, blue} bird"
