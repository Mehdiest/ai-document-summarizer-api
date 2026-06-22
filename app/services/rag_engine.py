from typing import List, Dict
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore


class RAGEngine:
    """
    Retrieval-Augmented Generation (RAG) Engine

    Responsibilities:
    - Chunking documents
    - Embedding text chunks
    - Storing vectors in FAISS
    - Retrieving relevant chunks for queries
    """

    def __init__(self, dimension: int = 384):
        self.embedder = Embedder()
        self.vector_store = VectorStore(dimension=dimension)

        self.chunks: List[str] = []
        self.is_indexed = False

    # -----------------------------
    # TEXT PROCESSING
    # -----------------------------
    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Simple chunking strategy (character-based).
        Can be upgraded later to semantic chunking.
        """
        if not isinstance(text, str):
            text = str(text)

        text = text.strip()

        if not text:
            return []

        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

    # -----------------------------
    # INDEXING
    # -----------------------------
    def index(self, text: str) -> Dict:
        """
        Index a document into vector store.
        Resets previous state to avoid duplication.
        """

        # reset state (important fix for duplication bug)
        self.vector_store = VectorStore(dimension=self.vector_store.dimension)
        self.chunks = []
        self.is_indexed = False

        # chunking
        self.chunks = self.chunk_text(text)

        if not self.chunks:
            return {
                "status": "error",
                "message": "No valid chunks found"
            }

        # embedding + storing
        for chunk in self.chunks:
            clean_chunk = chunk.strip()
            if not clean_chunk:
                continue

            embedding = self.embedder.encode(clean_chunk)
            self.vector_store.add(embedding, clean_chunk)

        self.is_indexed = True

        return {
            "status": "success",
            "chunks_indexed": len(self.chunks)
        }

    # -----------------------------
    # SEARCH
    # -----------------------------
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Semantic search over indexed document.
        """

        if not self.is_indexed:
            return []

        if not isinstance(query, str):
            query = str(query)

        query = query.strip()

        if not query:
            return []

        query_embedding = self.embedder.encode(query)

        results = self.vector_store.search(query_embedding, top_k=top_k)

        # remove duplicates (important fix)
        seen = set()
        unique_results = []

        for r in results:
            if r not in seen:
                unique_results.append(r)
                seen.add(r)

        return unique_results

    # -----------------------------
    # UTILITY
    # -----------------------------
    def reset(self):
        """
        Clear all indexed data.
        """
        self.vector_store = VectorStore(dimension=self.vector_store.dimension)
        self.chunks = []
        self.is_indexed = False

    def get_stats(self) -> Dict:
        """
        Debug info for system monitoring.
        """
        return {
            "chunks": len(self.chunks),
            "indexed": self.is_indexed,
            "dimension": self.vector_store.dimension
        }