# Project Architecture

## Product idea
A web application that compares a resume with a target job description and returns an explainable skill-match report. The current MVP uses deterministic keyword matching from a curated dictionary; it is not a trained AI model or a hiring decision tool.

## Architecture
```text
React + Vite UI -> FastAPI REST API -> PDF/DOCX text parser -> Skill analyzer -> JSON response -> Results UI
```

## Data model: AnalysisResponse
- `analysis_id`: unique request ID
- `filename`: uploaded filename
- `match_score`: integer from 0 to 100
- `matched_skills`: skills detected in both documents
- `missing_skills`: job-description skills not detected in the resume
- `resume_skills`, `job_skills`: detected skill lists
- `suggestions`: improvement prompts

No database is used; uploaded content is processed in memory.

## API routes
| Method | Route | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/analyze` | Upload resume and job description |

POST fields: `resume` (PDF/DOCX), `job_description` (30–20,000 characters), optional `job_title`.

## Frontend screens
1. Input screen: upload resume, enter optional role and job description.
2. Results screen: score, matched skills, skills to address, resume skills and suggestions.
3. Error states: unsupported/oversized/unreadable files and validation/network errors.

## Privacy and security
The MVP does not persist resumes or analysis history. Production deployment should add HTTPS, strict CORS, rate limiting, malware scanning, secure logging, monitoring and retention/deletion controls. Never commit personal resumes or secrets.

## Future scope
Semantic matching with embeddings, optional LLM suggestions with consent, PDF report export, accounts and saved history, expanded skill taxonomy, multilingual support, accessibility and integration tests.
