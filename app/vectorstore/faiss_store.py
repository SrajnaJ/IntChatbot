# app/vectorstore/faiss_store.py

import faiss
import numpy as np
import json
from pathlib import Path


class FAISSVectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)  # cosine similarity
        self.metadata = []

    def add(self, embeddings, metadata):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k=5):
        query_vector = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])

        return results


def load_embeddings(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    embeddings = [item["embedding"] for item in data]
    metadata = [
        {
            "id": item["id"],
            "text": item["text"],
            "source": item["source"]
        }
        for item in data
    ]

    return embeddings, metadata
