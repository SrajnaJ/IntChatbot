import fitz  # pymupdf
from docx import Document
from pathlib import Path


def load_pdf(path: Path) -> str:
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def load_docx(path: Path) -> str:
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def load_md(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def load_document(path: Path) -> str:
    if path.suffix == ".pdf":
        return load_pdf(path)
    elif path.suffix == ".docx":
        return load_docx(path)
    elif path.suffix == ".md":
        return load_md(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")