from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_DIM, EMBEDDING_MODEL

_model = SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    try:
        vectors = _model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).tolist()

        if len(vectors) != len(texts):
            raise RuntimeError(f"Batch mismatch! Sent {len(texts)}, got {len(vectors)}")

        if len(vectors[0]) != EMBEDDING_DIM:
            raise RuntimeError(
                f"Dimension mismatch: expected {EMBEDDING_DIM}, got {len(vectors[0])}"
            )

        return vectors

    except Exception as e:
        raise RuntimeError(f"Embedding failed: {e}")
