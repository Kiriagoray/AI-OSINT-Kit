"""
Finding model
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Finding(Base):
    """Finding model"""
    __tablename__ = "findings"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False, index=True)
    source = Column(String, nullable=False)  # whois, shodan, ssl, htb, scraping
    type = Column(String, nullable=False)  # breach, open_port, leaked_creds, suspicious_ssl
    confidence_score = Column(Float, default=0.0)
    raw_result = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    entity = relationship("Entity", back_populates="findings")












