import os
import mimetypes
from pypdf import PdfReader
from typing import Optional, Callable, Dict, List, Set
from pathlib import Path

try:
    import magic
except ImportError:
    magic = None

# Default configuration - can be overridden via config file
DEFAULT_ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".py", ".js", ".ts", ".json", ".yaml", ".yml"}
DEFAULT_ALLOWED_MIME_TYPES = {
    "text/plain", 
    "text/markdown",
    "application/pdf",
    "text/x-python",
    "application/javascript",
    "application/json",
    "text/yaml"
}

class DynamicFileLoader:
    def __init__(self):
        self.loader_registry: Dict[str, Callable] = {}
        self.extension_registry: Dict[str, Callable] = {}
        self.default_loader: Optional[Callable] = None
        
        # Configuration for allowed files
        self.allowed_extensions: Set[str] = DEFAULT_ALLOWED_EXTENSIONS.copy()
        self.allowed_mime_types: Set[str] = DEFAULT_ALLOWED_MIME_TYPES.copy()

        # Register default loaders
        self.register_loader(
            extensions=[".pdf"], mime_types=["application/pdf"], loader=self._load_pdf
        )
        self.register_loader(mime_types=["text/plain"], loader=self._load_text)
    
    def configure(self, allowed_extensions: Optional[List[str]] = None, allowed_mime_types: Optional[List[str]] = None):
        """Configure the file loader with allowed extensions and MIME types.
        
        Args:
            allowed_extensions: List of file extensions to allow (e.g. [".txt", ".md"])
            allowed_mime_types: List of MIME types to allow (e.g. ["text/plain"])
        """
        if allowed_extensions is not None:
            self.allowed_extensions = {ext.lower() for ext in allowed_extensions}
        if allowed_mime_types is not None:
            self.allowed_mime_types = {mime.lower() for mime in allowed_mime_types}

    def is_file_allowed(self, file_path: str) -> bool:
        """Check if a file is allowed to be loaded based on extension and MIME type."""
        ext = Path(file_path).suffix.lower()
        if ext in self.allowed_extensions:
            return True
            
        mime_type = self._get_mime_type(file_path)
        return mime_type in self.allowed_mime_types

    def register_loader(
        self,
        extensions: Optional[list] = None,
        mime_types: Optional[list] = None,
        loader: Optional[Callable] = None,
    ):
        if extensions:
            for ext in extensions:
                self.extension_registry[ext.lower()] = loader
        if mime_types:
            for mime in mime_types:
                self.loader_registry[mime.lower()] = loader

    def load_file_content(self, file_path: str) -> str:
        """Load file content if the file type is allowed."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not self.is_file_allowed(file_path):
            raise ValueError(f"File type not allowed: {file_path}")

        # Try extension-based loading first
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.extension_registry:
            return self.extension_registry[ext](file_path)

        # Fall back to MIME-type-based loading
        mime_type = self._get_mime_type(file_path)
        if mime_type in self.loader_registry:
            return self.loader_registry[mime_type](file_path)

        # Try default loader if set
        if self.default_loader:
            return self.default_loader(file_path)

        # If we get here, the file is allowed but we don't have a specific loader
        # Default to text loading
        return self._load_text(file_path)

    def _get_mime_type(self, file_path: str) -> str:
        # First try mimetypes based on extension
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            return mime_type.lower()

        # Fall back to magic for content-based detection
        if not magic:
            raise ImportError(
                "The 'python-magic' package is required for MIME type detection. "
                "Install with 'pip install python-magic'."
            )

        mime = magic.Magic(mime=True)
        with open(file_path, "rb") as f:
            file_content = f.read(2048)
            return mime.from_buffer(file_content).lower()

    def set_default_loader(self, loader: Callable):
        self.default_loader = loader

    @staticmethod
    def _load_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages])

    @staticmethod
    def _load_text(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()