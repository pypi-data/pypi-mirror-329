"""
Constants for Midjourney engine.
"""

# Parameter ranges and constraints
STYLIZE_RANGE = (0, 1000)
CHAOS_RANGE = (0, 100)
WEIRD_RANGE = (0, 3000)
IMAGE_WEIGHT_RANGE = (0.0, 3.0)
SEED_RANGE = (0, 4294967295)
STOP_RANGE = (10, 100)

# New parameter ranges (lenient)
QUALITY_RANGE = (0.1, 2.0)  # More lenient than spec
CHARACTER_WEIGHT_RANGE = (0, 200)  # More lenient than spec
STYLE_WEIGHT_RANGE = (0, 2000)  # More lenient than spec
STYLE_VERSION_RANGE = (1, 10)  # More lenient than spec
REPEAT_RANGE = (1, 100)  # More lenient than spec

# Default values from SPEC.md
DEFAULT_STYLIZE = 100  # --s (stylize) default
DEFAULT_CHAOS = 0  # --chaos default
DEFAULT_WEIRD = 0  # --weird default
DEFAULT_IMAGE_WEIGHT = 1.0  # --iw default
DEFAULT_STOP = 100  # --stop default
DEFAULT_QUALITY = 1  # --quality default
DEFAULT_CHARACTER_WEIGHT = 100  # --cw default
DEFAULT_STYLE_VERSION = 2  # --sv default
DEFAULT_ASPECT_RATIO = "1:1"  # --ar default

# Boolean parameter defaults (all False by default)
DEFAULT_TILE = False  # --tile
DEFAULT_TURBO = False  # --turbo
DEFAULT_RELAX = False  # --relax

# File extensions
ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

# Mode flags
VALID_STYLES = {"raw", "expressive", "cute", "scenic", "original"}  # Extensible
VALID_VERSIONS = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "5.0",
    "5.1",
    "5.2",
    "6",
    "6.1",
}  # Extensible
VALID_NIJI_VERSIONS = {"4", "5", "6"}  # Extensible
