from ai_kit.core.web.fetcher import Fetcher, FetcherResult
from ai_kit.core.web.parser import extract_internal_links, llm_html_to_markdown, html_to_markdown
from ai_kit.utils import print_stream
from ai_kit.shared_console import shared_console, shared_error_console
from ai_kit.core.web.duckduckgo import DuckDuckGoSearch
from typing import Optional, Set, Dict, Union, Literal
import aiohttp
from urllib.parse import urlparse
from rich.table import Table
from rich.status import Status

def clean_url(url: str):
    if url.startswith("http") or url.startswith("https"):
        return url
    elif url.startswith("www."):
        return f"https://{url}"
    else:
        return f"https://{url}"

async def get_page_snippets(base_url: str) -> Dict[str, str]:
    """Get snippets for pages on the domain using DuckDuckGo site search."""
    base_domain = urlparse(base_url).netloc
    ddg = DuckDuckGoSearch()
    
    # Search for pages on this domain
    results = await ddg.search(f"site:{base_domain}")
    
    # Create a mapping of URLs to their snippets
    snippets = {}
    for result in results:
        snippets[result["href"]] = result["body"]
    
    return snippets


async def display_links_table(links: Set[str], base_url: str, status: Status):
    """Display internal links in a formatted table."""
    # Get snippets for the domain
    status.update("[bold green]Fetching page descriptions...[/bold green]")
    snippets = await get_page_snippets(base_url)

    # Filter links to only those with snippets
    links_with_snippets = {
        link for link in links 
        if link in snippets or link.rstrip('/') in snippets
    }

    if not links_with_snippets:
        return

    table = Table(title=f"\nRelevant Internal Pages Found on {base_url}")
    table.add_column("Path", style="cyan", no_wrap=True)
    table.add_column("Description", style="white", max_width=60)
    table.add_column("Full URL", style="blue", no_wrap=True)

    # Sort links for consistent display
    sorted_links = sorted(links_with_snippets)

    for link in sorted_links:
        parsed = urlparse(link)
        # Get relative path, or use '/' for homepage
        path = parsed.path or '/'
        if parsed.query:
            path += f"?{parsed.query}"
            
        # Get snippet if available
        snippet = snippets.get(link, "")
        if not snippet and link.rstrip('/') in snippets:
            # Try without trailing slash
            snippet = snippets.get(link.rstrip('/'), "")
            
        table.add_row(path, snippet, link)

    shared_console.print(table)


async def fetch_web(urls: list[str], no_links_table: bool = False) -> Optional[int]:
    """Fetch and convert a webpage to markdown.
    
    Args:
        urls: The URLs to fetch
        no_links_table: If True, skips displaying the internal links table
    """
    if len(urls) > 5:
        shared_error_console.print(f"[red]Error: Too many URLs. Maximum is 5. Only using the first 5.[/red]")
        urls = urls[:5]
    clean_urls = [clean_url(url) for url in urls]

    # ! ARXIV HACK
    for url in clean_urls:
        if "arxiv.org/abs" in url:
            clean_urls.remove(url)
            clean_urls.append(url.replace("arxiv.org/abs", "arxiv.org/pdf"))
            shared_console.print(f"[yellow]HACK: Replacing abstract URL with PDF URL: {url} -> {clean_urls[-1]}[/yellow]")

    try:
        async with Fetcher() as fetcher:
            with shared_console.status("[bold green]Fetching content...[/bold green]") as status:
                results: list[FetcherResult] = await fetcher.batch_fetch(clean_urls)

        for url, result in zip(urls, results):
            if result["type"] == "error":
                shared_error_console.print(f"[red]Error: Could not fetch content from {url}[/red]")
            elif result["type"] == "pdf":
                shared_console.print(f"\n[bold blue]Content from PDF at {url}:[/bold blue]\n")
                shared_console.print(result["content"])
            elif result["type"] == "json":
                shared_console.print(f"\n[bold blue]Content from JSON at {url}:[/bold blue]\n")
                shared_console.print(result["content"])
            elif result["type"] == "html":
                # Extract internal links before cleaning HTML
                internal_links = extract_internal_links(result["content"], url)

                # Convert the cleaned HTML to markdown with no link syntax
                raw_markdown = html_to_markdown(result["content"], no_links=True)

                # Clean the content with Gemini
                with shared_console.status("[bold green]Cleaning content with Gemini...[/bold green]") as status:
                    stream = await llm_html_to_markdown(raw_markdown)

                    # Print the formatted markdown with syntax highlighting
                    shared_console.print(f"\n[bold blue]Content from {url}:[/bold blue]\n")
                    await print_stream(stream)

                    # Display internal links table after content if requested
                    if internal_links and not no_links_table:
                        await display_links_table(internal_links, url, status)
        
        # ! do not indent this any farther!!!
        return 0
    except Exception as e:
        shared_error_console.print(f"[red]Error fetching page: {str(e)}[/red]")
        return 1