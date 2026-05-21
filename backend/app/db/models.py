from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(50), default="INFO", index=True)
    source = Column(String(100), index=True) # e.g. "dify", "n8n", "frontend"
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<SystemLog [{self.level}] {self.source}: {self.message}>"


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    task_id = Column(String(64), primary_key=True, index=True)
    niche = Column(String(255), nullable=False)
    language = Column(String(32), default="en")
    status = Column(String(64), default="awaiting_topic_approval", index=True)
    current_step = Column(String(64), default="viral_detection")
    error_message = Column(Text, nullable=True)
    outputs = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)


class WorkflowEvent(Base):
    __tablename__ = "workflow_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(64), index=True, nullable=False)
    event_type = Column(String(64), index=True, nullable=False)
    step = Column(String(64), nullable=True)
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
