"""
Entity model
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class EntityType(str, enum.Enum):
    """Entity type enum"""
    DOMAIN = "domain"
    SUBDOMAIN = "subdomain"
    IP = "ip"
    EMAIL = "email"
    URL = "url"
    CERTIFICATE = "certificate"
    PERSON = "person"
    ACCOUNT = "account"


class Entity(Base):
    """Entity model"""
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=True, index=True)
    type = Column(SQLEnum(EntityType), nullable=False, index=True)
    canonical_value = Column(String, nullable=False, index=True)
    # NOTE: 'metadata' is a reserved attribute name in SQLAlchemy declarative models.
    # Use a safe attribute name while keeping the DB column name as 'metadata'.
    metadata_json = Column("metadata", JSON, nullable=True)  # raw info from sources
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    scan = relationship("Scan", back_populates="entities")
    findings = relationship("Finding", back_populates="entity")





