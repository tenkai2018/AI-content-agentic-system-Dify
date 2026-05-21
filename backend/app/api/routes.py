from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.session import get_db
from app.db.repository import create_log, get_logs

router = APIRouter(prefix="/api", tags=["Logging & System Activities"])

class LogCreateRequest(BaseModel):
    level: str = Field(default="INFO", description="Log level: INFO, WARNING, ERROR")
    source: str = Field(..., description="Source of the log: dify, n8n, frontend")
    message: str = Field(..., description="Log message")
    details: Optional[dict] = Field(None, description="Additional context data")

class LogResponse(BaseModel):
    id: int
    level: str
    source: str
    message: str
    details: Optional[dict]
    created_at: datetime

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
