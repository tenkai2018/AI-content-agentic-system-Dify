import os

os.environ["DATABASE_URL"] = "sqlite:///./test_app.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Base
from app.db.session import get_db
from app.main import app


def _build_client():
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
    client = TestClient(app)
    return client


def test_workflow_end_to_end_happy_path():
    client = _build_client()

    start_res = client.post(
        "/api/workflow/start",
        json={"niche": "ai automation", "language": "en", "keywords": ["ai", "ops"]},
    )
    assert start_res.status_code == 200
    start_body = start_res.json()
    task_id = start_body["task_id"]
    assert start_body["status"] == "awaiting_topic_approval"
    assert "viral_detection_result" in start_body["outputs"]

    res_topic = client.post("/api/approve", json={"task_id": task_id, "step": "topic", "approved": True})
    assert res_topic.status_code == 200
    assert res_topic.json()["status"] == "awaiting_script_approval"

    res_script = client.post("/api/approve", json={"task_id": task_id, "step": "script", "approved": True})
    assert res_script.status_code == 200
    assert res_script.json()["status"] == "awaiting_thumbnail_approval"

    res_thumb = client.post("/api/approve", json={"task_id": task_id, "step": "thumbnail", "approved": True})
    assert res_thumb.status_code == 200
    assert res_thumb.json()["status"] == "awaiting_assets_approval"

    res_assets = client.post("/api/approve", json={"task_id": task_id, "step": "assets", "approved": True})
    assert res_assets.status_code == 200
    assert res_assets.json()["status"] == "completed"

    status_res = client.get(f"/api/status/{task_id}")
    assert status_res.status_code == 200
    status_body = status_res.json()
    assert status_body["status"] == "completed"
    assert "video_result" in status_body["outputs"]
    assert "linkedin_posts" in status_body["outputs"]

    history_res = client.get(f"/api/workflow/{task_id}/history")
    assert history_res.status_code == 200
    events = history_res.json()["events"]
    assert any(e["event_type"] == "run_started" for e in events)
    assert any(e["event_type"] == "run_completed" for e in events)

    artifacts_res = client.get(f"/api/workflow/{task_id}/artifacts")
    assert artifacts_res.status_code == 200
    artifacts = artifacts_res.json()
    assert artifacts["video_result"] is not None

    app.dependency_overrides.clear()


def test_workflow_reject_fails():
    client = _build_client()
    start_res = client.post(
        "/api/workflow/start",
        json={"niche": "ai automation", "language": "en", "keywords": ["ai"]},
    )
    task_id = start_res.json()["task_id"]

    reject_res = client.post("/api/approve", json={"task_id": task_id, "step": "topic", "approved": False})
    assert reject_res.status_code == 200
    reject_body = reject_res.json()
    assert reject_body["status"] == "failed"
    assert "rejected" in (reject_body["error_message"] or "").lower()

    app.dependency_overrides.clear()
