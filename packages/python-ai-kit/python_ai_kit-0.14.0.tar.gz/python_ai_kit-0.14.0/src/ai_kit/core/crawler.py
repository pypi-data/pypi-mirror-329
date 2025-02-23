import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup  # Make sure to install beautifulsoup4 via pip
import markdownify
from ai_kit.shared_console import shared_console

def normalize_domain(domain: str) -> str:
    """Remove www. prefix and any trailing dots from domain."""
    return domain.lower().replace('www.', '').rstrip('.')

class Crawler:
    def __init__(self, seed_url, base_domain, max_workers=10, max_urls=100, throttle_limit=5, max_retries=2, max_levels_up=1):
        """
        Initialize the crawler with the seed URL, base domain, number of worker tasks,
        the maximum number of URLs to crawl, the concurrency throttling limit,
        and the maximum retries for failed HTTP requests.

        - seed_url: Starting URL for the crawl.
        - base_domain: Domain to restrict to (no path, just domain).
        - max_workers: Number of concurrent worker tasks.
        - max_urls: Maximum number of pages/URLs to crawl.
        - throttle_limit: Maximum number of concurrent HTTP fetches.
        - max_retries: Maximum number of retry attempts for a failed request.
        - max_levels_up: Maximum number of directory levels to crawl up from seed path (default: 1).
                        For example, if seed is /a/b/c and max_levels_up=1, it will crawl /a/b/* but not /a/*.
        """
        # Extract just the domain part, ignoring any path
        if "://" in base_domain:
            base_domain = urlparse(base_domain).netloc
        self.base_domain = normalize_domain(base_domain)
        
        # Parse and normalize the seed URL
        seed_parsed = urlparse(seed_url)
        normalized_domain = normalize_domain(seed_parsed.netloc)
        self.seed_url = seed_parsed._replace(netloc=normalized_domain).geturl()
        
        # Store the seed path, ensuring it starts with / and has no trailing slash
        self.seed_path = seed_parsed.path.rstrip('/') or '/'
        
        self.max_workers = max_workers
        self.max_urls = max_urls
        self.max_retries = max_retries
        self.max_levels_up = max_levels_up
        self.visited = set()
        self.queue = asyncio.Queue()
        self.sitemap = {}  # {url: {"url": url, "html": html, "children": [child_url, ...]}}

        # Semaphore to throttle concurrent HTTP requests.
        self.semaphore = asyncio.Semaphore(throttle_limit)
    
    def get_path_level(self, path: str) -> int:
        """Get the directory level (depth) of a path."""
        # Remove leading/trailing slashes and split
        parts = [p for p in path.split('/') if p]
        return len(parts)

    def is_path_allowed(self, path: str) -> bool:
        """
        Check if a path is allowed based on the seed path and max_levels_up.
        A path is allowed if it:
        1. Is the seed path itself
        2. Is a parent of the seed path (within max_levels_up)
        3. Is a child of the seed path
        4. Is a sibling of any ancestor (within max_levels_up)
        
        For example, if seed_path is /a/b/c and max_levels_up=1:
        - /a/b/c (exact match) ✓
        - /a/b (parent, level 1) ✓
        - /a (parent, level 2) ✗
        - /a/b/c/d (child) ✓
        - /a/b/d (sibling, level 1) ✓
        - /a/d (sibling, level 2) ✗
        - /d (outside) ✗
        """
        # Normalize paths for comparison
        path = path.rstrip('/')
        seed_path = self.seed_path.rstrip('/')
        
        # Always allow the seed path itself
        if path == seed_path:
            return True
        
        # Split paths into parts, removing empty strings
        path_parts = [p for p in path.split('/') if p]
        seed_parts = [p for p in self.seed_path.split('/') if p]
        
        seed_level = len(seed_parts)
        path_level = len(path_parts)
        
        # Check if this is a parent of the seed path
        if seed_path.startswith(path + '/'):
            # Calculate how many levels up this path is
            levels_up = seed_level - path_level
            return levels_up <= self.max_levels_up
        
        # Check if this is a child of the seed path
        if path.startswith(seed_path + '/'):
            return True
        
        # Check if this is a sibling of any ancestor within max_levels_up
        # Start from immediate parent (1 level up) to max_levels_up
        for levels_up in range(1, min(self.max_levels_up + 1, seed_level + 1)):
            ancestor_parts = seed_parts[:-levels_up]
            ancestor = '/' + '/'.join(ancestor_parts)
            if path.startswith(ancestor + '/'):
                # Verify this path isn't going deeper than the original seed level
                # This prevents crawling deep paths in sibling directories
                if path_level <= seed_level:
                    return True
        
        return False

    async def fetch(self, session, url):
        """Fetch the HTML content of the URL asynchronously with retry mechanism and throttling."""
        for attempt in range(self.max_retries + 1):  # Changed to max_retries + 1 to include initial attempt
            try:
                async with self.semaphore:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            print(f"Non-200 status code {response.status} for URL: {url}")
            except Exception as e:
                print(f"Error fetching {url}: {e} (attempt {attempt + 1}/{self.max_retries + 1})")
            if attempt < self.max_retries:  # Only sleep if we're going to retry
                await asyncio.sleep(1)  # brief delay before retrying
        return None

    def extract_links(self, base_url, html):
        """
        Extract all href links from <a> tags in the HTML that belong to the same base domain
        and have an allowed path based on the seed path.
        """
        links = set()
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all("a"):
            href = tag.get("href")
            if not href:
                continue
            
            # Clean up the href and convert to absolute URL
            href = href.strip(' "\'')
            absolute = urljoin(base_url, href)
            parsed = urlparse(absolute)
            
            # Only process http(s) URLs
            if parsed.scheme not in ['http', 'https'] or not parsed.netloc:
                continue
            
            # Check domain matches
            normalized_domain = normalize_domain(parsed.netloc)
            if normalized_domain != self.base_domain:
                continue
            
            # Check if the path is allowed
            if self.is_path_allowed(parsed.path):
                # Remove fragment identifiers and normalize
                normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
                links.add(normalized)
            
        return links

    async def worker(self, name, session):
        """Worker task that continuously processes URLs from the queue."""
        while True:
            url = await self.queue.get()
            # If we've reached the maximum URLs limit, skip processing further.
            if len(self.visited) >= self.max_urls:
                self.queue.task_done()
                continue

            if url in self.visited:
                self.queue.task_done()
                continue

            print(f"{name} crawling: {url}")
            self.visited.add(url)
            html = await self.fetch(session, url)
            if html:
                # Save the page info in the sitemap.
                self.sitemap[url] = {
                    "url": url,
                    "html": html,
                    "children": [],
                    "markdown": self.parse(html),
                }
                links = self.extract_links(url, html)
                for link in links:
                    # Update the children list for the current page.
                    if link not in self.sitemap[url]["children"]:
                        self.sitemap[url]["children"].append(link)
                    # Enqueue the child page if not visited and within the max_urls limit.
                    if link not in self.visited and len(self.visited) < self.max_urls:
                        await self.queue.put(link)
            self.queue.task_done()

    async def crawl(self):
        """
        Start the asynchronous crawling process.
        
        It enqueues the seed URL, starts the worker tasks, waits until the queue is empty,
        cancels the worker tasks and returns the sitemap object containing each page's URL,
        HTML content, and its child links.
        """
        await self.queue.put(self.seed_url)
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(self.worker(f"Worker-{i}", session))
                for i in range(self.max_workers)
            ]
            await self.queue.join()    
            for task in tasks:
                task.cancel()
        return self.sitemap
    
    def parse(self, html: str) -> str:
        if not html:
            return ""
        markdown = markdownify.markdownify(
            html,
            strip=["footer", "header", "a", "svg"],
            bullets="*",
        )
        return markdown.replace("\n\n", "").strip()
    
    def pretty_print_sitemap(self, current_url=None, indent=0, visited=None):
        """
        Recursively prints the sitemap starting from the current_url.
        If current_url is None, it starts from the seed URL.
        This function will show each URL along with a snippet of its HTML content.
        """
        if visited is None:
            visited = set()
        if current_url is None:
            current_url = self.seed_url
        if current_url in visited:
            return
        visited.add(current_url)
        node = self.sitemap.get(current_url)
        if not node:
            return
        indent_str = " " * indent
        # Print the URL and a snippet of HTML (first 100 characters).
        shared_console.print(f"[bold blue]URL: {node['url']}[/bold blue]")
        html_snippet = node['html'][:100].replace("\n", " ") if node['html'] else ""
        shared_console.print(f"[yellow]HTML: {html_snippet}...[/yellow]")
        shared_console.print("\n")
        # Recursively print the children.
        for child in node["children"]:
            self.pretty_print_sitemap(child, indent=indent + 2, visited=visited)
