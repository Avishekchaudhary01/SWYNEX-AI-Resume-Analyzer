# Task 3 — Frontend Integration

## Integration flow
1. The React/Vite client accepts PDF or DOCX resumes up to 5 MB and collects an optional target role plus job description.
2. It sends multipart form data to `POST /api/v1/analyze`.
3. FastAPI extracts document text, analyzes skill overlap, persists the analysis record in SQLite, and returns the report.
4. The UI displays the score, matched skills, missing skills, detected resume skills, and suggestions.
5. The client loads recent saved reports from `GET /api/v1/analyses?skip=0&limit=5`.
6. The header checks `GET /api/v1/health` to show backend availability.

## Implemented UI states
- Idle form and file selection.
- Loading state with disabled submit button and spinner.
- Client-side validation for file type, 5 MB file size, and job-description length.
- API/network error feedback.
- Recent-history loading, error, empty, and success states.
- Successful analysis report with skill groups and suggestions.

## Configuration
Copy `.env.example` to `.env` inside the frontend folder. Set `VITE_API_URL` to the FastAPI origin. Restart Vite after changing environment variables.

## Run locally
Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`

Frontend: `cd frontend && npm install && npm run dev`

Open the Vite URL (usually `http://localhost:5173`). FastAPI CORS must allow this origin; the backend default is `http://localhost:5173`.

## Limitation
The matching engine is a limited dictionary-based keyword matcher, not a trained AI model. Saved history contains analysis metadata and skill lists, not the uploaded resume bytes or extracted text.
