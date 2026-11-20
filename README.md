# SWYNEX AI Resume Analyzer

A full-stack web application that compares a resume with a job description and returns an explainable skill-match report.

> **MVP note:** The current analyzer uses a curated keyword/skill dictionary and deterministic scoring. It is not a trained AI model, does not predict hiring outcomes, and should be used as a resume-improvement aid only.

## Features
- Upload a resume in PDF or DOCX format (5 MB maximum)
- Paste a target job description and optional target role
- Extract document text with PyMuPDF and python-docx
- Detect skills from a configurable skill dictionary
- Calculate a transparent skill-overlap score
- Display matched skills, missing skills, and improvement suggestions
- React + Vite frontend and FastAPI backend
- Unit tests for core analysis logic

## Technology
| Layer | Technology |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| Document parsing | PyMuPDF, python-docx |
| API | REST, JSON, multipart upload |
| Testing | pytest |

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### Frontend
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite (usually http://localhost:5173).

## Run tests
```bash
cd backend
pytest
```

## Scoring
`match score = (matched job-description skills / detected job-description skills) × 100`

This is a keyword-overlap indicator. It does not measure a candidate's ability, experience quality, or probability of getting hired. Keyword matching can miss synonyms and context.

## Privacy and security
- The starter does not save uploaded resumes or extracted text to a database.
- Files are processed in memory and closed after the request.
- Only PDF/DOCX files are accepted; maximum upload size is 5 MB.
- Never commit real resumes, secrets, `.env` files, or personal data.
- Before public deployment, configure strict CORS, HTTPS, rate limiting, malware scanning, and production-grade monitoring.

See [docs/architecture.md](docs/architecture.md) for architecture, data models, API routes and frontend screens.

Created as a learning project for the SWYNEX Internship.
