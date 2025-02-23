"""AI Kit - The first CLI designed for AI agents."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("python-ai-kit")
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback version for development 