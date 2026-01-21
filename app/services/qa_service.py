from pathlib import Path
from app.core.embeddings import generate_embedding
from app.vectorstore.faiss_store import FAISSVectorStore, load_embeddings
from app.core.llm import call_llm, build_prompt

EMBEDDINGS_PATH = Path("data/embeddings/embeddings.json")


class QAService:
    def __init__(self):
        embeddings, metadata = load_embeddings(EMBEDDINGS_PATH)

        self.store = FAISSVectorStore(dim=len(embeddings[0]))
        self.store.add(embeddings, metadata)

    def answer(self, question: str, top_k: int = 3) -> str:
        query_embedding = generate_embedding(question)
        results = self.store.search(query_embedding, top_k=top_k)

        if not results:
            return "I don't have that information in the provided documents."

        chunks = [r["text"] for r in results]
        prompt = build_prompt(question, chunks)

        return call_llm(prompt)
