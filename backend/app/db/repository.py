from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import SystemLog, WorkflowEvent, WorkflowRun

def create_log(db: Session, level: str, source: str, message: str, details: dict = None) -> SystemLog:
    log_entry = SystemLog(
        level=level,
        source=source,
        message=message,
        details=details or {},
        created_at=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def get_logs(db: Session, limit: int = 100, offset: int = 0) -> list[SystemLog]:
    return db.query(SystemLog).order_by(SystemLog.created_at.desc()).offset(offset).limit(limit).all()


def create_workflow_run(
    db: Session,
    task_id: str,
    niche: str,
    language: str,
    status: str,
    current_step: str,
    outputs: dict,
) -> WorkflowRun:
    run = WorkflowRun(
        task_id=task_id,
        niche=niche,
        language=language,
        status=status,
        current_step=current_step,
        outputs=outputs,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_workflow_run(db: Session, task_id: str) -> WorkflowRun | None:
    return db.query(WorkflowRun).filter(WorkflowRun.task_id == task_id).first()


def update_workflow_run(
    db: Session,
    run: WorkflowRun,
    status: str,
    current_step: str,
    outputs: dict,
    error_message: str | None = None,
) -> WorkflowRun:
    run.status = status
    run.current_step = current_step
    run.outputs = outputs
    run.error_message = error_message
    run.updated_at = datetime.utcnow()
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def append_workflow_event(
    db: Session,
    task_id: str,
    event_type: str,
    step: str | None,
    payload: dict | None = None,
) -> WorkflowEvent:
    event = WorkflowEvent(
        task_id=task_id,
        event_type=event_type,
        step=step,
        payload=payload or {},
        created_at=datetime.utcnow(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_workflow_events(db: Session, task_id: str) -> list[WorkflowEvent]:
    return (
        db.query(WorkflowEvent)
        .filter(WorkflowEvent.task_id == task_id)
        .order_by(WorkflowEvent.created_at.asc())
        .all()
    )
