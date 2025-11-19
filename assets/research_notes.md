# Research Notes on Local-First AI

## What is Local-First AI?
Local-first AI refers to systems where the core computation—embeddings,
vector search, summarization, inference—runs directly on the user's device.
This approach improves privacy and reduces dependency on remote servers.

## Advantages of Local-First Models
- **Privacy:** No document data leaves the device.
- **Speed:** Retrieval is much faster due to local vector DBs.
- **Offline Access:** Users can query their knowledge base without internet.
- **Control:** Users can delete, backup, or move their data freely.

## Relevant Technologies
- `SQLite + Vector Extension` for embeddings
- `FAISS` for fast similarity search
- `llama.cpp` for local LLM inference
- `sentence-transformers` for local embeddings

Cerebro's architecture is designed to experiment with all of these.
