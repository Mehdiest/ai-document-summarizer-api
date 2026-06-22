import os


class AIProvider:
    """
    Safe AI layer with fallback support.
    Works with or without API key.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = bool(self.api_key)

    def summarize(self, text: str) -> dict:
        # Safety: always ensure string input
        if not isinstance(text, str):
            text = str(text)

        if not text.strip():
            return {
                "summary": "",
                "mode": "empty"
            }

        if not self.enabled:
            return self._fallback_summary(text)

        return self._openai_summary(text)

    def _openai_summary(self, text: str) -> dict:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this document clearly:\n\n{text}"
                }
            ]
        )

        return {
            "summary": response.choices[0].message.content,
            "mode": "ai"
        }

    def _fallback_summary(self, text: str) -> dict:
        # Ensure safe string handling
        text = str(text)

        sentences = text.split(".")
        first_sentence = sentences[0].strip() if sentences and sentences[0] else text[:200]

        return {
            "summary": first_sentence,
            "mode": "fallback"
        }