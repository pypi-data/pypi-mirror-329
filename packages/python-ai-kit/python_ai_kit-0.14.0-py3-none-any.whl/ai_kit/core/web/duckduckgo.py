from ai_kit.shared_console import shared_console
from duckduckgo_search import DDGS
from typing import TypedDict
class DuckDuckGoSearchResult(TypedDict):
    title: str
    href: str
    body: str

class DuckDuckGoSearch:
    def __init__(self):
        self.ddgs = DDGS()

    async def search(self, query: str, max_results: int = 5) -> list[dict]:
        return self.ddgs.text(query, max_results=max_results)

    @staticmethod
    def pprint(results: list[dict]):
        for result in results:
            shared_console.print(f"[bold green]{result['title']}[/bold green]")
            shared_console.print(f"[blue]{result['href']}[/blue]")
            # shared_console.print(result["body"])
            shared_console.print("\n")