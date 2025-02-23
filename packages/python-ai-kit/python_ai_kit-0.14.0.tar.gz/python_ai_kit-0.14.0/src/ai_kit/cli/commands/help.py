from pathlib import Path
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from ai_kit.shared_console import shared_console
from ai_kit.utils.fs import find_workspace_root
from ai_kit.config.client_config import ClientFactory
import os

def help_command() -> None:
    """Display AI Kit Help information and setup requirements."""
    shared_console.print()
    
    # Show Required API Key (OpenRouter)
    table = Table(
        title="🔑 Required API Key",
        title_style="bold cyan",
        show_header=False,
        box=None,
        padding=(0, 1)
    )
    table.add_column("Key", style="bold blue")
    table.add_column("Value", style="white")
    table.add_column("Link", style="white")
    
    # Get all API keys
    api_keys = ClientFactory.get_api_keys_and_urls()
    
    # First show OpenRouter as required
    openrouter_key = next((key for key in api_keys if key["name"] == "OPENROUTER_API_KEY"), None)
    if openrouter_key:
        has_key = openrouter_key["key"] is not None
        status_style = "green" if has_key else "red"
        status_icon = "✓" if has_key else "✗"
        link_text = f"[white link={openrouter_key['url']}]{openrouter_key['url']}[/]"
        table.add_row(
            f"  {openrouter_key['name']}",
            Text(
                f"{status_icon} {'configured' if has_key else 'not set'}", 
                style=status_style
            ),
            link_text
        )
    
    shared_console.print(table)
    shared_console.print("[dim]OpenRouter is required for basic functionality.[/dim]")
    shared_console.print()
    
    # Show Optional API Keys
    optional_table = Table(
        title="🔑 Optional API Keys (Performance Enhancements)",
        title_style="bold cyan",
        show_header=False,
        box=None,
        padding=(0, 1)
    )
    optional_table.add_column("Key", style="bold blue")
    optional_table.add_column("Value", style="white")
    optional_table.add_column("Link", style="white")
    
    # Add other providers as optional
    priority_providers = ["TOGETHER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY", "COHERE_API_KEY"]
    for provider in priority_providers:
        key_info = next((key for key in api_keys if key["name"] == provider), None)
        if key_info:
            has_key = key_info["key"] is not None
            status_style = "green" if has_key else "dim"
            status_icon = "✓" if has_key else "-"
            link_text = f"[white link={key_info['url']}]{key_info['url']}[/]"
            optional_table.add_row(
                f"  {key_info['name']}",
                Text(
                    f"{status_icon} {'configured' if has_key else 'optional'}", 
                    style=status_style
                ),
                link_text
            )
    
    shared_console.print(optional_table)
    shared_console.print("[dim]These providers can enhance performance for specific models.[/dim]")
    shared_console.print()

    # Show System Prompt Status
    try:
        workspace_root = find_workspace_root()
        cursor_rules_path = workspace_root / ".cursor" / "rules" / "agent.mdc"
        has_cursor_rules = cursor_rules_path.exists()
        
        status_icon = "✓" if has_cursor_rules else "✗"
        status_style = "green" if has_cursor_rules else "red"
        shared_console.print(f"[{status_style}]{status_icon} System Prompt[/{status_style}] [dim](run [white]ai-kit init[/white] to regenerate)[/dim]")
        shared_console.print()
    except Exception:
        shared_console.print("[red]✗ System Prompt[/red] [dim](run [white]ai-kit init[/white] to regenerate)[/dim]")
        shared_console.print() 