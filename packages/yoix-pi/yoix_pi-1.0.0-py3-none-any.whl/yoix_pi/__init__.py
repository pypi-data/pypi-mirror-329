"""BBEdit-style persistent includes for Python."""

from .processor import process_persistent_includes
from .cli import main as cli

__version__ = "0.1.0"
__all__ = ["process_persistent_includes", "cli"]
