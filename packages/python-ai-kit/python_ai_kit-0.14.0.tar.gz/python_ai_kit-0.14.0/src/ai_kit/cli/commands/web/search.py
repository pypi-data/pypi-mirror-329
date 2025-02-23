from typing import Dict, Any, List
from ai_kit.shared_console import shared_console
from ai_kit.core.llms.cohere_client import CohereClient, RerankCompletionResult
from ai_kit.core.web.duckduckgo import DuckDuckGoSearch
import os


async def search_web(
    query: str, rerank_query: str = None, max_results: int = 10
) -> list[Dict[str, Any]]:
    """Search the web for information."""

    with shared_console.status(
        "[bold cyan]Okay, I'm searching the web...[/bold cyan]"
    ) as status:
        ddgs = DuckDuckGoSearch()
        results = await ddgs.search(query, max_results)  # search

        status.update(f"[green]Found {len(results)} results[/green]")
        DuckDuckGoSearch.pprint(results)  # print the search results

        if not os.getenv("COHERE_API_KEY"):
            shared_console.print(
                "[bold red]Warning: COHERE_API_KEY is not set. Skipping reranking.[/bold red]"
            )
            return [
                {
                    "title": result["title"],
                    "url": result["href"],
                    "snippet": result["body"],
                }
                for result in results
            ]

        # 2. Find the most relevant pages
        status.update(f"[green]Reranking results...[/green]")
        reranker = CohereClient(model="rerank-v3.5")
        reranked_results: List[RerankCompletionResult] = (
            await reranker.rerank_completion(
                query,
                [
                    {
                        "text": result["body"],
                        "metadata": {
                            "title": result["title"],
                            "url": result["href"],
                        },
                    }
                    for result in results
                ],
            )
        )
        return [
            {
                "title": result["metadata"]["title"],
                "url": result["metadata"]["url"],
                "snippet": result["document"],
            }
            for result in reranked_results
        ]
