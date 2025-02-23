from abc import ABC
from pydantic import BaseModel

class Client(ABC):
    def __init__(self, model: str):
        self.model = model

    def chat_completion(self, messages: list[dict], stream: bool = False, *args, **kwargs) -> str:
        pass

    def reasoning_completion(self, messages: list[dict], stream: bool = False, *args, **kwargs) -> str:
        pass

    def structured_output_completion(self, messages: list[dict], schema: BaseModel, stream: bool = False, *args, **kwargs) -> BaseModel:
        pass
