import cohere
from cohere.types.rerank_response import RerankResponseResultsItem, RerankResponse
from ai_kit.core.llms.client import Client
from typing import TypedDict, List, Dict, Optional
from ai_kit.utils.chunker import TokenCounter, Chunkers


class RerankCompletionResult(TypedDict):
    """Result from reranking."""

    index: int
    relevance_score: float
    document: str
    metadata: Dict[str, str]
    original_index: int # Index in original document list

class CohereClient(Client):
    def __init__(self, model: str):
        self.model = model
        self.mapped_model = self._get_model_name(self.model)
        self.max_tokens_per_document = 4096
        self.token_counter = TokenCounter()
        self.client = cohere.ClientV2()

    def _get_model_name(self, model: str) -> str:
        return model

    async def rerank_completion(
        self,
        query: str,
        documents: List[dict],  # Now expects dicts with "text" and "metadata"
        top_n: int = 10,
        autochunk: bool = True,
    ) -> List[RerankCompletionResult]:

        processed_documents = []
        for original_index, doc in enumerate(documents):
            text = doc["text"]
            metadata = doc["metadata"]

            if self.token_counter.count_tokens(text) > self.max_tokens_per_document:
                if autochunk:
                    # Chunk the large document into smaller segments using token-based chunking.
                    chunks = Chunkers.sliding_window_chunker_by_tokens(
                        text=text,
                        chunk_size=self.max_tokens_per_document,
                        overlap=200,
                        model=self.token_counter.model,
                    )
                    processed_documents.extend(
                        {
                            "chunk": chunk,
                            "metadata": metadata,
                            "original_index": original_index,
                        }
                        for chunk in chunks
                    )
                else:
                    raise Exception("Document is too large and autochunk is disabled.")
            else:
                processed_documents.append(
                    {
                        "chunk": text,
                        "metadata": metadata,
                        "original_index": original_index,
                    }
                )

        response: RerankResponse = self.client.rerank(
            model=self.mapped_model,
            query=query,
            documents=[
                doc["chunk"] for doc in processed_documents
            ],  # pass just the text chunks
            top_n=top_n,
        )

        if not response.results or len(response.results) == 0:
            raise Exception("No results found")

        # Combine rerank results with metadata
        final_results = []
        for result in response.results:
            output_result = {}
            processed_doc = processed_documents[result.index]
            output_result["original_index"] = processed_doc["original_index"]
            output_result["document"] = processed_doc["chunk"]
            output_result["metadata"] = processed_doc["metadata"]
            output_result["relevance_score"] = result.relevance_score
            output_result["index"] = result.index
            final_results.append(RerankCompletionResult(**output_result))

        sorted_results: List[RerankCompletionResult] = sorted(
            final_results,
            key=lambda r: r["relevance_score"],  # sort by relevance score
            reverse=True,  # in descending order
        )
        return sorted_results
