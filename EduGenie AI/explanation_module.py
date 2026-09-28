from __future__ import annotations

from typing import Optional

from config import get_settings
from gemini_client import gemini_service


LOCAL_PIPELINE = None


def _load_local_model():
    """
    Lazily load LaMini-Flan-T5.

    The model is loaded only when USE_LOCAL_EXPLAINER=true.
    """

    global LOCAL_PIPELINE

    if LOCAL_PIPELINE is not None:
        return LOCAL_PIPELINE

    try:
        from transformers import pipeline

        settings = get_settings()

        LOCAL_PIPELINE = pipeline(
            "text2text-generation",
            model=settings.local_explainer_model,
        )

        return LOCAL_PIPELINE

    except ImportError as exc:
        raise RuntimeError(
            "Local explanation model requires transformers. "
            "Run: pip install -r requirements-local.txt"
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"Could not load local explanation model: {exc}"
        ) from exc


def explain_with_local_model(
    topic: str,
    level: str,
) -> str:
    model = _load_local_model()

    prompt = f"""
Explain the following educational topic for a {level} learner.

Topic:
{topic}

Requirements:
- Use simple language.
- Break difficult ideas into steps.
- Give one practical example.
- Avoid unnecessary jargon.
"""

    result = model(
        prompt,
        max_new_tokens=300,
        do_sample=False,
    )

    if not result:
        raise RuntimeError(
            "The local model returned an empty response."
        )

    return result[0]["generated_text"].strip()


def explain_topic(
    topic: str,
    level: str = "beginner",
) -> str:
    """
    Explain a concept.

    If local mode is enabled, use LaMini-Flan-T5.
    Otherwise use Gemini.
    """

    settings = get_settings()

    if settings.use_local_explainer:
        try:
            return explain_with_local_model(
                topic,
                level,
            )
        except Exception:
            # Graceful fallback to Gemini.
            pass

    prompt = f"""
Explain this educational concept to a {level} learner:

{topic}

Structure the response as:

1. Simple definition
2. How it works
3. Easy example
4. Important points
5. One quick check question

Keep the explanation clear and concise.
"""

    return gemini_service.generate_text(
        prompt,
        system_instruction="""
You are EduGenie's concept explanation tutor.
Your goal is to make difficult concepts understandable.
Never assume the learner already understands advanced terminology.
""",
        temperature=0.25,
        max_output_tokens=1800,
    )