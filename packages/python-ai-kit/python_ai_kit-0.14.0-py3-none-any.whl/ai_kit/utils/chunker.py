from ai_kit.utils.tokens import TokenCounter

class Chunkers:
    @staticmethod
    def sliding_window_chunker(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        if not text:
            return []
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            if end == len(text):
                break
            start = end - overlap
        return chunks

    @staticmethod
    def sliding_window_chunker_by_tokens(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
        model: str = None
    ) -> list[str]:
        """
        Splits the input text into chunks based on token counts rather than characters.
        This method encodes the text into tokens using the TokenCounter, then creates
        chunks containing `chunk_size` tokens, with `overlap` tokens overlapping between chunks.
        
        :param text: The input text to be chunked.
        :param chunk_size: The maximum number of tokens in each chunk.
        :param overlap: The number of tokens to overlap between consecutive chunks.
        :param model: (Optional) The model name to use for token encoding.
        :return: A list of text chunks.
        """
        if not text:
            return []
        
        token_counter = TokenCounter(model)
        tokens = token_counter.encode(text)
        
        # If the total token count is less than or equal to the chunk_size, return the full text.
        if len(tokens) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(tokens):
            end = start + chunk_size
            token_chunk = tokens[start:end]
            chunk_text = token_counter.decode(token_chunk)
            chunks.append(chunk_text)
            
            if end >= len(tokens):
                break
            
            start = end - overlap  # move back `overlap` tokens for overlapping chunks
        
        return chunks
        