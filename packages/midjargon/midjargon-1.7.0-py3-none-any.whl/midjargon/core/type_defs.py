"""
type_defs.py

Defines type aliases for clarity in the midjargon package.
"""

# The raw input prompt as a string.
MidjargonInput = str

# A list of expanded prompt strings.
MidjargonList = list[str]

# A single expanded prompt string.
MidjargonPrompt = str

# The basic parsed output:
# - "images": list of image URLs (if any)
# - "text": core text prompt
# - All other parameters (keys without the '--' prefix)
MidjargonDict = dict[str, None | str | list[str]]
