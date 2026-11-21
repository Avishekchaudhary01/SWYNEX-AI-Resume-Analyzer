# SWYNEX AI Resume Analyzer

A full-stack resume analysis application that compares a PDF/DOCX resume with a job description and produces an explainable skill-overlap report.

**Project status:** Full-stack source and deployment configuration are in GitHub. A live deployment and real application screenshots still need to be created from the hosting dashboard / a running browser session.

> **Important:** This MVP uses a curated keyword dictionary and deterministic overlap scoring. It is not a trained AI model, does not understand every synonym or context, and must not be used as a hiring decision system.

## Project links

- **GitHub repository:** https://github.com/Avishekchaudhary01/SWYNEX-AI-Resume-Analyzer
- **Live application:** Not deployed yet — follow [deployment instructions](docs/deployment.md), then replace this line with the actual frontend URL.
- **Backend API:** Not deployed yet — replace this line with the actual API URL after deployment.
- **API documentation:** Once deployed, open `<BACKEND_URL>/docs`.

## Features

- Upload PDF and DOCX resumes (maximum 5 MB).
- Paste a job description and optionally enter a target role.
- Extract text from documents using PyMuPDF and python-docx.
- Calculate a transparent keyword-overlap score.
- Display matched skills, missing skills, detected resume skills and improvement suggestions.
- Save analysis metadata and results to a relational database.
- Browse recent analysis history.
- Provide loading, validation, empty, network-error and API-error states.
- Expose validated REST endpoints for creating, reading, updating and deleting analysis records.
- Support local SQLite and deployment PostgreSQL configurations.

## Screenshots

Real screenshots should be captured after running the application and saved in `docs/screenshots/`. Do not use sample resumes containing personal information.

Suggested captures:
1. `app-home.png` — upload form and job-description input.
2. `analysis-results.png` — score, matched skills, missing skills and suggestions.
3. `analysis-history.png` — recent saved analyses.

See [screenshot instructions](docs/screenshots/README.md). Screenshots are not included yet because a real browser run has not been performed in this environment.

## Architecture

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | SQLite locally; PostgreSQL for hosted deployment |
| ORM / validation | SQLAlchemy 2.x, Pydantic |
| Resume parsing | PyMuPDF, python-docx |
| Testing / CI | pytest, GitHub Actions |
| Hosting blueprint | Render |

### Request flow

1. The user selects a PDF/DOCX file and enters a job description.
2. React sends multipart form data to `POST /api/v1/analyze`.
3. FastAPI validates the request and extracts document text in memory.
4. The analysis service detects supported skills and calculates keyword overlap.
5. The API stores analysis metadata and skill lists in the configured database.
6. React displays the score, skill groups, suggestions and recent history.

## Run locally

### Requirements

- Python 3.10 or newer
- Node.js 18 or newer and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Avishekchaudhary01/SWYNEX-AI-Resume-Analyzer.git
cd SWYNEX-AI-Resume-Analyzer
```

### 2. Start the backend

Windows PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

macOS / Linux:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at http://127.0.0.1:8000.

- Health: http://127.0.0.1:8000/api/v1/health
- Interactive API docs: http://127.0.0.1:8000/docs

SQLite is used by default and creates `resume_analyzer.db` in the backend working directory.

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
```

Create `.env` in the frontend folder:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Then start Vite:

```bash
npm run dev
```

Open http://localhost:5173.

The backend allows `http://localhost:5173` by default. For a different frontend origin, set `FRONTEND_ORIGINS` on the backend to a comma-separated list of trusted origins.

### 4. Run backend tests

From the repository root:

```bash
cd backend
pip install -r requirements.txt
pytest
```

The GitHub Actions workflow also builds the frontend and runs the backend test suite on pushes and pull requests.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health` | Checks API and database connectivity |
| POST | `/api/v1/analyze` | Analyze a resume upload and save its result |
| POST | `/api/v1/analyses` | Create a validated analysis record |
| GET | `/api/v1/analyses` | List records; supports `skip` and `limit` |
| GET | `/api/v1/analyses/{id}` | Retrieve one record |
| PUT | `/api/v1/analyses/{id}` | Replace a record after validation |
| DELETE | `/api/v1/analyses/{id}` | Delete a record |

## Scoring

```
match score = (matched job-description skills / detected job-description skills) × 100
```

The score is a simple keyword-overlap indicator. It does not measure a candidate's ability, seniority, experience quality or hiring probability.

## Deployment

A Render Blueprint is included at the repository root:

```
render.yaml
```

It describes a Python API service, a React static site and a PostgreSQL database. Follow [docs/deployment.md](docs/deployment.md) to deploy and obtain the live URLs.

**Free-tier warning:** Render's free PostgreSQL databases expire 30 days after creation. Upgrade or use another persistent database before storing data you need to keep. Free web services may sleep when idle. Review current hosting terms and pricing before choosing a paid plan.

## Privacy and security notes

- Uploaded resume bytes and extracted resume text are processed in memory; they are not intentionally stored in the database.
- Analysis metadata, detected skills and suggestions are persisted.
- Do not commit real resumes, database files, API keys or other personal data.
- Before production use, add authentication/authorization, rate limiting, upload malware scanning, retention/deletion controls, monitoring and a formal privacy policy.
- The score is informational only and should not be used for automated hiring decisions.

## Internship work

Built and extended as a learning project for the SWYNEX Internship:
- Task 1: Product and system architecture.
- Task 2: Backend API and database.
- Task 3: Frontend integration.
- Task 4: Deployment preparation and documentation.

---

**Maintainer:** Avishek Chaudhary  
**Repository:** [Avishekchaudhary01/SWYNEX-AI-Resume-Analyzer](https://github.com/Avishekchaudhary01/SWYNEX-AI-Resume-Analyzer)
