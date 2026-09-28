from typing import List

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="The student's input.",
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Input cannot be empty.")

        return value


class QARequest(TextRequest):
    pass


class ExplanationRequest(TextRequest):
    level: str = Field(
        default="beginner",
        description="Learner level.",
    )

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        allowed = {
            "beginner",
            "intermediate",
            "advanced",
        }

        value = value.strip().lower()

        if value not in allowed:
            raise ValueError(
                "Level must be beginner, intermediate, or advanced."
            )

        return value


class QuizRequest(TextRequest):
    number_of_questions: int = Field(
        default=3,
        ge=1,
        le=10,
    )


class SummaryRequest(TextRequest):
    max_words: int = Field(
        default=150,
        ge=30,
        le=1000,
    )


class LearningPathRequest(TextRequest):
    level: str = Field(
        default="beginner",
    )

    hours_per_week: int = Field(
        default=5,
        ge=1,
        le=40,
    )

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        allowed = {
            "beginner",
            "intermediate",
            "advanced",
        }

        value = value.strip().lower()

        if value not in allowed:
            raise ValueError(
                "Level must be beginner, intermediate, or advanced."
            )

        return value


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(
        ...,
        min_length=4,
        max_length=4,
    )
    correct_answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]