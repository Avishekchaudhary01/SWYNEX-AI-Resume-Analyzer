import os
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Analysis
from app.schemas import AnalysisCreate, AnalysisRecordRead, AnalysisResponse
from app.services.analyzer import analyze_resume
from app.services.parser import extract_text, MAX_FILE_BYTES

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SWYNEX AI Resume Analyzer API",
    description="Resume analysis API with persistent analysis records.",
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "service": "AI Resume Analyzer API", "database": "configured"}


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(..., min_length=30, max_length=20000),
    job_title: str | None = Form(default=None, max_length=120),
    db: Session = Depends(get_db),
):
    try:
        content = await resume.read(MAX_FILE_BYTES + 1)
        if len(content) > MAX_FILE_BYTES:
            raise HTTPException(status_code=413, detail="File exceeds the 5 MB upload limit.")
        filename = resume.filename or "resume"
        resume_text = extract_text(filename, content)
        result = analyze_resume(resume_text, job_description, filename)

        record = Analysis(
            id=result["analysis_id"],
            filename=filename,
            job_title=job_title.strip() if job_title and job_title.strip() else None,
            match_score=result["match_score"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            resume_skills=result["resume_skills"],
            job_skills=result["job_skills"],
            suggestions=result["suggestions"],
        )
        db.add(record)
        db.commit()
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await resume.close()


@app.post(
    "/api/v1/analyses",
    response_model=AnalysisRecordRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Analysis records"],
)
def create_analysis(payload: AnalysisCreate, db: Session = Depends(get_db)):
    record = Analysis(id=str(uuid4()), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/api/v1/analyses", response_model=list[AnalysisRecordRead], tags=["Analysis records"])
def list_analyses(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(Analysis).order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()


@app.get("/api/v1/analyses/{analysis_id}", response_model=AnalysisRecordRead, tags=["Analysis records"])
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    record = db.get(Analysis, analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return record


@app.put("/api/v1/analyses/{analysis_id}", response_model=AnalysisRecordRead, tags=["Analysis records"])
def replace_analysis(analysis_id: str, payload: AnalysisCreate, db: Session = Depends(get_db)):
    record = db.get(Analysis, analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    for field, value in payload.model_dump().items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


@app.delete(
    "/api/v1/analyses/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Analysis records"],
)
def delete_analysis(analysis_id: str, db: Session = Depends(get_db)):
    record = db.get(Analysis, analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    db.delete(record)
    db.commit()
    return None
