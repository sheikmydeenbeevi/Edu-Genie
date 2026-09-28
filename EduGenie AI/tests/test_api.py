from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_qa_requires_text():
    response = client.post(
        "/qa",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422


def test_explain_invalid_level():
    response = client.post(
        "/explain",
        json={
            "text": "Photosynthesis",
            "level": "expert"
        },
    )

    assert response.status_code == 422


def test_quiz_invalid_question_count():
    response = client.post(
        "/quiz",
        json={
            "text": "Photosynthesis",
            "number_of_questions": 0
        },
    )

    assert response.status_code == 422


def test_summary_invalid_word_limit():
    response = client.post(
        "/summarize",
        json={
            "text": "Some educational text.",
            "max_words": 10
        },
    )

    assert response.status_code == 422


def test_learning_path_validation():
    response = client.post(
        "/learn/recommendations",
        json={
            "text": "Python programming",
            "level": "unknown",
            "hours_per_week": 5
        },
    )

    assert response.status_code == 422