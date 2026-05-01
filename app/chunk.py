import uuid
import tiktoken
from app.config import CHUNK_SIZE, OVERLAP

# Locked Constants: 
TOKENIZER = tiktoken.get_encoding("cl100k_base")

def normalize_text(text: str)-> str:
    # removes leading, trailing, and excessive internal whitespace from a string
    normalized_texts = " ".join(text.split())
    return normalized_texts

def chunk_text(text:str, doc_id:str):
    text = normalize_text(text)
    tokens = TOKENIZER.encode(text)

    chunks = []
    start = 0
    length = len(tokens)

    # Safety check: if text is empty, return empty list
    if length == 0:
        return []

    
    while start<length:
        end = start+ CHUNK_SIZE
        token_chunk = tokens[start:end]
        chunk_text = TOKENIZER.decode(token_chunk)

        chunk_id = str(uuid.uuid5(uuid.NAMESPACE_OID, doc_id + chunk_text))

        chunks.append({
            "id":chunk_id,
            "text" : chunk_text
        })

        start = end - OVERLAP
    
    return chunks

