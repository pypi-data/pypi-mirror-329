from ai_kit.shared_console import shared_console
import aiohttp
import asyncio
from typing import TypedDict, Literal
from pypdf import PdfReader
import json
import io
from pypdf import PdfReader

def pdf_bytes_to_string(file_bytes: bytes) -> str:
    reader = PdfReader(file_bytes)
    return "\n".join([page.extract_text() for page in reader.pages])

class FetcherResult(TypedDict):
    type: Literal["text", "pdf", "json", "html", "error"]
    content: str

class Fetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _fetch_page(self, url: str) -> str:
        try:
            async with self.session.get(url, timeout=10) as response:
                response.raise_for_status()  # This will raise ClientResponseError
                # handle main content types
                content_type = response.headers.get("content-type").split(";")[0]
                # print("content_type", content_type) # ? debug
                if content_type == "application/pdf": 
                    buffer = io.BytesIO(await response.read())
                    return FetcherResult(type="pdf", content=pdf_bytes_to_string(buffer))
                elif content_type == "application/json":
                    return FetcherResult(type="json", content=json.dumps(await response.json()))
                elif content_type == "text/html":
                    return FetcherResult(type="html", content=await response.text())
                return FetcherResult(type="text", content=await response.text())
        # Erros go into results
        except aiohttp.ClientResponseError as e:
            return FetcherResult(type="error", content=str(e))
        except Exception as e:
            shared_console.print(f"[red]Error fetching page: {e}[/red]")
            return FetcherResult(type="error", content=str(e))
    
    async def batch_fetch(self, urls: list[str]) -> list[FetcherResult]:
        return await asyncio.gather(*[self._fetch_page(url) for url in urls])   