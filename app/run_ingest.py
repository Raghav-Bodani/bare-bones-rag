from qdrant_client import models
from app.config import SOURCE, DOC_ID
from app.ingest import load_text
from app.chunk import chunk_text
from app.embed import embed_texts
from app.store import index_document  # store.py already calls setup_collection() on import




def main():
    text = load_text()
    chunks = chunk_text(text, doc_id=DOC_ID)

    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    points = []
    for c, v in zip(chunks, vectors):
        points.append(
            models.PointStruct(
                id=c["id"],
                vector=v,
                payload={
                    "text": c["text"],
                    "source": SOURCE,
                    "doc_id": DOC_ID,
                    "chunk_id": c["id"],
                },
            )
        )

    index_document(points)
    print(f"Stored {len(points)} chunks")

if __name__ == "__main__":
    main()