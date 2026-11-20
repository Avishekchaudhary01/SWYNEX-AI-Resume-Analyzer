from io import BytesIO
from pathlib import Path

import fitz
from docx import Document

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_BYTES = 5 * 1024 * 1024


def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF and DOCX files are supported.")
    if not content:
        raise ValueError("The uploaded file is empty.")
    if len(content) > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 5 MB upload limit.")

    try:
        if suffix == ".pdf":
            with fitz.open(stream=content, filetype="pdf") as pdf:
                text = "\n".join(page.get_text() for page in pdf)
        else:
            document = Document(BytesIO(content))
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception as exc:
        raise ValueError("The document could not be read. Please upload a valid PDF or DOCX.") from exc

    if not text.strip():
        raise ValueError("No readable text was found. Scanned-image PDFs are not supported.")
    return text
