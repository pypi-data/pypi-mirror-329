import click
import logging
from pathlib import Path
from dotenv import load_dotenv
from ai_kit.utils.fs import find_workspace_root, WorkspaceError
import warnings
import sys
import asyncio
from ai_kit.cli.registry import registry_instance
from ai_kit import __version__  # Import version
from ai_kit.shared_console import shared_console, shared_error_console
from ai_kit.cli.commands.gitingest import gitingest_command

# Configure basic logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Filter out warnings from internal dependencies
warnings.filterwarnings("ignore", module="pydantic.*")
warnings.filterwarnings("ignore", module="openai.*")


def load_env_files():
    """Load environment variables from .env files in order of precedence."""
    # Load from user's home directory first
    home_env = Path.home() / '.env'
    if home_env.exists():
        load_dotenv(home_env)
    
    # Then load from current directory, allowing it to override home settings
    local_env = Path('.env')
    if local_env.exists():
        load_dotenv(local_env, override=True)

# ! MAIN COMMAND ===============================================
# This is the entry point for the CLI
@click.group(invoke_without_command=True)
@click.version_option(__version__, "--version", "-v", help="Show the version and exit.")
@click.pass_context
def main(ctx):
    """AI development toolkit for managing prompts and scripts."""
    
    # Load environment variables before any command
    load_env_files()

    # Handle no subcommand
    if ctx.invoked_subcommand is None:
        ctx.invoke(help)


# ! INIT COMMAND ===============================================
# This is the command for initializing the [ROOT_DIR] directory structure
# It copies over the template files and makes the index dir
@main.command()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    default="WARNING",
    help="Set logging level",
)
@registry_instance.add(
    name="init",
    description="Initialize AI Kit with cursor rules and logging configuration.",
    usage="ai-kit init [--log-level LEVEL]",
)
def init(log_level: str):
    """Initialize AI Kit with cursor rules and logging setup.

    Steps:
    1. Sets up logging based on --log-level
    2. Creates/updates cursor rules in .cursor/agent.mdc
    
    Options:
    --log-level: Set logging level (DEBUG, INFO, WARNING, ERROR)
    """
    from ai_kit.cli.commands.init import init_command
    init_command(log_level=log_level)


# ! WEB COMMAND GROUP ===============================================
@main.group(name="web")
def web():
    """Web utilities for searching and fetching content."""
    pass

@web.command(name="search")
@click.argument("query")
@click.option(
    "--rerank-query",
    type=str,
    help="Rerank the query",
)
@click.option(
    "--max-results",
    "-n",
    type=int,
    default=20,
    help="Maximum number of results to return",
)
@click.option(
    "--site",
    type=str,
    help="Limit search to a specific domain",
)
@registry_instance.add(
    name="web search",
    description="Search the web for information.",
    usage="ai-kit web search <query> [--rerank-query] [--max-results <n>] [--site <domain>]",
)
def web_search(query: str, rerank_query: str, max_results: int, site: str):
    """Search the web for information."""
    from ai_kit.cli.commands.web.search import search_web

    try:
        # Add site: prefix to query if site is specified
        if site:
            query = f"site:{site} {query}"
        results = asyncio.run(search_web(query, rerank_query, max_results))
    except Exception as e:
        shared_error_console.print(f"[red]Error searching web: {e}[/red]")
        sys.exit(1)

    def pprint(parsed_page: dict):
        shared_console.print(f"[bold cyan]{parsed_page['title']}[/bold cyan]")
        shared_console.print(f"[bold green]{parsed_page['url']}[/bold green]")
        shared_console.print(parsed_page["snippet"])
        shared_console.print("\n")

    for result in results:
        pprint(result)

@web.command(name="fetch")
@click.argument("urls", nargs=-1)
@registry_instance.add(
    name="web fetch",
    description="Fetch and display content from a list of URLs.",
    usage="ai-kit web fetch <url1> <url2> <url3>",
)
def web_fetch(urls: list[str], no_links_table: bool = True):
    """Fetch and display content from a specific URL."""
    from ai_kit.cli.commands.web.fetch import fetch_web
    
    try:
       asyncio.run(fetch_web(urls, no_links_table=no_links_table))
    except Exception as e:
        shared_error_console.print(f"[red]Error fetching URL: {e}[/red]")
        sys.exit(1)

