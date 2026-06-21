# Krakow Guide on AI

RAG system with hybrid retrieval (BM25 + TF-IDF vectors) over 500+ Krakow locations.

## What it is
Not another TUI demo. This is a working retriever: chunked location data, hybrid BM25 + dense similarity, ranked results.

- 500+ Krakow POIs in `locations.json`
- Chunking: 120 tokens, 20 token overlap
- Hybrid scoring: 60% TF-IDF cosine + 40% BM25 term hit ratio
- Zero external API deps — runs on `python3`

## Quickstart

```bash
python3 pythonRetrieval.py
```

Interactive:

```python
from pythonRetrieval import retriever
hits = retriever.retrieve("UNESCO sites near Krakow", k=4)
```

## Status
- Retrieval: ✅ working
- Dataset: ✅ 500+ locations
- Hybrid index: ✅ built on load
- UI: ⏳ planned (CLI/API wrapper)

## Stack
Python 3.11, no frameworks. Pure stdlib + math.
