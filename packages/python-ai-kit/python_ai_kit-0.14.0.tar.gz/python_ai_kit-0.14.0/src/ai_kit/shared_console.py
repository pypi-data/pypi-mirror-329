"""Shared console instances for consistent rich output across the codebase."""
from rich.console import Console

# Create shared console instances that all other modules can import
shared_console = Console()
shared_error_console = Console(stderr=True) 