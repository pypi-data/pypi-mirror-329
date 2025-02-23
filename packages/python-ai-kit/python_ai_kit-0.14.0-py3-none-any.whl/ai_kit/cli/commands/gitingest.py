from typing import Optional
from pathlib import Path
from gitingest import ingest_async
from ai_kit.shared_console import shared_console, shared_error_console
from rich.progress import Progress, SpinnerColumn, TextColumn
from ai_kit.utils.fs import find_workspace_root, WorkspaceError

async def gitingest_command(
    repo: str,
    output_dir: Optional[str],
) -> Optional[int]:
    """Analyze a Git repository and create a prompt-friendly text digest.
    
    Args:
        repo: Path to local directory or GitHub URL
        output_dir: Optional directory to save multiple output files (overrides output_file)
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=f"Analyzing repository: {repo}", total=None)
            
            # Call gitingest's async function
            summary, tree, content = await ingest_async(repo)
            
            # Handle output based on provided parameters
            if output_dir:
                # Create output directory
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                
                # Save each component to separate files
                summary_file = output_path / "summary.md"
                tree_file = output_path / "tree.md"
                content_file = output_path / "content.md"
                digest_file = output_path / "digest.txt"
                
                # Write summary
                with open(summary_file, 'w', encoding='utf-8') as f:
                    f.write("# Repository Analysis Summary\n\n")
                    f.write(summary)
                
                # Write tree
                with open(tree_file, 'w', encoding='utf-8') as f:
                    f.write("# Repository Structure\n\n```\n")
                    f.write(tree)
                    f.write("\n```\n")
                
                # Write content
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write("# Repository Content\n\n")
                    f.write(content)
                
                # Write complete digest
                with open(digest_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Display summary information
                shared_console.print("\n[bold green]Repository Analysis Complete![/bold green]")
                shared_console.print("\n[bold blue]Files created:[/bold blue]")
                shared_console.print(f"[green]✓[/green] Summary: {summary_file}")
                shared_console.print(f"[green]✓[/green] Tree: {tree_file}")
                shared_console.print(f"[green]✓[/green] Content: {content_file}")
                shared_console.print(f"[green]✓[/green] Complete digest: {digest_file}")
            
            return 0
            
    except Exception as e:
        shared_error_console.print(f"[red]Error analyzing repository: {str(e)}[/red]")
        return 1 