from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AnalysisResponse(BaseModel):
    analysis_id: str
    filename: str
    match_score: int = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    suggestions: list[str]


class AnalysisCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    job_title: str | None = Field(default=None, max_length=120)
    match_score: int = Field(ge=0, le=100)
    matched_skills: list[str] = Field(max_length=100)
    missing_skills: list[str] = Field(max_length=100)
    resume_skills: list[str] = Field(max_length=100)
    job_skills: list[str] = Field(min_length=1, max_length=100)
    suggestions: list[str] = Field(min_length=1, max_length=20)

    @field_validator("filename", "job_title", mode="before")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        if not isinstance(value, str):
            return value
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank.")
        return value

    @field_validator("matched_skills", "missing_skills", "resume_skills", "job_skills", "suggestions")
    @classmethod
    def clean_lists(cls, values):
        cleaned = [item.strip() for item in values if isinstance(item, str) and item.strip()]
        if len(cleaned) != len(values):
            raise ValueError("List items must be non-empty strings.")
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("List items must be unique.")
        return cleaned

    @model_validator(mode="after")
    def validate_skill_relationships(self):
        job = set(self.job_skills)
        resume = set(self.resume_skills)
        matched = set(self.matched_skills)
        missing = set(self.missing_skills)
        if not matched.issubset(job) or not matched.issubset(resume):
            raise ValueError("Matched skills must exist in both job_skills and resume_skills.")
        if not missing.issubset(job) or matched.intersection(missing):
            raise ValueError("Missing skills must be job skills and cannot also be matched.")
        expected_score = round(len(matched) / len(job) * 100)
        if self.match_score != expected_score:
            raise ValueError(f"match_score must equal {expected_score} for the supplied skill lists.")
        return self


class AnalysisRecordRead(AnalysisCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
