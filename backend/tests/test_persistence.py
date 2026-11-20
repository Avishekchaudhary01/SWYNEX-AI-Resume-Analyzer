import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def sample_payload():
    return {
        "filename": "avishek-resume.pdf",
        "job_title": "Python Developer Intern",
        "match_score": 67,
        "matched_skills": ["python", "sql"],
        "missing_skills": ["docker"],
        "resume_skills": ["python", "sql", "react"],
        "job_skills": ["python", "sql", "docker"],
        "suggestions": ["Add project evidence for Docker if you have that experience."],
    }


def test_create_and_read_analysis(client):
    created = client.post("/api/v1/analyses", json=sample_payload())
    assert created.status_code == 201
    record = created.json()
    assert record["match_score"] == 67
    assert record["filename"] == "avishek-resume.pdf"

    fetched = client.get(f"/api/v1/analyses/{record['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == record["id"]


def test_list_update_and_delete_analysis(client):
    created = client.post("/api/v1/analyses", json=sample_payload())
    analysis_id = created.json()["id"]

    listed = client.get("/api/v1/analyses")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated_payload = sample_payload()
    updated_payload["job_title"] = "Backend Developer Intern"
    updated = client.put(f"/api/v1/analyses/{analysis_id}", json=updated_payload)
    assert updated.status_code == 200
    assert updated.json()["job_title"] == "Backend Developer Intern"

    deleted = client.delete(f"/api/v1/analyses/{analysis_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/analyses/{analysis_id}").status_code == 404


def test_validation_rejects_inconsistent_skill_data(client):
    payload = sample_payload()
    payload["matched_skills"] = ["docker"]
    response = client.post("/api/v1/analyses", json=payload)
    assert response.status_code == 422


def test_validation_rejects_out_of_range_score(client):
    payload = sample_payload()
    payload["match_score"] = 150
    response = client.post("/api/v1/analyses", json=payload)
    assert response.status_code == 422
