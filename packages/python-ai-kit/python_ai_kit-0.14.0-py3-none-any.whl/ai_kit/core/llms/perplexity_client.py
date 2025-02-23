import os
from openai import AsyncOpenAI
from typing import List, Dict, Any, Set
import re
from ai_kit.core.llms.client import Client

class PerplexityClient(Client):
    def __init__(self, model: str):
        self.model = model
        self.temperature = 0
        # Initialize OpenAI client with Perplexity base URL
        self.client = AsyncOpenAI(
            api_key=os.environ.get("PERPLEXITY_API_KEY"),
            base_url="https://api.perplexity.ai"
        )


    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
    ):
        """Basic chat completion without think tags processing."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=stream,
            )

            if stream:
                async def response_generator():
                    all_citations: Set[str] = set()
                    async for chunk in response:
                        content = chunk.choices[0].delta.content
                        # Get citations from each chunk and add to total set
                        chunk_citations = getattr(chunk, 'citations', None)
                        if chunk_citations:
                            all_citations.update(chunk_citations)
                            
                        # Check if this is the last chunk (no content and finish_reason is set)
                        is_last_chunk = (content is None and getattr(chunk.choices[0], 'finish_reason', None) is not None)
                        
                        if content is not None or is_last_chunk:
                            yield {
                                "choices": [
                                    {
                                        "delta": {
                                            "content": content if content is not None else ""
                                        }
                                    }
                                ],
                                # For regular chunks, pass their citations. For final chunk, pass all accumulated citations
                                "citations": list(all_citations) if is_last_chunk else chunk_citations
                            }
                return response_generator()

            return {
                "choices": [
                    {
                        "message": {
                            "content": response.choices[0].message.content
                        }
                    }
                ],
                "citations": getattr(response, 'citations', None)
            }

        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")

    async def reasoning_completion(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        thoughts_only: bool = False,
    ):
        """Chat completion with think tags processing for reasoning."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=stream,
            )

            if not stream and thoughts_only:
                raise ValueError("thoughts_only is only supported for streaming responses")

            if stream:
                async def response_generator():
                    in_think_block = False
                    has_processed_think_block = False
                    all_citations: Set[str] = set()
                    
                    async for chunk in response:
                        content = chunk.choices[0].delta.content
                        # Get citations from each chunk and add to total set
                        chunk_citations = getattr(chunk, 'citations', None)
                        if chunk_citations:
                            all_citations.update(chunk_citations)
                            
                        # Check if this is the last chunk
                        is_last_chunk = (content is None and getattr(chunk.choices[0], 'finish_reason', None) is not None)
                        
                        if content is None and not is_last_chunk:
                            continue

                        # Check for think tags
                        if content is not None:
                            if "<think>" in content:
                                in_think_block = True
                                content = content.replace("<think>", "")
                            if "</think>" in content:
                                in_think_block = False
                                has_processed_think_block = True
                                if thoughts_only:
                                    break
                                content = content.replace("</think>", "")

                            # If thoughts_only and we're not in a think block, skip
                            if thoughts_only and has_processed_think_block:
                                continue

                        yield {
                            "choices": [
                                {
                                    "delta": {
                                        "content": content if not in_think_block else "",
                                        "reasoning_content": content if in_think_block else ""
                                    }
                                }
                            ],
                            # For regular chunks, pass their citations. For final chunk, pass all accumulated citations
                            "citations": list(all_citations) if is_last_chunk else chunk_citations
                        }

                return response_generator()

            # For non-streaming responses
            content = response.choices[0].message.content
            citations = getattr(response, 'citations', None)
            think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)

            return {
                "choices": [
                    {
                        "message": {
                            "reasoning_content": think_match.group(1) if think_match else None,
                            "content": content.split('</think>')[-1] if think_match else content
                        }
                    }
                ],
                "citations": citations
            }

        except ValueError as e:
            raise e  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")
