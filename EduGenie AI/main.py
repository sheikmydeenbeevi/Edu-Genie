from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import get_settings
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    ExplanationRequest,
    LearningPathRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
)
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "EduGenie - Google Gemini powered learning assistant."
    ),
)

app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


def validate_input_length(text: str) -> None:
    if len(text) > settings.max_input_length:
        raise HTTPException(
            status_code=413,
            detail=(
                f"Input is too long. Maximum allowed length is "
                f"{settings.max_input_length} characters."
            ),
        )


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
        },
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
        "gemini_configured": bool(settings.gemini_api_key),
        "local_explainer": settings.use_local_explainer,
    }


@app.post("/qa")
async def qa(request: QARequest):
    validate_input_length(request.text)

    try:
        answer = answer_question(request.text)

        return {
            "success": True,
            "answer": answer,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/explain")
async def explain(request: ExplanationRequest):
    validate_input_length(request.text)

    try:
        explanation = explain_topic(
            request.text,
            request.level,
        )

        return {
            "success": True,
            "explanation": explanation,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/quiz")
async def quiz(request: QuizRequest):
    validate_input_length(request.text)

    try:
        result = generate_quiz(
            request.text,
            request.number_of_questions,
        )

        return {
            "success": True,
            **result.model_dump(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/summarize")
async def summarize(request: SummaryRequest):
    validate_input_length(request.text)

    try:
        summary = summarize_text(
            request.text,
            request.max_words,
        )

        return {
            "success": True,
            "summary": summary,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningPathRequest,
):
    validate_input_length(request.text)

    try:
        recommendations = get_learning_recommendations(
            topic=request.text,
            level=request.level,
            hours_per_week=request.hours_per_week,
        )

        return {
            "success": True,
            "recommendations": recommendations,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc