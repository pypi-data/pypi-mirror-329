from typing import Dict, Set, AsyncIterator
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from ai_kit.config.client_config import ClientFactory
from bs4 import BeautifulSoup, Tag, NavigableString

class HTMLToMarkdownParser:
    """Convert HTML to Markdown using BeautifulSoup."""
    def __init__(self, no_links: bool = False):
        self._no_links = no_links
        self._list_depth = 0

    def decompose_html(self, html: str) -> str:
        """Clean HTML by removing unnecessary elements while preserving main content."""
        soup = BeautifulSoup(html, 'html.parser')        
        TAGS_TO_REMOVE =  {
            'script',       # JavaScript
            'style',        # CSS
            'noscript',     # NoScript content
            'meta',         # Meta tags
            'link',         # Link tags
            'nav',          # Navigation
            'header',       # Header
        }
        for tag in TAGS_TO_REMOVE:
            for element in soup.find_all(tag):
                element.decompose()

        return str(soup)

    def process(self, html: str) -> str:
        main = self.decompose_html(html)
        return self._process_tag(BeautifulSoup(main, 'html.parser'))

    def _process_tag(self, element: Tag) -> str:
            """Process a BeautifulSoup tag and its children recursively."""
            if isinstance(element, NavigableString):
                # Replace multiple spaces with a single space and return stripped string
                return ' '.join(str(element).split())
            
            # Initialize result for string building
            result = []
            
            # Process different tag types
            tag_name = element.name if element.name else ''
            
            # Handle block elements
            if tag_name in ['p', 'div']:
                inner = self._process_children(element)
                if inner.strip():  # Only add newlines if there's content
                    result.append(f"{inner}\n")
            
            # Handle headings
            elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(tag_name[1])
                inner = self._process_children(element)
                result.append(f"\n{'#' * level} {inner}\n")
            
            # Handle links
            elif tag_name == 'a':
                href = element.get('href', '')
                inner = self._process_children(element)
                if self._no_links:
                    result.append(inner)  # Just the link text
                else:
                    result.append(f"[{inner}]({href})")  # Full markdown link
            
            # Handle images
            elif tag_name == 'img':
                alt = element.get('alt', '')
                src = element.get('src', '')
                result.append(f"![{alt}]({src})")
            
            # Handle lists
            elif tag_name in ['ul', 'ol']:
                self._list_depth += 1
                items = []
                for i, child in enumerate(element.find_all('li', recursive=False)):
                    prefix = '  ' * (self._list_depth - 1)
                    marker = '*' if tag_name == 'ul' else f"{i+1}."
                    items.append(f"{prefix}{marker} {self._process_children(child)}")
                self._list_depth -= 1
                result.append('\n' + '\n'.join(items) + '\n')
            
            # Handle emphasis
            elif tag_name in ['em', 'i']:
                inner = self._process_children(element)
                result.append(f"_{inner}_")
            
            # Handle strong/bold
            elif tag_name in ['strong', 'b']:
                inner = self._process_children(element)
                result.append(f"**{inner}**")
            
            # Handle code blocks
            elif tag_name == 'pre':
                code_element = element.find('code')
                if code_element:
                    # Get class names and look for potential language specification
                    classes = code_element.get('class', [])
                    language = ''
                    for class_name in classes:
                        # Common class naming patterns for code languages
                        if class_name.startswith(('language-', 'lang-')):
                            language = class_name.split('-')[1]
                            break
                        elif class_name in ['python', 'javascript', 'java', 'cpp', 'ruby', 'php', 'html', 'css']:
                            language = class_name
                            break
                    
                    inner = self._process_children(code_element)
                    result.append(f"\n```{language}\n{inner}\n```\n")
                else:
                    inner = self._process_children(element)
                    result.append(f"\n```\n{inner}\n```\n")
            
            # Handle inline code
            elif tag_name == 'code':
                inner = self._process_children(element)
                result.append(f"`{inner}`")
            
            # Handle horizontal rules
            elif tag_name == 'hr':
                result.append("\n---\n")
            
            # Handle line breaks
            elif tag_name == 'br':
                result.append("\n")
            
            # Handle blockquotes (added for better readability)
            elif tag_name == 'blockquote':
                inner = self._process_children(element)
                # Prepend each line with "> " to match Markdown blockquote style
                lines = inner.splitlines()
                blockquote_text = "\n".join(f"> {line}" for line in lines if line.strip())
                result.append(f"\n{blockquote_text}\n")
            
            # Default case: process children
            else:
                result.append(self._process_children(element))
            
            return ''.join(result)
        
    def _process_children(self, element: Tag) -> str:
        """Process all children of a tag."""
        return ''.join(self._process_tag(child) for child in element.children)

def html_to_markdown(html: str, no_links: bool = False) -> str:
    """Convert HTML to Markdown using BeautifulSoup."""
    parser = HTMLToMarkdownParser(no_links)
    return parser.process(html)


def extract_internal_links(html: str, base_url: str) -> Set[str]:
    """Extract all internal links from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    internal_links = set()
    base_domain = urlparse(base_url).netloc

    for a in soup.find_all('a', href=True):
        href = a['href']
        # Handle relative URLs
        if href.startswith('/'):
            full_url = urljoin(base_url, href)
            internal_links.add(full_url)
        else:
            # Check if the link is to the same domain
            parsed_href = urlparse(href)
            if parsed_href.netloc == base_domain or not parsed_href.netloc:
                if not parsed_href.netloc:  # Relative URL without leading slash
                    full_url = urljoin(base_url, href)
                else:
                    full_url = href
                internal_links.add(full_url)
    
    return internal_links


async def llm_html_to_markdown(html: str) -> AsyncIterator[Dict[str, str]]:
    """Clean the html using LLM to remove unnecessary content."""
    client = ClientFactory.get_client_by_model("gemini-2.0-flash")
    stream = await client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a content extraction expert focused on getting ONLY the main content. Rules:"
                "\n1. NEVER include ANY navigation elements, links, or menus"
                "\n2. NEVER include table of contents or lists of links"
                "\n3. NEVER include headers, footers, or sidebars"
                "\n4. NEVER include any UI elements or navigation paths"
                "\n5. Extract ONLY the actual content that teaches or informs"
                "\n6. Remove ALL supplementary elements and only keep core content"
                "\n7. Format the content in clean markdown"
                "\n8. If you see a list of links or a navigation menu, remove the ENTIRE section"
                "\n9. When in doubt, remove it - better to have less content than include navigation"
            },
            {
                "role": "user",
                "content": f"Extract ONLY the main content that teaches or informs. Remove ALL navigation, links, menus, and supplementary elements: {html}"
            }
        ],
        stream=True
    )
    return stream
