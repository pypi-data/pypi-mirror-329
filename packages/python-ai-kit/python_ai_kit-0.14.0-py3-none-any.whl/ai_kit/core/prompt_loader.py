import re
import asyncio
from dataclasses import dataclass
from typing import Dict, AsyncIterator, List, Tuple, Set
import aiohttp
from pathlib import Path
from ai_kit.core.web.fetcher import Fetcher, FetcherResult
from ai_kit.core.web.parser import html_to_markdown
from ai_kit.shared_console import shared_error_console, shared_console
from ai_kit.utils.fs import WorkspaceError, join_workspace_path
from ai_kit.utils.dynamic_file_loader import DynamicFileLoader
from ai_kit.utils import get_text

@dataclass
class Reference:
    """A reference to content that needs to be loaded."""
    placeholder: str  # The full {{ ... }} text
    content_id: str   # The unique identifier for this content (file path or URL)
    is_url: bool     # Whether this is a URL reference
    index: int       # Original position in the prompt


class PromptLoader:
    """A class that handles loading and replacing both file and URL references in prompts."""

    def __init__(self):
        self.file_loader = DynamicFileLoader()
        self.url_pattern = re.compile(r'\{\{\s*url:([^}]+)\}\}')
        self.file_pattern = re.compile(r'\{\{(.+?)\}\}')

    async def load(self, prompt: str, raw: bool = False, append_content: bool = True) -> str:
        """Load and replace both file and URL references in a prompt.
        
        Args:
            prompt: The input prompt containing {{ file }} and {{ url:... }} references
            raw: If True, skips the Gemini cleaning step for URLs
            append_content: If True, appends loaded content at the end instead of inline replacement
            
        Returns:
            The prompt with all references processed, or original prompt if all references fail
        """
        # Extract all references first
        shared_console.print("[blue]Processing prompt...[/blue]")
        references = self._extract_references(prompt)
        if not references:
            return prompt

        shared_console.print("[blue]Loading content from references...[/blue]")
        # Load all content in parallel
        content_map = await self._load_all_content(references, raw)
        
        # Only process references that were successfully loaded
        valid_refs = [ref for ref in references if ref.placeholder in content_map]
        
        if not valid_refs:
            shared_error_console.print("[red]No content could be loaded, returning original prompt[/red]")
            return prompt
            
        if append_content:
            # Replace references with numbered markers and append content
            shared_console.print("[blue]Appending content...[/blue]")
            return self._append_content(prompt, valid_refs, content_map)
        else:
            # Replace references inline
            shared_console.print("[blue]Replacing inline...[/blue]")
            return self._replace_inline(prompt, content_map)

    def _extract_references(self, text: str) -> List[Reference]:
        """Extract all file and URL references from the text."""
        references = []
        
        # Find URL references
        for match in self.url_pattern.finditer(text):
            references.append(Reference(
                placeholder=match.group(0),
                content_id=match.group(1).strip(),
                is_url=True,
                index=match.start()
            ))
        
        # Find file references (excluding URL references)
        for match in self.file_pattern.finditer(text):
            content = match.group(1).strip()
            if not content.startswith('url:'):
                references.append(Reference(
                    placeholder=match.group(0),
                    content_id=content,
                    is_url=False,
                    index=match.start()
                ))
        
        # Sort by original position
        references.sort(key=lambda r: r.index)
        return references

    async def _load_all_content(self, references: List[Reference], raw: bool) -> Dict[str, str]:
        """Load all content in parallel."""
        content_map = {}
        
        # Group references by type
        url_refs = [ref for ref in references if ref.is_url]
        file_refs = [ref for ref in references if not ref.is_url]
        
        # Load files and URLs in parallel
        results = await asyncio.gather(
            self._load_files(file_refs),
            self._load_urls(url_refs, raw),
            return_exceptions=True
        )
        
        # Combine results
        for result in results:
            if isinstance(result, dict):
                content_map.update(result)
            elif isinstance(result, Exception):
                shared_error_console.print(f"[red]Error loading content: {str(result)}[/red]")
        
        return content_map

    async def _load_files(self, references: List[Reference]) -> Dict[str, str]:
        """Load all file references."""
        content_map = {}
        for ref in references:
            try:
                full_path = join_workspace_path(ref.content_id)
                if full_path.is_dir():
                    # For directories, process all allowed files recursively
                    contents = []
                    workspace_root = join_workspace_path()
                    for child_path in full_path.rglob("*"):
                        if child_path.is_file():
                            try:
                                if self.file_loader.is_file_allowed(str(child_path)):
                                    child_rel_path = child_path.relative_to(workspace_root)
                                    content = self.file_loader.load_file_content(str(child_path))
                                    contents.append(
                                        f"\n=== Content of {child_rel_path} ===\n{content}\n=== End of {child_rel_path} ===\n"
                                    )
                            except ValueError:
                                shared_error_console.print(f"[red]Skipping {child_path}: File type not allowed[/red]")
                                continue
                    if contents:  # Only add if we found valid files
                        content_map[ref.placeholder] = "".join(contents)
                    else:
                        shared_error_console.print(f"[red]No valid files found in directory: {ref.content_id}[/red]")
                else:
                    # For single files, load directly if allowed
                    content = self.file_loader.load_file_content(str(full_path))
                    content_map[ref.placeholder] = f"\n=== Content of {ref.content_id} ===\n{content}\n=== End of {ref.content_id} ===\n"
            except (WorkspaceError, ValueError, Exception) as e:
                shared_error_console.print(f"[red]Error loading {ref.content_id}: {str(e)}[/red]")
                continue
        
        return content_map

    async def _load_urls(self, references: List[Reference], raw: bool) -> Dict[str, str]:
        """Load all URL references."""
        if not references:
            return {}

        content_map = {}
        try:
            # Deduplicate URLs while preserving mapping to original placeholders
            unique_urls = []
            url_to_refs: Dict[str, List[Reference]] = {}
            for ref in references:
                # Skip non-HTML URLs
                if ref.content_id not in url_to_refs:
                    unique_urls.append(ref.content_id)
                    url_to_refs[ref.content_id] = []
                url_to_refs[ref.content_id].append(ref)

            if not unique_urls:
                return {}

            # ! ARXIV HACK
            for url in unique_urls:
                if "arxiv.org/abs" in url:
                    unique_urls.remove(url)
                    unique_urls.append(url.replace("arxiv.org/abs", "arxiv.org/pdf"))
                    shared_console.print(f"[yellow]HACK: Replacing abstract URL with PDF URL: {url} -> {unique_urls[-1]}[/yellow]")


            async with Fetcher() as fetcher:
                fetched_results: list[FetcherResult] = await fetcher.batch_fetch(unique_urls)
                
                # Process each fetched HTML
                for url, result in zip(unique_urls, fetched_results):
                    if result["type"] == "error":
                        shared_error_console.print(f"[red]Error: Could not fetch content from {url}[/red]")
                        continue
                    
                    try:
                        if result["type"] == "html":
                            to_display = html_to_markdown(result["content"], no_links=True)
                            to_display = to_display.replace("\n\n", "\n")
                        else: # pdf, json, text, etx.
                            to_display = result["content"]
                        
                        # Store for all references to this URL
                        for ref in url_to_refs[url]:
                            content_map[ref.placeholder] = to_display
                    except Exception as e:
                        shared_error_console.print(f"[red]Error processing {url}: {str(e)}[/red]")
                        continue
                        
        except aiohttp.ClientResponseError as e:
            shared_error_console.print(f"[red]Error ({e.status}): Unable to fetch URL: {e.request_info.url}[/red]")
        except Exception as e:
            shared_error_console.print(f"[red]Error: {str(e)}[/red]")
        
        return content_map

    def _append_content(self, prompt: str, references: List[Reference], content_map: Dict[str, str]) -> str:
        """Replace references with markers and append content at the end."""
        result = prompt
        appendix = ["\n\n=== Referenced Content ===\n"]
        
        for i, ref in enumerate(references, 1):
            if ref.placeholder in content_map:
                marker = f"[REF_{i}]"
                result = result.replace(ref.placeholder, marker)
                content = content_map[ref.placeholder]
                appendix.append(f"\n[REF_{i}]:\n{content}\n")
        
        return result + "".join(appendix)

    def _replace_inline(self, prompt: str, content_map: Dict[str, str]) -> str:
        """Replace references inline with their content."""
        result = prompt
        for placeholder, content in content_map.items():
            result = result.replace(placeholder, content)
        return result

    async def _collect_stream(self, stream: AsyncIterator[str]) -> str:
        """Collect an async stream into a string."""
        content = []
        async for chunk in stream:
            if text := get_text(chunk):
                content.append(text)
        return "".join(content) 