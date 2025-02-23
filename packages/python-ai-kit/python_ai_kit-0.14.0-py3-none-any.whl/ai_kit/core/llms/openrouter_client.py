from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionChunk, ChatCompletion
import os
from pydantic import BaseModel
from typing import Union, AsyncIterator
import requests
from ai_kit.config.openrouter_config import OpenRouterConfig
from ai_kit.core.llms.client import Client

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set")


class OpenRouterClient(Client):
    def __init__(self, model: str):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        self.model = model
        self.model_config = OpenRouterConfig.get_model_config(model)

    async def chat_completion(
        self, messages: list[dict], stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:

        # Validate model type (is it a chat model?)
        OpenRouterConfig.validate_model_type(self.model, "chat")

        # Make the API call
        response: ChatCompletion | AsyncIterator[ChatCompletionChunk] = (
            await self.client.chat.completions.create(
                extra_headers={},
                model=self.model,
                messages=messages,
                stream=stream,
                extra_body=self.model_config,  # Inject model config
            )
        )
        if stream:

            async def stream_completion():
                async for chunk in response:
                    yield chunk.choices[0].delta.content

            return stream_completion()
        else:
            return response.choices[0].message.content

    async def reasoning_completion(
        self, messages: list[dict], stream: bool = False, thoughts_only: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        # Validate model type (is it a reasoning model?)
        OpenRouterConfig.validate_model_type(self.model, "reasoning")

        # Validate stream and thoughts_only
        if not stream and thoughts_only:
            raise ValueError("thoughts_only is only supported for streaming responses")

        # Make the API call
        response: ChatCompletion | AsyncIterator[ChatCompletionChunk] = (
            await self.client.chat.completions.create(
                extra_headers={},
                model=self.model,
                messages=messages,
                stream=stream,
                extra_body=self.model_config,
            )
        )
        if stream:

            async def response_generator():
                generation_id = None
                async for chunk in response:
                    if not generation_id:
                        generation_id = chunk.id
                    # If we're only asking for thoughts, and we've received a chunk with content and no reasoning, we're done thinking
                    if (
                        thoughts_only
                        and chunk.choices[0].delta.content != ""
                        and chunk.choices[0].delta.reasoning is None
                    ):
                        break
                    yield {
                        "choices": [
                            {
                                "delta": {
                                    "content": chunk.choices[0].delta.content,
                                    "reasoning_content": (
                                        chunk.choices[0].delta.reasoning
                                        if hasattr(chunk.choices[0].delta, "reasoning")
                                        else ""
                                    ),
                                }
                            }
                        ],
                    }

            return response_generator()
        else:
            return {
                "choices": [
                    {
                        "message": {
                            "content": response.choices[0].message.content,
                            "reasoning_content": (
                                response.choices[0].message.reasoning
                                if hasattr(response.choices[0].message, "reasoning")
                                else ""
                            ),
                        }
                    }
                ]
            }

    async def structured_output_completion(
        self, messages: list[dict], schema: BaseModel
    ) -> BaseModel:
        # Validate model type (is it a structured output model?)
        OpenRouterConfig.validate_model_type(self.model, "structured_output")

        # Make the API call
        completion = await self.client.beta.chat.completions.parse(
            extra_headers={},
            model=self.model,
            messages=messages,
            response_format=schema,
            extra_body=self.model_config,  # Inject model config
        )
        return completion.choices[0].message.parsed

    def list_models(self) -> list[str]:
        try:
            response = requests.get("https://openrouter.ai/api/v1/models")
            response.raise_for_status()
            json_response = response.json()
            return json_response.get("data", None)
        except Exception as e:
            raise Exception(f"Error listing models: {e}")

    def get_generation(self, id: int):
        response = requests.get(
            f"https://openrouter.ai/api/v1/generation?id={id}",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        )
        response.raise_for_status()
        return response.json()
