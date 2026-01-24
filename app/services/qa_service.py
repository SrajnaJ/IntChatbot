from pathlib import Path
from app.core.embeddings import generate_embedding
from app.vectorstore.faiss_store import FAISSVectorStore, load_embeddings
from app.core.llm import call_llm, build_prompt
from app.core.redaction import redact_text, contains_blocked_info


EMBEDDINGS_PATH = Path("data/embeddings/embeddings.json")


class QAService:
    def __init__(self):
        embeddings, metadata = load_embeddings(EMBEDDINGS_PATH)

        self.store = FAISSVectorStore(dim=len(embeddings[0]))
        self.store.add(embeddings, metadata)

    def answer(self, question: str, top_k: int = 3):
        query_embedding = generate_embedding(question)
        results = self.store.search(query_embedding, top_k=top_k)

        safe_chunks = []

        for r in results:
            text = r["text"]

            if contains_blocked_info(text):
                return {
                    "answer": "This information is restricted and cannot be shared.",
                    "sources": []
                }

            safe_chunks.append(redact_text(text))

        # if not results:
        #     return {
        #         "answer": "I don't have that information in the provided documents.",
        #         "sources": []
        #     }

        prompt = build_prompt(question, safe_chunks)
        answer = call_llm(prompt)

        sources = [
            {
                "document": r.get("source"),
                "chunk_id": r.get("chunk_id")
            }
            for r in results
        ]

        return {
            "answer": answer,
            "sources": sources
        }
