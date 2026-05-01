import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.ingest import load_text
from app.chunk import chunk_text
from app.embed import embed_texts
from app.store import search_with_scores

from app.generate import answer_query


app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    history: List[dict] = []

@app.get("/health")
def health():
    return {"STATUS": "OKAY"}

@app.get("/chunks")
def chunks():
    text = load_text()
    chunks = chunk_text(text, doc_id="employee_handbook_v1")
    return {
        "num_chunks": len(chunks),
        "sample": chunks[0]["text"][:200] if chunks else ""
    }

@app.get("/retrieve")
def retrieve(q: str):
    vector = embed_texts([q])[0]
    results = search_with_scores(vector, k=3)
    return{
        "query":q,
        "results":results
    }

@app.get("/search")
def search(q: str, k:int = 5):
    vector = embed_texts([q])[0]
    results = search_with_scores(vector, k=k)
    return {
        "query":q,
        "results":results
    }

@app.post("/answer") # Use POST so we can send the history list
def answer(request: QueryRequest):
    result = answer_query(request.query, request.history)
    return {
        "query": request.query,
        **result
    }



