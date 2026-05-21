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
