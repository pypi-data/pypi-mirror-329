from pathlib import Path
import re
from typing import Optional
from urllib.parse import urlparse, urljoin

from rich.progress import Progress, SpinnerColumn, TextColumn
from bs4 import BeautifulSoup

from ai_kit.core.crawler import Crawler
from ai_kit.shared_console import shared_console

def sanitize_filename(name: str) -> str:
    """Sanitize a filename by replacing invalid characters with underscores."""
    return re.sub(r'[^a-zA-Z0-9\-_\.]', '_', name)

def determine_file_path(url: str, seed_path: str, output_dir: Path) -> Path:
    """
    Determine the output file path for a given URL.
    
    Args:
        url: The URL being processed
        seed_path: The base path from the seed URL
        output_dir: The root directory to save files in
    
    Returns:
        A Path object representing where the file should be saved
    """
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    
    # Remove the seed_path from the start of the url_path
    if not url_path.startswith(seed_path):
        relative_path = url_path
    else:
        relative_path = url_path[len(seed_path):]
    
    if not relative_path:
        return output_dir / 'index.md'
    
    path_obj = Path(relative_path)
    if relative_path.endswith('/'):
        # Directory, create index.md inside
        dir_parts = path_obj.parts
        sanitized_parts = [sanitize_filename(part) for part in dir_parts if part]
        full_dir = output_dir.joinpath(*sanitized_parts)
        return full_dir / 'index.md'
    else:
        # File, use the last part as filename
        dir_parts = path_obj.parent.parts
        sanitized_dir_parts = [sanitize_filename(part) for part in dir_parts if part]
        full_dir = output_dir.joinpath(*sanitized_dir_parts)
        file_name = sanitize_filename(path_obj.name) + '.md'
        return full_dir / file_name

def validate_url(url: str) -> str:
    """Validate and normalize the URL."""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)
    
    if not parsed.scheme in ('http', 'https'):
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Must be http or https.")
    
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}. Must include domain name.")
    
    # Return the full URL without any normalization
    return url

def normalize_domain(domain: str) -> str:
    """Normalize a domain by removing subdomains and TLDs."""
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[-2:])
    else:
        return domain

async def crawl_web(
    seed_url: str,
    output_dir: str,
    site_dir: Optional[str] = None,
    max_urls: int = 100,
    debug: bool = True,
):
    """
    Crawl a documentation site and save it as Markdown files with a directory structure matching the site.
    
    Args:
        seed_url: The starting URL to crawl from
        output_dir: Parent directory where the site content will be saved
        site_dir: Name of the subdirectory for this site's content (defaults to normalized domain name)
        max_urls: Maximum number of URLs to crawl
        debug: Whether to print debug information
    """
    # Validate and normalize URLs
    try:
        seed_url = validate_url(seed_url)
        parsed = urlparse(seed_url)
        base_domain = parsed.netloc
        normalized_base = site_dir if site_dir else normalize_domain(base_domain)
        
        shared_console.print(f"Starting crawl from: {seed_url}")
        if debug:
            shared_console.print(f"Base domain: {base_domain}")
            shared_console.print(f"Output directory: {output_dir}/{normalized_base}/")
            shared_console.print(f"Seed path: {parsed.path or '/'}")
    except ValueError as e:
        shared_console.print(f"[red]Error:[/red] {str(e)}")
        return

    # Create output directory with domain subdirectory
    output_dir_path = Path(output_dir) / normalized_base
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Initialize crawler with debug
    class DebugCrawler(Crawler):
        def extract_links(self, base_url, html):
            links = super().extract_links(base_url, html)
            if debug:
                shared_console.print(f"\n[blue]Found links for {base_url}:[/blue]")
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup.find_all("a"):
                    href = tag.get("href")
                    if href:
                        href = href.strip(' "\'')
                        absolute = urljoin(base_url, href)
                        parsed = urlparse(absolute)
                        if parsed.scheme in ['http', 'https'] and parsed.netloc:
                            shared_console.print(
                                f"{'[green]✓[/green]' if absolute in links else '[red]✗[/red]'} "
                                f"{absolute} "
                                f"(netloc: {parsed.netloc}, normalized: {normalize_domain(parsed.netloc)}, path: {parsed.path})"
                            )
            return links

    crawler = DebugCrawler(
        seed_url=seed_url,
        base_domain=base_domain,
        max_urls=max_urls,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Crawling website...", total=None)
        try:
            sitemap = await crawler.crawl()
        except Exception as e:
            shared_console.print(f"[red]Error during crawl:[/red] {str(e)}")
            return

    if not sitemap:
        shared_console.print("[yellow]Warning:[/yellow] No pages were crawled. Check if the URL and domain are correct.")
        return

    # Process each URL in the sitemap
    shared_console.print(f"\nProcessing {len(sitemap)} pages...")
    for url, data in sitemap.items():
        markdown_content = data.get('markdown', '')
        if not markdown_content:
            shared_console.print(f"[yellow]Warning:[/yellow] No content for {url}")
            continue
        
        try:
            file_path = determine_file_path(url, crawler.seed_path, output_dir_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            shared_console.print(f"[green]✓[/green] Saved: {file_path.relative_to(output_dir_path)}")
        except Exception as e:
            shared_console.print(f"[red]Error saving {url}:[/red] {str(e)}")

    # Concatenate all markdown content for llms.txt
    all_content = []
    for url, data in sitemap.items():
        markdown_content = data.get('markdown', '')
        if markdown_content:
            all_content.append(markdown_content)

    if all_content:
        concatenated = '\n\n'.join(all_content)
        llms_path = output_dir_path / 'llms.txt'
        try:
            with open(llms_path, 'w', encoding='utf-8') as f:
                f.write(concatenated)
            shared_console.print(f"[green]✓[/green] Created llms.txt with {len(all_content)} content chunks")
        except Exception as e:
            shared_console.print(f"[red]Error writing llms.txt:[/red] {str(e)}")
    else:
        shared_console.print("[yellow]Warning:[/yellow] No content available to write to llms.txt")

    shared_console.print(f"\n[bold green]Done![/bold green] Documentation saved to {output_dir_path}") 