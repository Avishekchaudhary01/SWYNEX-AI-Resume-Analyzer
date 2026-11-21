# SWYNEX AI Resume Analyzer

A full-stack web application that compares a resume with a job description and returns an explainable skill-match report. Task 2 adds a persistent SQLite database and validated CRUD endpoints for analysis records.

> **MVP note:** Skill detection currently uses a curated keyword dictionary and deterministic scoring. It is not a trained AI model and does not predict hiring outcomes.

## Features
- PDF/DOCX resume upload (5 MB maximum)
- Job description input and optional target role
- Text extraction with PyMuPDF and python-docx
- Explainable skill-match score, matched/missing skills and suggestions
- FastAPI backend with validated analysis-record CRUD endpoints
- SQLAlchemy ORM and SQLite persistence
- React + Vite frontend
- Unit tests for analysis and database/API behavior

## Technology
| Layer | Technology |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy 2.x |
| Validation | Pydantic |
| Document parsing | PyMuPDF, python-docx |
| Testing | pytest, TestClient |

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
Health check: http://127.0.0.1:8000/api/v1/health

By default, SQLite creates `backend/resume_analyzer.db` when the API starts. To change the database location, set `DATABASE_URL` before starting the backend. Example:
```env
DATABASE_URL=sqlite:///./resume_analyzer.db
FRONTEND_ORIGIN=http://localhost:5173
```

### Frontend
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite (usually http://localhost:5173). The frontend defaults to `http://127.0.0.1:8000` for its API. Ensure the backend CORS setting allows `http://localhost:5173`.

## Frontend integration (Task 3)
The React frontend submits resumes to `POST /api/v1/analyze`, displays the analysis report, checks backend health through `GET /api/v1/health`, and loads recent saved reports from `GET /api/v1/analyses?skip=0&limit=5`. It includes file validation, loading indicators, API error feedback, and history loading/error/empty states.

Configure the API origin in `frontend/.env` using `frontend/.env.example` as a template. The default is `http://127.0.0.1:8000`. Restart Vite after changing environment variables.

See [Task 3 frontend integration notes](docs/task-3-frontend-integration.md).

## API endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health` | API health check |
| POST | `/api/v1/analyze` | Analyze uploaded resume; saves the result to SQLite |
| POST | `/api/v1/analyses` | Create a validated analysis record |
| GET | `/api/v1/analyses` | List records (supports `skip` and `limit`) |
| GET | `/api/v1/analyses/{id}` | Retrieve one record |
| PUT | `/api/v1/analyses/{id}` | Replace a record after validation |
| DELETE | `/api/v1/analyses/{id}` | Delete a record |

The analysis resource validates filename length, score range, unique skill lists, skill relationships, and score consistency. Invalid payloads return HTTP 422; missing records return HTTP 404.

## Run tests
```bash
cd backend
pytest
```

## Scoring
`match score = (matched job-description skills / detected job-description skills) × 100`

This is a keyword-overlap indicator, not a measure of ability or hiring probability. It can miss synonyms and context.

## Privacy and security
- Resume file content is processed in memory and is not stored in the database.
- Analysis metadata and skill lists are stored locally in SQLite.
- Do not commit database files, real resumes, secrets, or personal data.
- Before public deployment, configure HTTPS, strict CORS, rate limiting, malware scanning, access controls, retention/deletion policies and monitoring.

See [docs/architecture.md](docs/architecture.md) for data models and system design.

Created as a learning project for the SWYNEX Internship.
