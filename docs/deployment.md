# Deployment guide — Render

This repository uses a Render Blueprint (`render.yaml`) to describe the frontend, API and database.

## Deploy

1. Push the latest repository changes to GitHub.
2. Sign in to [Render](https://render.com/).
3. Choose **New → Blueprint**.
4. Connect GitHub and select `Avishekchaudhary01/SWYNEX-AI-Resume-Analyzer`.
5. Select the `main` branch and confirm the Blueprint file is `render.yaml`.
6. Review the three resources before applying: API web service, frontend static site and PostgreSQL database.
7. Apply the Blueprint and wait for all services to finish their first deployment.
8. Open the frontend static site URL and test the complete upload → analysis → results → saved history flow.
9. Open `<BACKEND_URL>/api/v1/health`; it should return JSON with `"status": "ok"` and `"database": "connected"`.
10. Copy the real frontend URL and backend URL into the Project links section of the root README. Do not publish guessed URLs as live links.

## Resource and cost warning

The Blueprint deliberately selects Render's free plans to avoid automatically opting into paid services. Render documents that free web services can spin down when idle and free PostgreSQL databases expire 30 days after creation. Free Postgres is therefore suitable only for a short-lived demo; do not store important data there. Upgrade the database or choose another persistent database before relying on saved analyses.

Check current terms: [Render free instance limitations](https://render.com/docs/free) and [Render Blueprint reference](https://render.com/docs/blueprint-spec).

## Environment wiring

The Blueprint connects services using Render-provided environment variables:
- API `DATABASE_URL` receives the PostgreSQL connection string.
- API `FRONTEND_ORIGINS` receives the deployed static site's public URL.
- Frontend `VITE_API_URL` receives the deployed API's public URL.

No database credentials are committed to this repository.

## Post-deployment verification

- Frontend loads over HTTPS.
- API health endpoint returns HTTP 200.
- API docs load at `/docs`.
- A test PDF/DOCX under 5 MB can be analyzed.
- Match score and skill groups appear in the frontend.
- The report appears in recent analysis history after refresh.
- An invalid file type and an oversized file are rejected.
- The browser console has no CORS or failed-request errors.

Use a synthetic resume for testing. Never upload another person's resume without permission.
