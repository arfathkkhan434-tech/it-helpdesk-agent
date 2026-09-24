import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./audit_logs.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True if not DATABASE_URL.startswith("sqlite") else False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TicketAuditLog(Base):
    __tablename__ = "audit_ticket_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(120), nullable=False)
    raw_request = Column(Text, nullable=False)
    actions_taken = Column(Text, nullable=True)
    resolution_status = Column(String(50), default="RESOLVED")
    execution_time_seconds = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def log_ticket(user_email: str, raw_request: str, actions_taken: str, status: str = "RESOLVED", exec_time: float = 0.0):
    db = SessionLocal()
    try:
        entry = TicketAuditLog(
            user_email=user_email,
            raw_request=raw_request,
            actions_taken=actions_taken,
            resolution_status=status,
            execution_time_seconds=exec_time
        )
        db.add(entry)
        db.commit()
    finally:
        db.close()