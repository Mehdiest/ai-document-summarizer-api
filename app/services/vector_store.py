import faiss
import numpy as np


class VectorStore:
    """
    Simple FAISS-based vector store for semantic search.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, embedding: np.ndarray, text: str):
        embedding = np.array(embedding).astype("float32").reshape(1, -1)

        self.index.add(embedding)
        self.texts.append(text)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])

        return results