import os
from qdrant_client import QdrantClient, models
from app.config import COLLECTION_NAME, VECTOR_SIZE, DISTANCE_METRIC


client = QdrantClient(path="qdrant_data")

def setup_collection():
    if not client.collection_exists(COLLECTION_NAME):
        print(f"Creating Collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=DISTANCE_METRIC
            )
        )
        print("Collection Created and Locked.")
    else:
        info = client.get_collection(COLLECTION_NAME)
        params = info.config.params.vectors

        if params.size != VECTOR_SIZE or params.distance != DISTANCE_METRIC:
            raise RuntimeError(
                f"DB SCHEMA CORRUPTION DETECTED!\n"
                f"Collection: {COLLECTION_NAME}\n"
                f"Expected: Size={VECTOR_SIZE}, Distance={DISTANCE_METRIC}\n"
                f"Actual:   Size={params.size}, Distance={params.distance}\n"
                f"FIX: Delete the 'qdrant_data' folder to reset, or update your code."
            )
        pass

setup_collection()

def index_document(points: list[models.PointStruct]):
    if not points:
        return

    for p in points:
        if len(p.vector) != VECTOR_SIZE:
             raise ValueError(f"Vector dimension mismatch! Expected {VECTOR_SIZE}, got {len(p.vector)}")
        
        required_keys = {"text", "source", "doc_id", "chunk_id"}
        if not required_keys.issubset(p.payload.keys()):
             raise ValueError(f"Payload missing required keys: {required_keys - p.payload.keys()}")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def search_with_scores(vector: list[float], k: int = 5, score_threshold: float = 0.4):
    try:
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=k,
            with_payload=True,
            score_threshold=score_threshold
        )
        
        return [
            {
                "text": hit.payload.get("text", ""),
                "source": hit.payload.get("source", "unknown"),
                "score": hit.score
            } 
            for hit in results.points 
        ]
        
    except Exception as e:
        print(f"Database Error: {e}")
        return []







"""from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from uuid import uuid4

COLLECTION = "docs"
DIM = 384

client = QdrantClient(path="data/qdrant")

def init_store():
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
        )

def upsert_vectors(vectors, chunks):
    points =[]
    for v, text in zip(vectors, chunks):
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=v.tolist(),
                payload={"text": text},
            )
        )
        
    client.upsert(
        collection_name=COLLECTION,
        points=points,
    )

def search_with_scores(query_vector, k=5):
    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector, 
        limit=k,
        with_payload=True,
    )
    
    output = []
    for r in results.points:
        output.append({
            "text": r.payload.get("text", "No text found"),
            "score": r.score,
        })
    return output"""