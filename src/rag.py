# src/rag.py
# RAG — Retrieval-Augmented Generation
# Uses chromadb for vector search — no sentence-transformers needed

import chromadb
import os
import hashlib


CHROMA_PATH = "database/chroma"


def get_collection():
    """Get or create a ChromaDB collection using built-in embeddings."""
    os.makedirs(CHROMA_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )


def chunk_document(text, chunk_size=300, overlap=30):
    """
    Split a document into overlapping chunks.
    Smaller chunks = faster search + more precise answers.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def index_document(document_text, document_name, user_id):
    """
    Split document into chunks and store in ChromaDB.
    ChromaDB handles embeddings internally — no separate model needed.
    """
    collection = get_collection()

    doc_hash = hashlib.md5(f"{user_id}_{document_name}".encode()).hexdigest()

    # Remove old chunks for this document first
    try:
        existing = collection.get(where={"doc_hash": {"$eq": doc_hash}})
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except Exception:
        pass

    chunks = chunk_document(document_text)
    print(f"Indexing '{document_name}' — {len(chunks)} chunks...")

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"{doc_hash}_chunk_{i}")
        documents.append(chunk)
        metadatas.append({
            "document_name": document_name,
            "user_id": str(user_id),
            "chunk_index": i,
            "doc_hash": doc_hash
        })

    # ChromaDB generates embeddings automatically
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"✅ Indexed {len(chunks)} chunks for '{document_name}'")
    return len(chunks)


def get_relevant_context(query, document_name, user_id, top_k=3):
    """
    Find the most relevant chunks for a query.
    Returns joined context string.
    """
    collection = get_collection()
    doc_hash = hashlib.md5(f"{user_id}_{document_name}".encode()).hexdigest()

    try:
        total = collection.count()
        if total == 0:
            return None

        results = collection.query(
            query_texts=[query],
            n_results=min(top_k, total),
            where={"doc_hash": {"$eq": doc_hash}}
        )

        if not results["documents"] or not results["documents"][0]:
            return None

        return "\n\n---\n\n".join(results["documents"][0])

    except Exception as e:
        print(f"Search error: {e}")
        return None


def remove_document(document_name, user_id):
    """Remove all chunks for a document from ChromaDB."""
    collection = get_collection()
    doc_hash = hashlib.md5(f"{user_id}_{document_name}".encode()).hexdigest()

    try:
        results = collection.get(where={"doc_hash": {"$eq": doc_hash}})
        if results["ids"]:
            collection.delete(ids=results["ids"])
            print(f"✅ Removed {len(results['ids'])} chunks for '{document_name}'")
    except Exception as e:
        print(f"Remove error: {e}")


if __name__ == "__main__":
    print("Testing RAG system...")

    test_text = """
    Python is a high-level programming language created by Guido van Rossum in 1991.
    It is known for its simple and readable syntax.
    Python is widely used in web development, data science, AI, and automation.

    Hyderabad is the capital city of Telangana state in India.
    It is known as the City of Pearls and is a major technology hub.
    Many top companies like Microsoft, Google, and Amazon have offices in Hyderabad.

    Machine learning is a subset of artificial intelligence.
    It allows computers to learn from data without being explicitly programmed.
    """

    index_document(test_text, "test_doc.txt", user_id=1)

    print("\nSearching: 'Who created Python?'")
    result = get_relevant_context("Who created Python?", "test_doc.txt", user_id=1)
    print(f"Found: {result[:150] if result else 'Nothing found'}...")

    print("\nSearching: 'Tell me about Hyderabad'")
    result = get_relevant_context("Tell me about Hyderabad", "test_doc.txt", user_id=1)
    print(f"Found: {result[:150] if result else 'Nothing found'}...")

    print("\n✅ RAG test complete!")