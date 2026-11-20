# SWYNEX AI Resume Analyzer — Task 2 Architecture

## 1. Product overview
A web application that compares a resume with a target job description. It extracts document text, detects skills, calculates a transparent overlap score, and returns matched skills, missing skills, and suggestions. Task 2 adds persistence for analysis records.

**MVP limitation:** Skill detection uses a curated keyword dictionary and deterministic matching. It is not a trained AI model or a hiring decision tool.

## 2. System architecture
```text
React + Vite Frontend
       | REST / multipart upload
       v
FastAPI Routes + Pydantic Validation
       |
       +--> Resume Parser (PDF/DOCX)
       |
       +--> Skill Analyzer
       |
       +--> Analysis CRUD Service
                  |
                  v
           SQLAlchemy ORM
                  |
                  v
             SQLite DB
       |
       v
 JSON response / saved analysis records
```

## 3. Database model
### Analysis
| Column | Type | Rules |
|---|---|---|
| id | VARCHAR(36) | Primary key, UUID |
| filename | VARCHAR(255) | Required |
| job_title | VARCHAR(120) | Optional |
| match_score | INTEGER | 0–100, database check constraint |
| matched_skills | JSON | Required list |
| missing_skills | JSON | Required list |
| resume_skills | JSON | Required list |
| job_skills | JSON | Required, at least one skill |
| suggestions | JSON | Required list |
| created_at | DATETIME | Set on creation |
| updated_at | DATETIME | Updated on modification |

The database stores analysis metadata and skill lists, not the uploaded resume bytes or extracted resume text. SQLite is the default local database; configure `DATABASE_URL` to change the connection string.

## 4. API routes
Base path: `/api/v1`

| Method | Route | Behavior |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze PDF/DOCX and automatically persist the result |
| POST | `/analyses` | Create a validated analysis resource |
| GET | `/analyses` | List records with pagination |
| GET | `/analyses/{id}` | Retrieve one record |
| PUT | `/analyses/{id}` | Replace a record with a validated payload |
| DELETE | `/analyses/{id}` | Delete a record |

### Validation
- Filename is required and limited to 255 characters.
- Match score must be between 0 and 100.
- Skill arrays have size limits and cannot contain blank or duplicate values.
- Matched skills must exist in both the resume and job skill lists.
- Missing skills must exist in the job skill list and cannot also be matched.
- Match score must equal the calculated matched-skill percentage.
- Job skill list and suggestions cannot be empty.
- Invalid request bodies return 422; unknown record IDs return 404.

## 5. Frontend screens
1. Analyzer form: PDF/DOCX upload, optional role, job description.
2. Results: score, matched skills, missing skills, detected skills, suggestions.
3. Error states: invalid/oversized/unreadable file, invalid fields, and API errors.

## 6. Security and privacy
The app does not retain resume file bytes or extracted resume text. It persists analysis metadata and skill lists. Before production, add authentication/authorization, HTTPS, strict CORS, rate limiting, malware scanning, secure logging, retention/deletion controls, backups and monitoring. Do not commit local database files or personal documents.

## 7. Tests
The backend test suite covers skill detection, score calculation, API create/read/list/update/delete behavior, and invalid resource payloads. Tests use a temporary in-memory SQLite database so they do not modify the developer's local database.

## 8. Future improvements
Semantic matching with embeddings, optional LLM suggestions with consent, user accounts, exportable reports, expanded skill taxonomy, multilingual parsing, accessibility and deployment automation.
