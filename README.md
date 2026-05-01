# BareBones RAG

*A simple functional RAG built to better understand how the tech behind LLMs and RAGs works.*

## Why this exists

I built this to understand the RAG pipeline end to end by writing the smallest version that works. For the reasoning behind specific choices, what I deliberately left out, what I'd build next, and how I think. see [NOTES.md](NOTES.md).

## What it does

The system ingests `.txt` files, generates local vector embeddings, and stores them in a local Qdrant instance. An LLM can then be queried over these embeddings through a Streamlit frontend, answers are grounded in the ingested documents, not the model's parametric knowledge.

## Stack

- **Language:** Python 3.12
- **Embedding model:** `BAAI/bge-small-en-v1.5` (384-dim)
- **Tokenizer:** `tiktoken` (cl100k_base)
- **Vector store:** Qdrant (local)
- **LLM:** Groq — `llama-3.3-70b-versatile`
- **API layer:** FastAPI (served via uvicorn)
- **Frontend:** Streamlit

## How it works

1. **Ingest** — reads `.txt` files from `data/raw_docs/`
2. **Chunk** — splits text into fixed-size chunks (500 tokens, 100 overlap) using tiktoken
3. **Embed** — generates 384-dim vectors via BGE-small
4. **Store** — writes vectors and metadata to a local Qdrant collection
5. **Retrieve** — on query, embeds the question and pulls the top-k nearest chunks via cosine similarity
6. **Generate** — passes retrieved chunks as context to Groq's Llama 3.3 70B for a grounded answer

## Running it locally

**Prerequisites:** Python 3.12, a [Groq API key](https://console.groq.com).

1. **Clone and enter the repo**
```bash
   git clone https://github.com/Raghav-Bodani/bare-bones-rag.git
   cd bare-bones-rag
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
   Copy `.env.example` to `.env` and add your Groq API key:
```bash
   GROQ_API_KEY=your_key_here
```
5. **Ingest your documents**
   Drop any `.txt` file into `data/raw_docs/`, then run:
```bash
   python run_ingest.py
```

6. **Run the backend and frontend** (in two separate terminals)

   Terminal 1 — backend:
```bash
   uvicorn app.main:app --reload
```

   Terminal 2 — frontend:
```bash
   streamlit run app/frontend.py
```

7. Open the Streamlit URL in your browser and query your documents.

## Project structure
```bash
bare-bones-rag/
├── app/
│   ├── chunk.py         # Token-based chunking
│   ├── embed.py         # BGE-small embedding
│   ├── store.py         # Qdrant collection management
│   ├── ingest.py        # Ingestion pipeline
│   ├── generate.py      # Groq LLM call with retrieved context
│   ├── main.py          # FastAPI backend
│   └── frontend.py      # Streamlit UI
├── data/
│   └── raw_docs/        # Drop .txt files here
├── qdrant_data/         # Local Qdrant storage (gitignored)
├── run_ingest.py        # Entry point for ingestion
├── requirements.txt
└── .env.example
```
## Status & limitations

This is a deliberately minimal build. Known limitations:

- **`.txt` only.** No PDF, DOCX, HTML, or markdown ingestion.
- **Strict grounding.** The system prompt locks responses to retrieved context. It will not respond to general conversation — even "hello" gets a non-answer. This is intentional for the v0 scope.
- **No reranking.** Top-k retrieval by cosine similarity, no second-stage reranker.
- **Fixed chunking.** 500-token chunks with 100-token overlap. No semantic or recursive chunking.
- **No evaluation harness.** Retrieval and generation quality are not measured.
- **Single collection, single-user.** No multi-tenant or session isolation.
  
## License

[MIT](LICENSE)
