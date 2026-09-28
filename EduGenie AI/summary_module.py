from gemini_client import gemini_service


def summarize_text(
    text: str,
    max_words: int = 150,
) -> str:

    prompt = f"""
Summarize the following educational text.

TEXT:
{text}

Requirements:
- Maximum approximately {max_words} words.
- Preserve the important ideas.
- Remove repetition.
- Use simple language.
- Keep important technical terms.
- Do not introduce facts that are absent from the source.
- Use short paragraphs or bullet points where useful.
"""

    return gemini_service.generate_text(
        prompt,
        system_instruction="""
You are EduGenie's educational summarization engine.
Your job is to make study material shorter without losing its essential meaning.
""",
        temperature=0.2,
        max_output_tokens=1800,
    )