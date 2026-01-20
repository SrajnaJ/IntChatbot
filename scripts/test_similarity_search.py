# scripts/test_similarity_search.py

from pathlib import Path

from app.core.embeddings import generate_embedding
from app.vectorstore.faiss_store import FAISSVectorStore, load_embeddings


EMBEDDINGS_PATH = Path("data/embeddings/embeddings.json")


def main():
    embeddings, metadata = load_embeddings(EMBEDDINGS_PATH)

    dim = len(embeddings[0])
    store = FAISSVectorStore(dim=dim)

    store.add(embeddings, metadata)

    print("FAISS index built")

    # Test query
    query = "How many paid leaves do employees get?"
    query_embedding = generate_embedding(query)

    results = store.search(query_embedding, top_k=3)

    print("\nTop results:\n")
    for r in results:
        print(f"Source: {r['source']}")
        print(r["text"][:300])
        print("-" * 50)


if __name__ == "__main__":
    main()
