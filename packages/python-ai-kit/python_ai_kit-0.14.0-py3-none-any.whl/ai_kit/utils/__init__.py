from typing import Dict, Any, AsyncIterable, Iterable, AsyncIterator
import logging
import tiktoken
import re

logger = logging.getLogger(__name__)

# ! Parsing Utils ==============================
def get_text(chunk: Dict[str, Any]) -> str:
    """Get the text from a streaming chunk."""
    choices = chunk.get("choices")
    if not choices:
        logger.debug(f"No choices found in chunk: {chunk}")
        return ""
    if not isinstance(choices, list):
        logger.debug(f"Choices is not a list: {choices}")
        return ""
    
    delta = choices[0].get("delta")
    if not delta:
        logger.debug(f"No delta found in choices: {choices}")
        return ""

    return delta.get("content") or delta.get("reasoning_content")

def get_headers(chunk: Dict[str, Any]) -> Dict[str, Any]:
    """Get the response headers from a streaming chunk."""
    if (h:=chunk.get("_response_headers")): return h
    return {}

async def print_stream(chunks: AsyncIterable[Dict[str, Any]], buffer_size: int = 128) -> str:
    """
    Read text chunks from an async generator, print them to console as they arrive,
    and return the collected text.
    
    Args:
        chunks: Async iterable of chunks to process
        buffer_size: Size threshold for buffer before printing
        
    Returns:
        The complete text collected from all chunks
    """
    buffer = []  # We'll collect text pieces here
    current_size = 0
    output = ""

    async for chunk in chunks:
        text = get_text(chunk)
        if text:
            buffer.append(text)
            current_size += len(text)
            output += text
            # If we pass the threshold, print and reset
            if current_size >= buffer_size:
                print("".join(buffer), end="", flush=True)
                buffer = []
                current_size = 0

    if buffer:
        print("".join(buffer), end="", flush=True)

    return output

def print_stream_synchronous(chunks: Iterable[Dict[str, Any]], buffer_size: int = 128):
    """
    Read text chunks from an sync generator,
    accumulate them in a buffer, and print to console
    once the buffer reaches a certain size.
    """
    buffer = []  # We'll collect text pieces here
    current_size = 0

    for chunk in chunks:
        text = get_text(chunk)  # Uses your get_text function
        if text:
            buffer.append(text)
            current_size += len(text)

            # If we pass the threshold, print and reset
            if current_size >= buffer_size:
                print("".join(buffer), end="", flush=True)
                buffer = []
                current_size = 0

    # If there's anything left in the buffer, print it
    if buffer:
        print("".join(buffer), end="", flush=True)



def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count the number of tokens in a string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def truncate_to_tokens(text: str, max_tokens: int, encoding_name: str = "cl100k_base") -> str:
    """
    Truncate text to a maximum number of tokens.
    
    Args:
        text: The text to truncate
        max_tokens: Maximum number of tokens to keep
        encoding_name: The name of the tiktoken encoding to use
        
    Returns:
        The truncated text as a string
    """
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)[:max_tokens]
    return encoding.decode(tokens)

def strip_ansi(text):
    """Remove ANSI escape sequences from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
