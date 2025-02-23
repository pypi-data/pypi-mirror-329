import tiktoken
from ai_kit.shared_console import shared_console

class TokenCounter:
    def __init__(self, model: str = None):
        self.model = model
        self.encoding = self.get_encoding()

    def get_encoding(self):
        if not self.model:
            return tiktoken.get_encoding("cl100k_base")
        try:
            return tiktoken.get_encoding(self.model)
        except Exception as e:
            shared_console.print(f"[red]Error getting encoding for model {self.model}: {e}. Defaulting to cl100k_base.[/red]")
            return tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))
    
    def encode(self, *args, **kwargs) -> list[int]:
        return self.encoding.encode(*args, **kwargs)
    
    def decode(self, *args, **kwargs) -> str:
        return self.encoding.decode(*args, **kwargs)
