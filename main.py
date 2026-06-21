#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Krakow Guide on AI - Hybrid RAG CLI
500+ locations, BM25 + TF-IDF hybrid retrieval, chunked corpus.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent))

from pythonRetrieval import retriever

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║              KRAKOW GUIDE ON AI — HYBRID RAG                ║
║  500+ locations | BM25 + TF-IDF | Chunked corpus           ║
╚══════════════════════════════════════════════════════════════╝
"""

def interactive():
    print(BANNER)
    print(f"Loaded {len(retriever.docs)} chunks from {len(set(d['title'] for d in retriever.docs))} locations.")
    print("Type queries, or 'quit' to exit.\n")
    while True:
        try:
            q = input("🔍 Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not q or q.lower() in ('quit','exit','q'):
            print("Bye.")
            break
        hits = retriever.retrieve(q, k=4)
        print(f"\nTop {len(hits)} results:\n")
        for i, h in enumerate(hits, 1):
            print(f"{i}. {h['source']} — {h['text'][:120]}...")
            print(f"   URI: {h['uri']}\n")

if __name__ == "__main__":
    interactive()
