from pathlib import Path
import json

from app.services.document_loader import load_document
from app.services.chunker import chunk_text


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(exist_ok=True)


def ingest():
    all_chunks = []

    for file in RAW_DIR.iterdir():
        print(f"Processing {file.name}")

        text = load_document(file)
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{file.stem}_{i}",
                "text": chunk,
                "source": file.name
            })

    with open(PROCESSED_DIR / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Saved {len(all_chunks)} chunks")


if __name__ == "__main__":
    ingest()
