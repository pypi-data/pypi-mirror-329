from together import AsyncTogether
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import re
from ai_kit.core.llms.client import Client

load_dotenv()
class TogetherClient(Client):
    def __init__(self, model: str):
        self.model = model
        self.temperature = 0

        # pass in api key to the client
        self.client = AsyncTogether(
            api_key=os.environ.get("TOGETHER_API_KEY"),
        )

    async def reasoning_completion(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        thoughts_only: bool = False,
    ):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=stream,
        )
        if not stream and thoughts_only:
            raise ValueError("thoughts_only is only supported for streaming responses")
        
        try:
            if stream:
                async def response_generator():
                    in_think_block = False
                    has_processed_think_block = False
                    async for chunk in response:
                        content = chunk.choices[0].delta.content
                        if content is None:
                            continue
                            
                        # Check for think tags
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
                        }

                return response_generator()

            # For non-streaming responses
            content = response.choices[0].message.content
            think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
            
            return {
                "choices": [
                    {
                        "message": {
                            "reasoning_content": think_match.group(1) if think_match else None,
                            "content": content.split('</think>')[-1] if think_match else content
                        }
                    }
                ]
            }

        except ValueError as e:
            raise e  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")