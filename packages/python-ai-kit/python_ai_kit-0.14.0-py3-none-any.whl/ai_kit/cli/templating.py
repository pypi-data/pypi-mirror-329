from pathlib import Path
from ai_kit.shared_console import shared_console
from rich.prompt import Confirm

def handle_cursorrules(source: Path, dest: Path) -> None:
    """Handle cursor rules file copying with confirmation for overwrites.
    
    Copies all cursor rule files from system_prompts/cursorrules to .cursor/rules directory.
    Prompts for confirmation before overwriting any existing files.
    """
    # Ensure .cursor/rules directory exists
    cursor_dir = Path('.cursor/rules')
    if not cursor_dir.exists():
        cursor_dir.mkdir(parents=True, exist_ok=True)
    
    # Get source directory (the cursorrules directory)
    source_dir = source.parent / "cursorrules"
    if not source_dir.exists():
        shared_console.print("[red]Error: Could not find cursor rules directory[/red]")
        return
        
    # Process each .mdc file in the source directory
    for source_file in source_dir.glob("*.mdc"):
        dest_file = cursor_dir / source_file.name
        
        # If destination exists, ask for confirmation
        if dest_file.exists():
            should_overwrite = Confirm.ask(
                f"[yellow]File {dest_file.name} already exists. Would you like to overwrite it?[/yellow]",
                default=False
            )
            if not should_overwrite:
                shared_console.print(f"[yellow]Skipping {dest_file.name}[/yellow]")
                continue
        
        # Copy the file
        dest_file.write_text(source_file.read_text())
        shared_console.print(f"[green]✓ {'Updated' if dest_file.exists() else 'Created'} cursor rule at {dest_file}[/green]") 