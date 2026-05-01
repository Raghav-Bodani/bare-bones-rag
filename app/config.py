# Chunking
CHUNK_SIZE = 500
OVERLAP = 100

# Embedding
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384  # must match EMBEDDING_MODEL's output dim

# Vector store
COLLECTION_NAME = "rigel_ai_docs_v1"
DISTANCE_METRIC = models.Distance.COSINE # convert to models.Distance.COSINE in store.py

# Ingest defaults
DOC_ID = "example_doc_v1"
SOURCE = "data/raw_docs"