"""
Scan model
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class ScanStatus(str, enum.Enum):
    """Scan status enum"""
    QUEUED = "queued"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"


class ScanType(str, enum.Enum):
    """Scan type enum"""
    DOMAIN = "domain"
    EMAIL = "email"
    IP = "ip"
    HANDLE = "handle"


class Scan(Base):
    """Scan model"""
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target = Column(String, nullable=False, index=True)
    type = Column(SQLEnum(ScanType), nullable=False)
    status = Column(SQLEnum(ScanStatus), default=ScanStatus.QUEUED, index=True)
    settings = Column(JSON, nullable=True)  # scan modules enabled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    entities = relationship("Entity", back_populates="scan")
    reports = relationship("Report", back_populates="scan")












