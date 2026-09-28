from gemini_client import gemini_service


SYSTEM_PROMPT = """
You are EduGenie, an educational AI assistant.

Your job is to answer student questions accurately and clearly.

Rules:
1. Give a direct answer first.
2. Explain the reasoning in simple language.
3. Avoid unnecessary jargon.
4. Use examples when useful.
5. If the question is ambiguous, state the assumption you made.
6. Do not invent sources, citations, statistics, or facts.
7. For academic topics, prioritize educational clarity.
"""


def answer_question(question: str) -> str:
    prompt = f"""
Student question:

{question}

Answer this question as an educational assistant.
"""

    return gemini_service.generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT,
        temperature=0.2,
        max_output_tokens=1500,
    )