import re
from uuid import uuid4

SKILLS = {
    "python", "java", "c++", "javascript", "typescript", "react",
    "node.js", "fastapi", "django", "flask", "sql", "postgresql",
    "mysql", "mongodb", "html", "css", "git", "docker", "aws",
    "machine learning", "data analysis", "pandas", "numpy",
    "communication", "problem solving", "linux", "rest api",
    "firebase", "flutter", "kotlin", "figma", "excel"
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def detect_skills(text: str) -> list[str]:
    normalized = normalize(text)
    found = []
    for skill in sorted(SKILLS):
        pattern = rf"(?<![\w]){re.escape(skill)}(?![\w])"
        if re.search(pattern, normalized):
            found.append(skill)
    return found


def analyze_resume(resume_text: str, job_description: str, filename: str) -> dict:
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_description)
    if not job_skills:
        raise ValueError("No supported skills were detected in the job description.")

    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    suggestions = []
    if missing:
        suggestions.append(
            "If you genuinely have these skills, show evidence in projects or experience: "
            + ", ".join(missing[:8]) + "."
        )
    if not any(term in normalize(resume_text) for term in ("project", "developed", "built")):
        suggestions.append("Consider adding a Projects section with your contribution and outcomes.")
    if not suggestions:
        suggestions.append("Good keyword overlap. Tailor project descriptions to the role.")

    return {
        "analysis_id": str(uuid4()),
        "filename": filename,
        "match_score": round(len(matched) / len(job_skills) * 100),
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "suggestions": suggestions,
    }
