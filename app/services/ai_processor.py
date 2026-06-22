from app.services.ai_provider import AIProvider
from app.services.insight_generator import InsightGenerator

provider = AIProvider()
insight_engine = InsightGenerator()


def process_text(extracted_result) -> dict:
    """
    Full processing pipeline:
    - AI summary
    - fallback summary
    - structured insights
    """

    if isinstance(extracted_result, dict):
        text = extracted_result.get("text", "")
    else:
        text = extracted_result

    ai_result = provider.summarize(text)
    insights = insight_engine.generate(text)

    return {
        "summary": ai_result["summary"],
        "mode": ai_result["mode"],
        "key_points": insights["key_points"],
        "keywords": insights["keywords"],
        "insight": insights["insight"]
    }