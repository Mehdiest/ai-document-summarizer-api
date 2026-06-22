from collections import Counter
import re


class InsightGenerator:
    """
    Extracts structured insights from raw text.
    Lightweight NLP layer (no external dependency).
    """

    def generate(self, text: str) -> dict:
        if not isinstance(text, str):
            text = str(text)

        sentences = self._get_sentences(text)
        keywords = self._extract_keywords(text)
        bullets = self._generate_bullets(sentences)

        return {
            "summary": self._summary(sentences, text),
            "key_points": bullets,
            "keywords": keywords[:10],
            "insight": {
                "sentence_count": len(sentences),
                "word_count": len(text.split()),
                "complexity": self._estimate_complexity(text)
            }
        }

    def _get_sentences(self, text):
        return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    def _summary(self, sentences, text):
        if sentences:
            return sentences[0]
        return text[:200]

    def _generate_bullets(self, sentences):
        return [f"- {s}" for s in sentences[:5]]

    def _extract_keywords(self, text):
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
        stop_words = {"this", "that", "with", "from", "have", "will", "into", "your"}
        filtered = [w for w in words if w not in stop_words]

        freq = Counter(filtered)
        return [w for w, _ in freq.most_common(10)]

    def _estimate_complexity(self, text):
        words = len(text.split())
        if words < 100:
            return "low"
        elif words < 500:
            return "medium"
        return "high"