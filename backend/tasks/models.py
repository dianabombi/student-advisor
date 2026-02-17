"""
Database models for Celery tasks
Defines SQLAlchemy models without importing from main
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class ScrapingStatus(str, enum.Enum):
    PENDING = "PENDING"  # Database has both 'pending' and 'PENDING'
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    pending = "pending"  # Lowercase variant
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    website_url = Column(String)
    jurisdiction_id = Column(Integer, ForeignKey("jurisdictions.id"))
    type = Column(String)
    is_active = Column(Boolean, default=True)


class UniversityScrapingStatus(Base):
    __tablename__ = "university_scraping_status"
    
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"), unique=True)
    scraping_status = Column(Enum(ScrapingStatus), default=ScrapingStatus.PENDING)
    last_scraped_at = Column(DateTime)
    pages_scraped = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UniversityContent(Base):
    __tablename__ = "university_content"
    
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    url = Column(String, nullable=False)
    title = Column(String)
    content = Column(Text)
    content_type = Column(String)
    language = Column(String)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
