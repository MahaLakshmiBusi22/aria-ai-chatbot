# src/document_reader.py
# Reads PDF, DOCX, and TXT files and extracts clean text

import os
import fitz  # pymupdf
from docx import Document


def read_pdf(file_path):
    """
    Extract all text from a PDF file.
    fitz is the pymupdf library — it reads each page.
    """
    text = ""
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"


def read_docx(file_path):
    """
    Extract all text from a DOCX file.
    Reads each paragraph one by one.
    """
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {e}"


def read_txt(file_path):
    """
    Read a plain text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"Error reading TXT: {e}"


def read_document(file_path):
    """
    Master function — detects file type and reads accordingly.
    This is the only function you need to call from outside.
    """
    if not os.path.exists(file_path):
        return "Error: File not found."

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)
    elif extension == ".docx":
        return read_docx(file_path)
    elif extension == ".txt":
        return read_txt(file_path)
    else:
        return f"Error: Unsupported file type '{extension}'. Use PDF, DOCX, or TXT."


def chunk_text(text, chunk_size=1000):
    """
    Split large text into smaller chunks.
    Why: AI models have a limit on how much text they can read at once.
    We send only the most relevant chunk, not the entire document.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1

        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_document_summary(file_path):
    """
    Returns basic info about a document without reading all content.
    """
    text = read_document(file_path)

    if text.startswith("Error"):
        return text

    word_count = len(text.split())
    char_count = len(text)
    chunks = chunk_text(text)

    return {
        "file_path": file_path,
        "word_count": word_count,
        "char_count": char_count,
        "chunks": len(chunks),
        "preview": text[:200] + "..."
    }