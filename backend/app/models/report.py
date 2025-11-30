"""
Report model
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Report(Base):
    """Report model"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False, index=True)
    title = Column(String, nullable=True)
    generated_text = Column(Text, nullable=True)  # LLM summary
    sections = Column(JSON, nullable=True)  # structured sections
    score = Column(Integer, nullable=True)  # risk score 1-10
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    scan = relationship("Scan", back_populates="reports")












