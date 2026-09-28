from gemini_client import gemini_service


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    hours_per_week: int = 5,
) -> str:

    prompt = f"""
Create a personalized learning path for:

TOPIC:
{topic}

LEARNER LEVEL:
{level}

AVAILABLE STUDY TIME:
{hours_per_week} hours per week

Create a structured progression from the learner's current level
toward advanced understanding.

Include:

1. Learning goal
2. Prerequisites
3. Stage-by-stage progression
4. Suggested weekly schedule
5. Practice activities
6. Projects or exercises
7. Recommended resource types
8. Milestones for checking progress
9. Next steps after completing the path

Make the plan practical and achievable.
Do not invent specific URLs.
When suggesting resources, identify resource types such as:
documentation, textbooks, courses, tutorials, videos, or practice platforms.
"""

    return gemini_service.generate_text(
        prompt,
        system_instruction="""
You are EduGenie's personalized learning-path planner.

Build educational paths that move logically from beginner concepts
through intermediate and advanced concepts.
""",
        temperature=0.35,
        max_output_tokens=3000,
    )