import os


class AIProvider:
    """
    Unified AI layer (OpenAI + fallback)
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = bool(self.api_key)

    def summarize(self, text: str) -> dict:
        if not isinstance(text, str):
            text = str(text)

        if not text.strip():
            return {
                "summary": "",
                "mode": "empty"
            }

        if self.enabled:
            return self._openai_summary(text)

        return self._fallback_summary(text)

    def _openai_summary(self, text: str) -> dict:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this document:\n\n{text}"
                }
            ]
        )

        return {
            "summary": response.choices[0].message.content,
            "mode": "ai"
        }

    def _fallback_summary(self, text: str) -> dict:
        text = str(text)

        sentences = text.split(".")
        first = sentences[0].strip() if sentences and sentences[0] else text[:200]

        return {
            "summary": first,
            "mode": "fallback"
        }


# Global instance (important for routes)
ai_provider = AIProvider()