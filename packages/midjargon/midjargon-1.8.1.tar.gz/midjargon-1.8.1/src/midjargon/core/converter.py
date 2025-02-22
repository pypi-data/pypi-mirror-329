"""
TODO: Here are several end-user functionalites that our code can do. Your task is to implement the body of these functions, following the `TODO` indicators:

1. permute_prompt
2. parse_prompt
3. _prep_conversion
4. to_midjourney_prompts
5. to_fal_dicts

Let's modify the `cli` section of our code and expose these functions as Fire CLI commands. Move the existing CLI handling into a Fire `midjargon` command.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Annotated as Doc

from midjargon.core.input import expand_midjargon_input
from midjargon.core.parser import parse_midjargon_prompt_to_dict
from midjargon.engines.fal import FalDict, to_fal_dict
from midjargon.engines.midjourney import MidjourneyPrompt, parse_midjourney_dict

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict


def permute_prompt(
    text: Doc[str, "Input prompt that may include permutation markers"],
) -> Doc[list[str], "List of permutated prompt strings"]:
    """
    Permute the input prompt, expanding it into a list of strings, by replacing permutation markers with actual values.

    Also, in our CLI, expose this as `permute` command.

    Args:
        text: The input prompt containing permutation markers.

    Returns:
        Always list of permutated prompt strings.
    """
    return expand_midjargon_input(text)


def parse_prompt(
    text: Doc[str, "Input prompt string"],
    permute: Doc[
        bool,
        "if true, we pass the prompt to permute_prompt first and then parse all prompts",
    ],
) -> Doc[MidjargonDict | list[MidjargonDict], "List of parsed prompt dicts"]:
    """
    Parse the input prompt into:
    - a single dict (if permute is False)
    - or a list of dicts (if permute is True). When permute is True, we always return a list, even if there's only one result.

    Also, in our CLI, expose this as `json` command. In CLI.

    Args:
        text: The input prompt that may contain permutation markers if permute is True.
        permute: If True, we pass the prompt to permute_prompt first and then parse all prompts.

    Returns:
        A single dict (if permute is False) or a list of dicts (if permute is True).
    """
    if not permute:
        return parse_midjargon_prompt_to_dict(text)

    expanded = permute_prompt(text)
    if not expanded:
        return [parse_midjargon_prompt_to_dict(text)]

    return [parse_midjargon_prompt_to_dict(prompt) for prompt in expanded]


def _prep_conversion(
    prompt: Doc[
        str | list[str] | MidjargonDict | list[MidjargonDict],
        "Prompt(s) to convert, in various forms",
    ],
) -> Doc[list[MidjargonDict], "List of MidJargonDicts"]:
    """
    If input is:
        - a single str, permute it and call this function on the list of the result strings
        - a list of strings, call parse_prompt on each, then call this function again on the resulting list of dicts
        - a single dict, treat it as a single-item list of dicts
    Return:
        - a list of MidJargonDict
    """
    if isinstance(prompt, str):
        # Always expand permutations for strings
        expanded = permute_prompt(str(prompt))
        if not expanded:
            # If no permutations, parse as a single prompt
            return [parse_prompt(prompt, permute=False)]  # type: ignore
        # Parse each expanded permutation
        return [parse_prompt(p, permute=False) for p in expanded]  # type: ignore

    if isinstance(prompt, list):
        if not prompt:
            return []
        if all(isinstance(p, str) for p in prompt):
            # For list of strings, parse each one with permutations
            dicts = []
            for p in prompt:
                expanded = permute_prompt(str(p))
                if expanded:
                    dicts.extend(parse_prompt(exp, permute=False) for exp in expanded)  # type: ignore
                else:
                    dicts.append(parse_prompt(p, permute=False))  # type: ignore
            return dicts
        if all(isinstance(p, dict) for p in prompt):
            return list(prompt)  # type: ignore
        msg = f"Unsupported list item type: {type(prompt[0])}"
        raise ValueError(msg)

    if isinstance(prompt, dict):
        return [prompt]

    msg = f"Unsupported prompt type: {type(prompt)}"
    raise ValueError(msg)


def to_midjourney_prompts(
    prompt: Doc[
        str | list[str] | MidjargonDict | list[MidjargonDict],
        "Prompt(s) to convert as Midjourney prompt",
    ],
) -> Doc[MidjourneyPrompt | list[MidjourneyPrompt], "Midjourney prompt(s)"]:
    """
    Convert the input prompt(s) into a Midjourney prompt(s). Pass the inputs to _prep_conversion and then take the resulting list of dicts and perform the actual conversion, calling parse_midjourney_dict on each, and prepare a list of MidjourneyPrompt results.

    Also, in our CLI, expose this as `midjourney` command.

    Return:
        - a single MidjourneyPrompt if input is a single dict or non-permuted string
        - a list of MidjourneyPrompt if input contains permutations or is a list
    """
    dicts = _prep_conversion(prompt)
    if not dicts:
        msg = "No valid prompts found"
        raise ValueError(msg)

    results = [parse_midjourney_dict(d) for d in dicts]
    # Return a list if input was a string with permutations or a list
    if isinstance(prompt, str) and "{" in prompt:
        return results
    if isinstance(prompt, list):
        return results
    return results[0] if len(results) == 1 else results


def to_fal_dicts(
    prompt: Doc[
        str | list[str] | MidjargonDict | list[MidjargonDict],
        "Prompt(s) to convert as Fal prompt",
    ],
) -> Doc[FalDict | list[FalDict], "Fal prompt(s)"]:
    """
    Convert the input prompt(s) into Fal.ai prompt(s). Pass the inputs to _prep_conversion and then take the resulting list of dicts and perform the actual conversion, calling to_fal_dict on each, and prepare a list of FalDict results.

    Also, in our CLI, expose this as `fal` command.

    Return:
        - a single FalDict if input is a single dict or non-permuted string
        - a list of FalDict if input contains permutations or is a list
    """
    dicts = _prep_conversion(prompt)
    if not dicts:
        msg = "No valid prompts found"
        raise ValueError(msg)

    results = [to_fal_dict(d) for d in dicts]
    # Always return a list if input was a string with permutations
    if isinstance(prompt, str) and "{" in prompt:
        return results
    if isinstance(prompt, list):
        return results
    # For single inputs without permutations, return just the first result
    return results[0] if len(results) == 1 else results
