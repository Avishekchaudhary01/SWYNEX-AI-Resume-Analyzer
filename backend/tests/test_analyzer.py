import pytest
from app.services.analyzer import analyze_resume, detect_skills

def test_detect_skills():
    assert detect_skills("Built a React app with Python and SQL") == ["python", "react", "sql"]

def test_match_score_and_skill_lists():
    result = analyze_resume("Developed projects using Python, SQL and React.", "Looking for Python, SQL and Docker experience.", "sample.pdf")
    assert result["match_score"] == 67
    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["docker"]

def test_no_job_skills_raises_helpful_error():
    with pytest.raises(ValueError, match="No supported skills"):
        analyze_resume("Python developer", "Must be curious and proactive.", "resume.pdf")
