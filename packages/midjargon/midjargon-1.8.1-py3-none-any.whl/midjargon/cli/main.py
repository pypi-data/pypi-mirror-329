#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fire", "rich", "pydantic"]
# ///

"""
midjargon.cli.main
~~~~~~~~~~~~~~~~~

A CLI tool that parses and validates Midjourney prompts.
Supports both raw parsing and Midjourney-specific validation.
"""

import json
import sys
from typing import Any, NoReturn

import fire
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from midjargon.core.converter import (
    parse_prompt,
    permute_prompt,
    to_fal_dicts,
    to_midjourney_prompts,
)

# Install rich traceback handler
install(show_locals=True)


def _handle_error(console: Console, error: Exception) -> NoReturn:
    """Handle errors by printing to stderr and exiting."""
    error_console = Console(stderr=True)
    error_console.print(f"Error: {error!s}", style="red")
    sys.exit(1)


def _output_json(data: Any) -> None:
    """Output data as formatted JSON without any Rich formatting."""
    sys.stdout.write(json.dumps(data, indent=2))
    sys.stdout.flush()


def _format_prompt(prompt: Any) -> str:
    """Format a prompt for display."""
    if hasattr(prompt, "model_dump"):
        return json.dumps(prompt.model_dump(), indent=2)
    return json.dumps(prompt, indent=2)


class MidjargonCLI:
    """Midjargon CLI interface."""

    def perm(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> None:
        """
        Permute a prompt string, expanding all permutation markers.

        Args:
            prompt: The prompt string to permute.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A {red, blue, green} bird on a {branch, rock}"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)

        try:
            results = permute_prompt(prompt)

            if json_output:
                _output_json(results)
                return

            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                console.print(Panel(result))

        except (
            ValueError,
            TypeError,
            SyntaxError,
        ) as error:  # More specific exceptions
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)

    def json(
        self,
        prompt: str,
        *,
        json_output: bool = True,
        no_color: bool = False,
    ) -> None:
        """
        Parse a prompt into MidjargonDict format.

        Args:
            prompt: The prompt string to parse.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
        """
        console = Console(force_terminal=not no_color)

        try:
            # Always expand permutations to ensure consistent behavior with other commands
            results = parse_prompt(prompt, permute=True)

            # If there are no permutations (result is a single-item list), return just the dict
            if isinstance(results, list) and len(results) == 1:
                results = results[0]

            if json_output:
                _output_json(results)
                return

            if isinstance(results, list):
                for i, result in enumerate(results, 1):
                    if len(results) > 1:
                        console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(result)))
            else:
                console.print(Panel(_format_prompt(results)))

        except (
            ValueError,
            TypeError,
            SyntaxError,
        ) as error:  # More specific exceptions
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)

    def mj(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> None:
        """
        Convert a prompt to Midjourney format.

        Args:
            prompt: The prompt string to convert.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
        """
        console = Console(force_terminal=not no_color)

        try:
            results = to_midjourney_prompts(prompt)

            if json_output:
                if isinstance(results, list):
                    json_results = [prompt.model_dump() for prompt in results]
                else:
                    json_results = results.model_dump()
                _output_json(json_results)
                return

            if isinstance(results, list):
                for i, result in enumerate(results, 1):
                    if len(results) > 1:
                        console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(result)))
            else:
                console.print(Panel(_format_prompt(results)))

        except (
            ValueError,
            TypeError,
            SyntaxError,
        ) as error:  # More specific exceptions
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)

    def fal(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> None:
        """
        Convert a prompt to Fal.ai format.

        Args:
            prompt: The prompt string to convert.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
        """
        console = Console(force_terminal=not no_color)

        try:
            results = to_fal_dicts(prompt)

            if json_output:
                _output_json(results)
                return

            if isinstance(results, list):
                for i, result in enumerate(results, 1):
                    if len(results) > 1:
                        console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(result)))
            else:
                console.print(Panel(_format_prompt(results)))

        except (
            ValueError,
            TypeError,
            SyntaxError,
        ) as error:  # More specific exceptions
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)


def main() -> None:
    from rich.ansi import AnsiDecoder
    from rich.console import Console, Group
    from rich.theme import Theme
    from rich.traceback import install

    install(show_locals=True)
    ansi_decoder = AnsiDecoder()
    console = Console(theme=Theme({"prompt": "cyan", "question": "bold cyan"}))

    def display(lines, out):
        console.print(Group(*map(ansi_decoder.decode_line, lines)))

    fire.core.Display = display

    """Run the CLI application."""
    fire.Fire(MidjargonCLI())


if __name__ == "__main__":
    main()
