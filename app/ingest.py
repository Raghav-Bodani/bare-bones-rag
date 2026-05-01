from pathlib import Path 
from pypdf import PdfReader

RAW_DIR = Path("data/raw_docs")

def load_text():
    texts = []
    for p in RAW_DIR.iterdir():
        if p.suffix.lower() == ".txt":
            texts.append(p.read_text(encoding="utf-8"))
        elif p.suffix.lower() == ".pdf":
            reader = PdfReader(str(p))
            texts.append("\n".join(page.extract_text() or "" for page in reader.pages))
    return "\n".join(texts)

