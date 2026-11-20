from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    analysis_id: str
    filename: str
    match_score: int = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    suggestions: list[str]
