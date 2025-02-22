# Midjargon

`midjargon` is a powerful Python library designed to simplify the parsing and manipulation of Midjourney-style prompts. 

Midjourney uses a specialized syntax for prompts, which we call “midjargon”. It allows for `{}` permutation and for specifying of parameters using an `--` prefix. This syntax is useful for other applications, such as constructing prompts for Flux models. 

The `midjargon` package reads midjargon prompts, deconstructs them into manageable components, ensuring type-safe operations and comprehensive validation. It also converts midjargon prompts into other formats, such as Fal.ai, and serializes them back into the Midjourney format.

_It’s work in progress, but already pretty usable._

## Features

- **Robust Prompt Parsing**:
  - Parses Midjourney prompts into structured components (text, parameters, image URLs)
  - Type-safe parsing with comprehensive validation
  - Supports complex prompt structures and syntax

- **Advanced Permutation Support**:
  - Handles nested permutations in curly braces `{option1, option2}`
  - Supports escaped characters in permutations (e.g., `\,` for literal commas)
  - Automatically expands all possible combinations

- **Comprehensive Parameter Handling**:
  - Validates parameter names and values
  - Supports numeric ranges and type conversion
  - Processes boolean flags and multi-value parameters

- **Image URL Processing**:
  - Extracts and validates image URLs
  - Supports multiple image inputs and file extensions

- **Multi-prompt Support**:
  - Handles weighted prompts using `::`
  - Processes multiple variations in a single input

- **Type Safety**:
  - Full type hints throughout the codebase
  - Pydantic models for robust validation

- **Rich CLI Interface**:
  - Fire-based command-line interface with rich output
  - CLI commands for converting prompts to different formats (Midjourney, Fal.ai)
  - JSON output option for automation

## Installation

```bash
pip install midjargon
```

## Quick Start

### Basic Usage

```python
from midjargon import parse_midjourney_dict, expand_midjargon_input

# Parse a simple prompt
prompt = "a serene landscape --ar 16:9 --stylize 100"
result = expand_midjargon_input(prompt)[0]
validated = parse_midjourney_dict(result)
```

### CLI Usage

Midjargon exposes a single CLI interface with multiple commands. Here are some examples:

```bash
# You can run the tool with uv without installing dependencies: 
uv run midjargon

# You can also run it directly: 
midjargon

# Or using your Python interpreter:
python -m midjargon
```

To get help on the commands: 

```bash
# Help for Fal.ai conversion (convert prompt to Fal.ai format)
midjargon fal --help

# Help for Midjourney conversion
midjargon mj --help

# Help for JSON parsing (MidjargonDict output)
midjargon json --help

# Help for permutation expansion
midjargon perm --help
```

You can also run commands directly:

```bash
# Convert prompt to Fal.ai format:
midjargon fal "a portrait of a cat --ar 1:1"

# Parse prompt to MidjargonDict:
midjargon json "a futuristic city --chaos 20 --stylize 200"

# Convert prompt to Midjourney format:
midjargon mj "a landscape --ar 16:9 --tile"

# Expand prompt permutations:
midjargon perm "a {red, blue} bird on a tree"
```

## Project Structure

```
.
├── LICENSE                    # MIT license
├── README.md                  # Project introduction and documentation
├── TODO.md                    # Task list to clear before release
├── TODO2.md                   # Additional tasks and feature proposals
├── dist                       # Distribution files
├── docs                       # Project documentation
│   ├── midjourney-docs.md      # Original Midjourney documentation
│   ├── refactoring-ideas.md    # Ideas for refactoring and improvements
│   └── specification.md        # Detailed prompt syntax specification
├── package.toml               # Hatch project configuration
├── pyproject.toml             # Python project configuration
├── pytest.ini                 # Pytest configuration
├── uv.lock                    # UV dependency lock file
├── src                        # Source code
│   └── midjargon
│       ├── __init__.py
│       ├── __main__.py        # CLI entry point (Fire-based)
│       ├── cli
│       │   ├── __init__.py
│       │   └── main.py        # CLI command definitions
│       ├── core
│       │   ├── __init__.py
│       │   ├── converter.py     # Conversion utilities for prompts
│       │   ├── input.py         # Input processing and permutation expansion
│       │   ├── parameters.py    # Parsing and validation of parameters
│       │   ├── parser.py        # Basic prompt parsing into dictionaries
│       │   ├── permutations.py  # Permutation expansion logic
│       │   └── type_defs.py     # Type definitions for midjargon
│       └── engines
│           ├── __init__.py
│           ├── base.py          # Abstract base for engine-specific converters
│           ├── fal            # Fal.ai engine implementation
│           │   ├── __init__.py
│           │   └── converter.py   # Conversion of Midjargon dict to Fal.ai format
│           └── midjourney     # Midjourney engine implementation
│               ├── __init__.py
│               ├── constants.py   # Parameter constraints and defaults
│               ├── models.py      # Pydantic models for Midjourney prompts
│               └── parser.py      # Engine-specific parsing logic
└── tests                      # Test suite for midjargon
    ├── cli
    │   ├── __init__.py
    │   └── test_main.py       # CLI tests
    ├── conftest.py
    ├── core
    │   ├── __init__.py
    │   ├── test_input.py      # Tests for input handling
    │   ├── test_parameters.py # Tests for parameter parsing
    │   └── test_permutations.py # Tests for permutation expansion
    ├── engines
    │   ├── __init__.py
    │   ├── midjourney
    │   │   ├── __init__.py
    │   │   └── test_parser.py  # Tests for Midjourney parser
    │   └── test_base.py       # Tests for engine base functionality
    ├── integration
    │   └── test_workflow.py   # Integration tests for full prompt processing
    ├── test_package.py        # Package interface tests
    └── tests                # Additional tests
```

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

### Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install --system --upgrade ".[all]"
   ```
3. Run tests:
   ```bash
   hatch test
   ```
4. Format code:
   ```bash
   hatch fmt
   ```

## License

MIT License - See LICENSE file for details  
.
