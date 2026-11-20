import os
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AnalysisResponse
from app.services.analyzer import analyze_resume
from app.services.parser import extract_text, MAX_FILE_BYTES

app = FastAPI(title="SWYNEX AI Resume Analyzer API", description="Explainable resume/job skill matching", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "service": "AI Resume Analyzer API"}

@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze(resume: UploadFile = File(...), job_description: str = Form(..., min_length=30, max_length=20000), job_title: str | None = Form(default=None, max_length=120)):
    _ = job_title
    try:
        content = await resume.read(MAX_FILE_BYTES + 1)
        if len(content) > MAX_FILE_BYTES:
            raise HTTPException(status_code=413, detail="File exceeds the 5 MB upload limit.")
        resume_text = extract_text(resume.filename or "resume", content)
        return analyze_resume(resume_text, job_description, resume.filename or "resume")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await resume.close()