@web.command(name="crawl")
@click.argument("seed_url")
@click.option("--output-dir", "-o", type=str, help="Parent directory where the site content will be saved (default: workspace root)")
@click.option("--site-dir", "-s", type=str, help="Name of the subdirectory for this site's content (default: normalized domain name)")
@click.option("--max-urls", "-n", type=int, default=100, help="Maximum number of URLs to crawl")
@registry_instance.add(
    name="web crawl",
    description="Crawl a documentation site and save it as Markdown files with a directory structure matching the site.",
    usage="ai-kit web crawl <seed_url> [--output-dir <parent_dir>] [--site-dir <site_name>] [--max-urls <n>]",
)
def web_crawl(seed_url: str, output_dir: str | None, site_dir: str | None, max_urls: int):
    """Crawl a documentation site and save it as Markdown files.
    
    The content will be saved in <output_dir>/<site_dir>/, where:
    - output_dir: Parent directory (defaults to workspace root)
    - site_dir: Site-specific subdirectory (defaults to normalized domain name)
    """
    from ai_kit.cli.commands.web.crawl import crawl_web
    
    try:
        # Use workspace root as default output directory
        if output_dir is None:
            try:
                output_dir = str(find_workspace_root())
            except WorkspaceError:
                shared_error_console.print("[yellow]Warning:[/yellow] Could not find workspace root. Using current directory.")
                output_dir = "."
        
        asyncio.run(crawl_web(
            seed_url=seed_url,
            output_dir=output_dir,
            site_dir=site_dir,
            max_urls=max_urls,
        ))
    except Exception as e:
        shared_error_console.print(f"[red]Error crawling: {e}[/red]")
        sys.exit(1)

# ! THINK COMMAND ===============================================
@click.argument("prompt")
@click.option(
    "--think-model",
    "-tm",
    type=str,
    default="r1-70b",
    help="Model to use for thinking",
)
@click.option(
    "--deepthink-model",
    "-dm",
    type=str,
    default="r1",  
    help="Model to use for deep thinking",
)
@main.command()
@registry_instance.add(
    name="think",
    description="Access your brain. If the request is complex enough, this will call on a smar AI to generate a thought stream. Otherwise it will return back to you. You can pass {{ filepath }} in the prompt to reference files and directories in the codebase.",
    usage="ai-kit think <prompt> [--think-model <model>] [--deepthink-model <model>]",
)
def think(prompt: str, think_model: str, deepthink_model: str):
    """Think about the prompt."""
    from ai_kit.cli.commands.think import think_command

    try:
        asyncio.run(think_command(prompt, think_model, deepthink_model))
    except Exception as e:
        shared_error_console.print(f"[red]Error thinking: {e}[/red]")
        sys.exit(1)

# ! HELP COMMAND ===============================================
@main.command()
@registry_instance.add(
    name="help",
    description="Show help information and setup requirements.",
    usage="ai-kit help",
)
def help():
    """Show help information and setup requirements."""
    from ai_kit.cli.commands.help import help_command
    help_command()

# ! STATUS COMMAND ===============================================
@main.command()
@registry_instance.add(
    name="status",
    description="Show status information.",
    usage="ai-kit status",
)
def status():
    """Show status information."""
    from ai_kit.cli.commands.status import status_command
    status_command()


# ! LIST COMMAND ===============================================
# This is the command for listing all commands so every command is registered
@main.command()
@registry_instance.add(
    name="list",
    description="List all commands.",
    usage="ai-kit list.",
)
def list():
    """List all commands."""
    registry_instance.display_commands()

# ! AGENT COMMAND GROUP ===============================================
@main.group(name="agent")
def agent():
    """Agent utilities for managing agents."""
    pass

@agent.command(name="browse")
@click.argument("instruction")
@click.option("--headless", "-h", is_flag=True, help="Run the browser in headless mode", default=False)
@registry_instance.add(
    name="agent browse",
    description="Run a browser automation task with the given instruction.",
    usage="ai-kit agent browse [instruction]",
)
def browse(instruction: str, headless: bool):
    """Run browser automation with natural language instructions."""
    from ai_kit.cli.commands.agent.browse import browse_command

    try:
        asyncio.run(browse_command(instruction, headless))
    except Exception as e:
        shared_error_console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()

# ! disabling this until fixed
# @main.command()
@click.argument("repo")
@click.option(
    "--output-dir", "-d",
    type=str,
    help="Directory to save multiple output files (overrides --output-file)",
    default=".",
)
@registry_instance.add(
    name="gitingest",
    description="Analyze a Git repository and create a prompt-friendly text digest.",
    usage="ai-kit gitingest <repo> [-o output_file] [-d output_dir]",
)
def gitingest(repo: str, output_dir: str):
    """Analyze a Git repository and create a prompt-friendly text digest.
    
    When using --output-dir, the following files will be created:
    - summary.md: Repository analysis summary
    - tree.md: Directory structure
    - content.md: Repository content with markdown formatting
    - digest.txt: Complete digest in plain text
    """
    asyncio.run(gitingest_command(
        repo=repo,
        output_dir=output_dir,
    )) 