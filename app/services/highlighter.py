import re


class Highlighter:
    """
    Extracts important phrases for UI highlighting.
    """

    def extract(self, text: str):
        sentences = re.split(r"[.!?]", text)

        important = [
            s.strip()
            for s in sentences
            if any(word in s.lower() for word in ["important", "key", "result", "conclusion", "summary"])
        ]

        return {
            "highlights": important[:5]
        }