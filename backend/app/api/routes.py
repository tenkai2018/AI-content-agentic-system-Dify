from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Any, Optional

from app.db.session import get_db
from app.db.repository import (
    append_workflow_event,
    create_log,
    create_workflow_run,
    get_logs,
    get_workflow_events,
    get_workflow_run,
    update_workflow_run,
)

router = APIRouter(prefix="/api", tags=["Logging & System Activities"])

class LogCreateRequest(BaseModel):
    level: str = Field(default="INFO", description="Log level: INFO, WARNING, ERROR")
    source: str = Field(..., description="Source of the log: dify, n8n, frontend")
    message: str = Field(..., description="Log message")
    details: Optional[dict] = Field(None, description="Additional context data")

class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    level: str
    source: str
    message: str
    details: Optional[dict]
    created_at: datetime


class StartWorkflowRequest(BaseModel):
    niche: str = Field(..., min_length=2, max_length=255)
    language: str = Field(default="en", min_length=2, max_length=16)
    keywords: list[str] = Field(default_factory=list)


class ApproveRequest(BaseModel):
    task_id: str
    step: str = Field(..., pattern="^(topic|script|thumbnail|assets)$")
    approved: bool
    selected_item: Optional[dict[str, Any]] = None


class WorkflowStatusResponse(BaseModel):
    task_id: str
    status: str
    niche: str
    language: str
    error_message: Optional[str] = None
    outputs: dict[str, Any]


def _mock_research_result(niche: str, keywords: list[str]) -> dict[str, Any]:
    seed = " | ".join(keywords) if keywords else niche
    videos = [
        {
            "video_id": f"vid-{i}",
            "title": f"{seed} growth strategy #{i}",
            "channel": f"Channel {i}",
            "thumbnail_url": f"https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg?i={i}",
            "video_views": 100000 + (i * 17500),
            "channel_average_views": 25000 + (i * 3000),
        }
        for i in range(1, 6)
    ]
    for video in videos:
        video["outlier_score"] = round((video["video_views"] / video["channel_average_views"]) * 100, 2)
    top = sorted(videos, key=lambda v: v["outlier_score"], reverse=True)[0]
    return {"videos": videos, "top_recommended_topic": top}


def _next_state_after_approval(run_status: str, step: str, approved: bool) -> tuple[str, str, str | None]:
    if not approved:
        return ("failed", "stopped", f"{step.title()} rejected by user.")

    if run_status == "awaiting_topic_approval" and step == "topic":
        return ("awaiting_script_approval", "script_writing", None)
    if run_status == "awaiting_script_approval" and step == "script":
        return ("awaiting_thumbnail_approval", "thumbnail_brief", None)
    if run_status == "awaiting_thumbnail_approval" and step == "thumbnail":
        return ("awaiting_assets_approval", "asset_generation", None)
    if run_status == "awaiting_assets_approval" and step == "assets":
        return ("completed", "linkedin_repurposing", None)
    return ("failed", "stopped", "Invalid approval step for current state.")

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "service": "System Logging API"
    }

@router.post("/logs", response_model=LogResponse)
async def add_log(request: LogCreateRequest, db: Session = Depends(get_db)):
    log_entry = create_log(
        db=db,
        level=request.level,
        source=request.source,
        message=request.message,
        details=request.details
    )
    return log_entry

