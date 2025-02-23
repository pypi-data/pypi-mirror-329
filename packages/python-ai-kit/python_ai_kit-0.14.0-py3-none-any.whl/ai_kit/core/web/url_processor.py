import re
from typing import Dict, AsyncIterator
import aiohttp
from ai_kit.core.web.fetcher import Fetcher
from ai_kit.core.web.parser import Parser
from ai_kit.utils.markdown_parser import html_to_markdown
from ai_kit.shared_console import shared_error_console


async def process_urls_in_prompt(prompt: str, raw: bool = False) -> str:
    """Process URLs in a prompt by fetching and replacing with cleaned content.
    
    Args:
        prompt: The input prompt containing URLs in {{ url:... }} format
        raw: If True, skips the Gemini cleaning step
        
    Returns:
        The prompt with {{ url:... }} placeholders replaced by their cleaned content
    """
    # Extract all URLs from the prompt using {{ url:... }} pattern
    url_pattern = re.compile(r'\{\{\s*url:([^}]+)\}\}')
    matches = url_pattern.finditer(prompt)
    urls_in_prompt = [(m.group(0), m.group(1).strip()) for m in matches]
    if not urls_in_prompt:
        return prompt  # No URLs to process
    
    # Deduplicate URLs while preserving order
    seen_urls = set()
    unique_urls = []
    url_map = {}  # Maps cleaned URL to original placeholder
    for placeholder, url in urls_in_prompt:
        if url not in seen_urls:
            seen_urls.add(url)
            unique_urls.append(url)
        url_map[url] = placeholder
    
    # Batch fetch all unique URLs
    url_to_content: Dict[str, str] = {}
    try:
        async with Fetcher() as fetcher:
            fetched_htmls = await fetcher.batch_fetch(unique_urls)
            
            # Process each fetched HTML into cleaned markdown
            parser = Parser()
            for url, html in zip(unique_urls, fetched_htmls):
                if not html:
                    shared_error_console.print(f"[red]Error: Could not fetch content from {url}[/red]")
                    continue
                
                try:
                    # Clean HTML
                    cleaned_html = await parser.clean_html(html)
                    # Convert to markdown
                    raw_md = html_to_markdown(cleaned_html, no_links=True)
                    
                    if not raw:
                        # Clean with Gemini
                        stream = await parser.clean_markdown(raw_md)
                        cleaned_md = await collect_stream(stream)
                    else:
                        cleaned_md = raw_md
                        
                    # Store with the original placeholder
                    placeholder = url_map[url]
                    url_to_content[placeholder] = cleaned_md
                except Exception as e:
                    shared_error_console.print(f"[red]Error processing {url}: {str(e)}[/red]")
                    continue
                    
    except aiohttp.ClientResponseError as e:
        if e.status == 403:
            shared_error_console.print(
                "[red]Error 403: Access Forbidden[/red]\n"
                "This usually means:\n"
                "1. The website is blocking automated access\n"
                "2. You might need authentication\n"
                "3. The website's robots.txt may be restricting access\n"
            )
        else:
            shared_error_console.print(f"[red]Error fetching URLs: {str(e)}[/red]")
        return prompt
    except Exception as e:
        shared_error_console.print(f"[red]Error: {str(e)}[/red]")
        return prompt
    
    # Replace URLs in the original prompt
    return replace_urls_in_prompt(prompt, url_to_content)


def replace_urls_in_prompt(prompt: str, url_to_content: Dict[str, str]) -> str:
    """Replace each {{ url:... }} placeholder with its cleaned content."""
    for placeholder, content in url_to_content.items():
        prompt = prompt.replace(placeholder, content)
    return prompt


async def collect_stream(stream: AsyncIterator[str]) -> str:
    """Collect an async stream into a string."""
    content = []
    async for chunk in stream:
        content.append(chunk)
    return ''.join(content) 