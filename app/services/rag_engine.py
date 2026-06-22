class SimpleRAG:
    """
    Lightweight multi-document memory system.
    """

    def __init__(self):
        self.docs = []

    def add_document(self, text: str):
        self.docs.append(text)

    def query(self, question: str):
        # very simple keyword overlap scoring
        scores = []

        for doc in self.docs:
            score = len(set(question.lower().split()) & set(doc.lower().split()))
            scores.append((score, doc))

        scores.sort(reverse=True, key=lambda x: x[0])

        best_match = scores[0][1] if scores else ""

        return {
            "answer": best_match[:300],
            "context_used": len(self.docs)
        }