@router.get("/logs", response_model=list[LogResponse])
async def list_logs(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    logs = get_logs(db=db, limit=limit, offset=offset)
    return logs


@router.post("/workflow/start", response_model=WorkflowStatusResponse)
async def start_workflow(request: StartWorkflowRequest, db: Session = Depends(get_db)):
    task_id = str(uuid4())
    research = _mock_research_result(request.niche, request.keywords)
    outputs = {
        "viral_detection_result": research,
        "selected_topic": research.get("top_recommended_topic"),
    }
    run = create_workflow_run(
        db=db,
        task_id=task_id,
        niche=request.niche,
        language=request.language,
        status="awaiting_topic_approval",
        current_step="viral_detection",
        outputs=outputs,
    )
    append_workflow_event(
        db=db,
        task_id=task_id,
        event_type="run_started",
        step="viral_detection",
        payload={"niche": request.niche, "keywords": request.keywords},
    )
    append_workflow_event(
        db=db,
        task_id=task_id,
        event_type="approval_required",
        step="topic",
        payload={"status": run.status},
    )
    return WorkflowStatusResponse(
        task_id=run.task_id,
        status=run.status,
        niche=run.niche,
        language=run.language,
        error_message=run.error_message,
        outputs=run.outputs or {},
    )


@router.get("/status/{task_id}", response_model=WorkflowStatusResponse)
async def get_status(task_id: str, db: Session = Depends(get_db)):
    run = get_workflow_run(db=db, task_id=task_id)
    if not run:
        raise HTTPException(status_code=404, detail="Task not found")
    return WorkflowStatusResponse(
        task_id=run.task_id,
        status=run.status,
        niche=run.niche,
        language=run.language,
        error_message=run.error_message,
        outputs=run.outputs or {},
    )


@router.post("/approve", response_model=WorkflowStatusResponse)
async def approve(request: ApproveRequest, db: Session = Depends(get_db)):
    run = get_workflow_run(db=db, task_id=request.task_id)
    if not run:
        raise HTTPException(status_code=404, detail="Task not found")

    new_status, new_step, error_message = _next_state_after_approval(run.status, request.step, request.approved)
    outputs = dict(run.outputs or {})

    if request.step == "topic" and request.approved:
        selected = request.selected_item or outputs.get("selected_topic")
        outputs["selected_topic"] = selected
        outputs["script_result"] = {
            "hook": "You are leaving massive attention on the table.",
            "full_script_text": "Identify pain -> missed opportunity -> outcome -> visual preview.",
        }
    elif request.step == "script" and request.approved:
        outputs["thumbnail_brief"] = {
            "concept": "Operator with analytics dashboard and clear promise text.",
            "text_overlay": "Operational Clarity Wins",
            "avoid": ["cluttered layout", "more than 5 words", "copycat thumbnail"],
        }
    elif request.step == "thumbnail" and request.approved:
        outputs["assets_result"] = {
            "scenes": [
                {"scene": 1, "image_url": "https://picsum.photos/640/360?scene=1", "audio_url": "/audio/scene1.mp3"},
                {"scene": 2, "image_url": "https://picsum.photos/640/360?scene=2", "audio_url": "/audio/scene2.mp3"},
            ],
            "manifest_path": "remotion_app/public/assets/generated/mock/manifest.json",
        }
    elif request.step == "assets" and request.approved:
        outputs["video_result"] = {"output_path": "remotion_app/public/output_mock.mp4"}
        outputs["linkedin_posts"] = {
            "personal_story": "Post 1...",
            "strong_opinion": "Post 2...",
            "step_by_step": "Post 3...",
            "question_hook": "Post 4...",
            "data_insight": "Post 5...",
            "failure_lesson": "Post 6...",
        }

    run = update_workflow_run(
        db=db,
        run=run,
        status=new_status,
        current_step=new_step,
        outputs=outputs,
        error_message=error_message,
    )

    append_workflow_event(
        db=db,
        task_id=run.task_id,
        event_type="step_completed" if request.approved else "run_failed",
        step=request.step,
        payload={"approved": request.approved},
    )

    if run.status.startswith("awaiting_"):
        append_workflow_event(
            db=db,
            task_id=run.task_id,
            event_type="approval_required",
            step=run.status.replace("awaiting_", "").replace("_approval", ""),
            payload={"status": run.status},
        )
    elif run.status == "completed":
        append_workflow_event(
            db=db,
            task_id=run.task_id,
            event_type="run_completed",
            step="linkedin_repurposing",
            payload={},
        )

    return WorkflowStatusResponse(
        task_id=run.task_id,
        status=run.status,
        niche=run.niche,
        language=run.language,
        error_message=run.error_message,
        outputs=run.outputs or {},
    )


@router.get("/workflow/{task_id}/history")
async def workflow_history(task_id: str, db: Session = Depends(get_db)):
    run = get_workflow_run(db=db, task_id=task_id)
    if not run:
        raise HTTPException(status_code=404, detail="Task not found")
    events = get_workflow_events(db=db, task_id=task_id)
    return {
        "task_id": task_id,
        "events": [
            {
                "id": e.id,
                "event_type": e.event_type,
                "step": e.step,
                "payload": e.payload or {},
                "created_at": e.created_at,
            }
            for e in events
        ],
    }


@router.get("/workflow/{task_id}/artifacts")
async def workflow_artifacts(task_id: str, db: Session = Depends(get_db)):
    run = get_workflow_run(db=db, task_id=task_id)
    if not run:
        raise HTTPException(status_code=404, detail="Task not found")
    outputs = run.outputs or {}
    return {
        "task_id": task_id,
        "assets_result": outputs.get("assets_result"),
        "video_result": outputs.get("video_result"),
        "linkedin_posts": outputs.get("linkedin_posts"),
    }
