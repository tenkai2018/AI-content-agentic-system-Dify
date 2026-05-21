from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import SystemLog

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
