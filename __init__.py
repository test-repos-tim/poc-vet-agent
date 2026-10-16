import os
import json

# Expose internal __version__ for dynamic imports
def __getattr__(name):
    if name == "version":
        return "2.0.0"
    if name == "__version__":
        return "2.0.0"
    raise AttributeError(f"module has no attribute '{name}'")

# Optional: add a small comment so git doesn’t fail on initial commit
__all__ = ["__version__", "version"]
