from pathlib import Path
import logging
from rich.console import Console
from rich.prompt import Confirm
from ai_kit.utils.fs import package_root
from ai_kit.cli.templating import handle_cursorrules
from ai_kit.shared_console import shared_console

def init_command(log_level: str):
    """Initialize AI Kit with cursor rules and logging setup.
    
    Args:
        log_level: The logging level to set (e.g. INFO, DEBUG, etc.)
    """
    # Setup logging
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level.upper())
    shared_console.print(f"[green]✓ Set logging level to {log_level}[/green]")

    # Handle cursor rules setup
    pkg_root = package_root()
    cursorrules_source = pkg_root / "system_prompts" / "cursorrules.md"  # This is just a reference point
    
    update_cursorrules = Confirm.ask(
        "[bold yellow]Would you like to create/update cursor rules with default AI Kit rules?[/bold yellow]",
        default=True
    )
    
    if update_cursorrules:
        try:
            handle_cursorrules(cursorrules_source, Path(".cursor/rules"))
        except Exception as e:
            shared_console.print(f"[red]Error: Could not update cursor rules: {e}[/red]")
            return

    shared_console.print("\n[bold green]✨ AI Kit initialization complete![/bold green]")
    shared_console.print("You can now use AI Kit commands with the configured settings.")
