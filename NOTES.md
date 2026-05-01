# Notes

## Why I built this

I built this in January 2026, when RAGs were everywhere. I'd read about them and studied the architecture, but it hadn't fully clicked and I've learned not to trust an understanding that lives only in articles. So I built the smallest functional version I could.

This aligns with how I approach engineering and study generally: learn by building, build by learning. Reading more would have given me more vocabulary; building gave me intuition.

## The choice to keep it barebones

Barebones meant focusing on the fundamentals and refusing to digress into nice-to-haves. The clearest example is the system prompt, it has one job and no niceties. I deliberately did not spend time crafting the perfect prompt, because that wasn't the point. The point was to understand how the pipeline actually operates.

I read the docs for every component I used... the ingestion logic, the embedding model, Qdrant and tried to internalize what each layer was actually doing rather than treat any of it as a black box. The goal was theoretical grounding, not production software.

## Choices and tradeoffs

**Vector store: Qdrant, local.** Simple to set up, runs entirely on my machine, no external dependencies. Cloud would have meant another service to manage and another moving part I didn't need. Running it locally also kept everything close the math and the storage happening on the same machine I was thinking on. There's a small psychological thing to that proximity that I think helped.

**Embedding model: `BAAI/bge-small-en-v1.5`.** Default choice for this size class. 384 dimensions, fast to run locally, good enough quality for a learning project. Open to revisiting if I push this further.

**Chunking: 500 tokens with 100 overlap.** Trial and error. I tested several sizes against the document I was using and 500/100 gave the cleanest retrieval. Not a defended optimum a working one for this corpus.

**LLM: Groq + Llama 3.3 70B Versatile.** I started on Gemini 2.5 Flash, but my key expired and Google Cloud's auth flow was painful enough that I switched. Groq has been excellent, fast inference, clean SDK, no friction. The model choice within Groq was straightforward: 70B Versatile is the strongest open-source option they serve, and for a single-user system the latency hit over 8B is negligible.

**Backend split: FastAPI + Streamlit, not just Streamlit.** Cleaner separation between the retrieval/generation logic and the UI. The backend can be queried independently; the frontend stays purely about presentation. It also forced me to think of the RAG as a service rather than a script with a UI on top. The UI did not concern me in this project, hence it was 100% AI-Generated.

**Strict grounding prompt.** The system prompt locks the model to retrieved context. It will refuse general conversation even "hello" gets nothing useful. This is intentional. The focus was the pipeline, not prompt tuning. A friendlier prompt would have made the project feel more polished and taught me less.

## What I deliberately left out

A short list of what a "real" RAG would have, and why each was correctly out of scope for v0:

- **A good prompt.** Prompt engineering is its own discipline. Mixing it into a pipeline-learning project would have muddled the signal on what was actually working.
- **Better chunking.** Semantic chunking, recursive splitting, document-aware boundaries, all real improvements over fixed-window.
- **Reranking.** A second-stage reranker after top-k retrieval typically lifts answer quality more than any other single addition. Worth adding if in case this becomes anything serious.
- **Evaluation.** No retrieval metrics, no answer-quality scoring, no test set. You can't improve what you don't measure, but at v0 the goal was to get the loop running, not to optimize it.
- **Multi-format ingestion.** PDF, DOCX, HTML, markdown each adds parsing complexity that has nothing to do with the RAG fundamentals. `.txt` strips the problem to its core.

The list is the point. Knowing what to leave out is most of the work.

## What I learned

Beyond the obvious: how the pipeline fits together end to end, three things stuck:

I went down a long rabbit hole on cosine similarity and ended up with a much better intuition for what next-token prediction actually is and how language models relate words to each other in vector space. The math felt abstract until I was pulling top-k matches and watching which chunks scored highest for which queries. Then it stopped feeling abstract.

I also got my first real reps in scrappy debugging and working in the terminal. Every project before this had been a tutorial, where the path was laid out and the errors were anticipated. This was the first time I was running into errors with no script to follow, and the first time I had to read tracebacks seriously. That muscle was new.

And finally: even with heavy AI assistance, this was a project I directed end to end. The pipeline structure, the file layout, the decisions about what went where... all mine. The code was partly AI-written; the system was not. That distinction turned out to matter more than I expected.

## What I'd build next

I don't have plans to extend this RAG much further as a standalone project. Given how fast the field is moving, refining it into a more modern version is worth doing: better chunking, reranking, evaluation, multi-format ingestion. Once it's at that level, I may potentially integrate it as a memory layer into the products I'm building rather than continue developing it as its own thing. The value of this project was the understanding it gave me. The understanding compounds across everything I build next.