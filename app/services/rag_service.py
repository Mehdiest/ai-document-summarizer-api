<<<<<<< HEAD
from typing import List

DOCUMENT_CHUNKS = []


def chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    """
    Split text into fixed-size chunks.
    """
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def store_document(text: str) -> int:
    """
    Store document chunks in memory.
    """

    global DOCUMENT_CHUNKS

    DOCUMENT_CHUNKS = chunk_text(text)

    return len(DOCUMENT_CHUNKS)


def retrieve_chunks(question: str, top_k: int = 3) -> List[str]:
    """
    Simple keyword retrieval.
    """

    question_words = set(question.lower().split())

    scored = []

    for chunk in DOCUMENT_CHUNKS:

        chunk_words = set(chunk.lower().split())

        score = len(question_words.intersection(chunk_words))

        scored.append((score, chunk))

    scored.sort(reverse=True)

    return [chunk for score, chunk in scored[:top_k]]


def answer_question(question: str) -> dict:
    """
    Generate answer from retrieved chunks.
    """

    chunks = retrieve_chunks(question)

    if not chunks:
        return {
            "answer": "No relevant information found.",
            "chunks": []
        }

    return {
        "answer": chunks[0],
        "chunks": chunks
=======
from typing import List

DOCUMENT_CHUNKS = []


def chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    """
    Split text into fixed-size chunks.
    """
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def store_document(text: str) -> int:
    """
    Store document chunks in memory.
    """

    global DOCUMENT_CHUNKS

    DOCUMENT_CHUNKS = chunk_text(text)

    return len(DOCUMENT_CHUNKS)


def retrieve_chunks(question: str, top_k: int = 3) -> List[str]:
    """
    Simple keyword retrieval.
    """

    question_words = set(question.lower().split())

    scored = []

    for chunk in DOCUMENT_CHUNKS:

        chunk_words = set(chunk.lower().split())

        score = len(question_words.intersection(chunk_words))

        scored.append((score, chunk))

    scored.sort(reverse=True)

    return [chunk for score, chunk in scored[:top_k]]


def answer_question(question: str) -> dict:
    """
    Generate answer from retrieved chunks.
    """

    chunks = retrieve_chunks(question)

    if not chunks:
        return {
            "answer": "No relevant information found.",
            "chunks": []
        }

    return {
        "answer": chunks[0],
        "chunks": chunks
>>>>>>> c37b28e (Add V3.1 document chat prototype)
    }