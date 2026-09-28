from typing import List

from gemini_client import gemini_service
from schemas import QuizQuestion, QuizResponse


def generate_quiz(
    source_text: str,
    number_of_questions: int = 3,
) -> QuizResponse:

    prompt = f"""
Create {number_of_questions} multiple-choice questions
from the educational content below.

CONTENT:
{source_text}

Requirements:

- Each question must test understanding of the content.
- Each question must contain exactly four options.
- There must be exactly one correct answer.
- correct_answer must exactly match one of the four options.
- Include a short explanation of the correct answer.
- Do not ask questions unrelated to the content.
- Avoid trick questions.
- Return only the requested structured data.
"""

    data = gemini_service.generate_json(
        prompt,
        response_schema=QuizResponse,
        system_instruction="""
You are EduGenie's quiz-generation engine.

Create useful educational MCQs.
Every question must have exactly four options.
""",
        temperature=0.2,
        max_output_tokens=4000,
    )

    quiz = QuizResponse.model_validate(data)

    if len(quiz.questions) != number_of_questions:
        raise RuntimeError(
            f"Expected {number_of_questions} questions but "
            f"received {len(quiz.questions)}."
        )

    for question in quiz.questions:
        if len(question.options) != 4:
            raise RuntimeError(
                "Every quiz question must contain exactly four options."
            )

        if question.correct_answer not in question.options:
            raise RuntimeError(
                "A correct answer was not found among the options."
            )

    return quiz