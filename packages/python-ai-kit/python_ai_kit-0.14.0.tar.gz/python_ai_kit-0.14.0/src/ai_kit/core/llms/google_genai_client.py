from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from ai_kit.core.llms.client import Client
from typing import List, Dict, Any, AsyncIterator, AsyncGenerator, Union
from pydantic import BaseModel

load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

def _get_user_message(messages: List[Dict[str, Any]]) -> str:
    user_message = ""
    for message in messages:
        if message["role"] == "user":
            user_message += message["content"] + "\n"
    return user_message.strip() if user_message else None

def _get_system_message(messages: List[Dict[str, Any]]) -> str:
    system_message = ""
    for message in messages:
        if message["role"] == "system":
            system_message += message["content"] + "\n"
    return system_message.strip() if system_message else None

class GoogleGenAIClient(Client):
    def __init__(self, model: str):
        self.model = model
        self.client = genai.Client(
            api_key=GEMINI_API_KEY, http_options={"api_version": "v1alpha"}
        )
        self.max_tokens = 4096
        self.temperature = 0

    async def chat_completion(
        self, messages: List[Dict[str, str]], stream: bool = False, **kwargs
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        """Get a chat completion from the model."""
        system_instruction=_get_system_message(messages)
        model_config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        try:
            if stream:
                response = self.client.models.generate_content_stream(
                    model=self.model,
                    contents=_get_user_message(messages),
                    config=model_config,
                )

                async def response_generator():
                    for chunk in response:
                        if not chunk.candidates:
                            continue

                        for part in chunk.candidates[0].content.parts:
                            yield {
                                "choices": [
                                    {
                                        "delta": {"content": part.text},
                                    }
                                ]
                            }

                return response_generator()
            else:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=_get_user_message(messages),
                    config=model_config,
                )
                return {
                    "choices": [
                        {
                            "message": {
                                "content": response.candidates[0].content.parts[0].text
                            },
                        }
                    ]
                }
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")

    async def reasoning_completion(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        thoughts_only: bool = False,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        if not stream and thoughts_only:
            raise ValueError("thoughts_only is only supported for streaming responses")
        try:
            if stream:
                response = self.client.models.generate_content_stream(
                    model=self.model,
                    contents=_get_user_message(messages),
                    config={"thinking_config": {"include_thoughts": True}},
                )

                async def response_generator():
                    for chunk in response:
                        if not chunk.candidates:
                            continue

                        for part in chunk.candidates[0].content.parts:
                            print("Part.thought: ", part.thought)
                            if thoughts_only and part.thought == None:
                                return

                            yield {
                                "choices": [
                                    {
                                        "delta": {
                                            "content": (
                                                part.text if not part.thought else ""
                                            ),
                                            "reasoning_content": (
                                                part.text if part.thought else ""
                                            ),
                                        }
                                    }
                                ]
                            }

                return response_generator()
            else:
                # For non-streaming responses
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=_get_user_message(messages),
                    config={"thinking_config": {"include_thoughts": True}},
                )

                content = ""
                reasoning_content = ""

                # Process all parts to separate thoughts from content
                for part in response.candidates[0].content.parts:
                    if part.thought:
                        reasoning_content += part.text
                    else:
                        content += part.text

                return {
                    "choices": [
                        {
                            "message": {
                                "content": content,
                                "reasoning_content": reasoning_content,
                            }
                        }
                    ]
                }

        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")


    def structured_output_completion(
        self,
        messages: List[Dict[str, Any]],
        schema: BaseModel,
    ) -> BaseModel:
        system_instruction=_get_system_message(messages)
        model_config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=self.max_tokens,
            temperature=self.temperature,
            response_mime_type="application/json",
            response_schema=schema,
        )
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=_get_user_message(messages),
            config=model_config,
        )
        
        return schema.model_validate_json(response.candidates[0].content.parts[0].text)
        
        
