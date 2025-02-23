from rich.table import Table
from rich.text import Text
from rich.markup import escape
from dotenv import load_dotenv
from ai_kit.shared_console import shared_console
import os
from ai_kit.config.client_config import ClientFactory

load_dotenv()

def obscure_key(key: str) -> str:
    if not key:
        return "not set"
    return key[:6] + "..." + key[-4:]

def truncate_url(url: str, max_length: int = 50) -> str:
    if len(url) <= max_length:
        return url
    return url[:max_length-3] + "..."


def status_command() -> None:
    """Display AI Kit status information."""
    # Create main status table
    table = Table(
        title="🔍 AI Kit Status",
        title_style="bold cyan",
        show_header=False,
        box=None,
        padding=(0, 1)
    )
    table.add_column("Key", style="bold blue")
    table.add_column("Value", style="white")
    table.add_column("Link", style="white")
    
    # Add API keys section
    table.add_row(
        Text("🔑 API Keys", style="bold yellow"),
        "",
        ""
    )
    
    for api_key in ClientFactory.get_api_keys_and_urls():
        value = os.getenv(api_key["name"])
        has_key = value is not None
        status_style = "green" if has_key else "red"
        status_icon = "✓" if has_key else "✗"
        url = api_key["url"]
        link_text = f"[white link={url}]{truncate_url(url)}[/]" if url != "#" else ""
        table.add_row(
            f"  {api_key['name']}",
            Text(
                f"{status_icon} {obscure_key(value) if has_key else 'not set'}", 
                style=status_style
            ),
            link_text
        )

    shared_console.print()
    shared_console.print(table)
    shared_console.print()

