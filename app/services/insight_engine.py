import re
from collections import Counter


def generate_insights(text: str) -> dict:
    """
    Lightweight document analytics for V3 pipeline.
    """

    if not isinstance(text, str):
        text = str(text)

    words = re.findall(r"\w+", text.lower())
    sentences = [s for s in text.split(".") if s.strip()]

    word_count = len(words)
    sentence_count = len(sentences)

    # simple keyword extraction
    most_common = Counter(words).most_common(5)
    keywords = [word for word, _ in most_common if len(word) > 3]

    # complexity heuristic
    if word_count < 50:
        complexity = "low"
    elif word_count < 200:
        complexity = "medium"
    else:
        complexity = "high"

    return {
        "key_points": [
            f"- {sentences[0].strip()}" if sentences else "- No content"
        ],
        "keywords": keywords,
        "insight": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "complexity": complexity
        }
    }