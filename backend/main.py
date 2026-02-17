import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean, UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import openai
from services.ocr_service import OCRService, OCRProvider
# from services.ocr_service import classify_document  # DISABLED: Requires ML libraries
from services.cache_service import cache, cached
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
import structlog
from logging_config import setup_logging
import sys

# Validate critical environment variables
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "SECRET_KEY",
    "JWT_SECRET_KEY",
    "DATABASE_URL"
]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# Validate security keys are not defaults
if os.getenv("SECRET_KEY", "").startswith("generate_random"):
    print("ERROR: SECRET_KEY must be changed from default!")
    sys.exit(1)

if os.getenv("JWT_SECRET_KEY", "").startswith("generate_random"):
    print("ERROR: JWT_SECRET_KEY must be changed from default!")
    sys.exit(1)

# Setup structured logging
logger = setup_logging()

# Log application start
logger.info("application_started", version="1.0.0", environment="production")

# Database setup with connection pooling for scalability
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/codex_db")
engine = create_engine(
    DATABASE_URL,
    pool_size=20,              # Base connections per worker (4 workers × 20 = 80 connections)
    max_overflow=10,           # Extra connections when needed (up to 120 total)
    pool_pre_ping=True,        # Verify connection health before using
    pool_recycle=3600,         # Recycle connections after 1 hour
    echo=False                 # Set to True for SQL query logging (debug only)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# OCR Service setup
OCR_PROVIDER = os.getenv("OCR_PROVIDER", "mindee")  # mindee, tesseract, veryfi, klippa
ocr_service = OCRService(provider=OCRProvider(OCR_PROVIDER))

# Models
class Jurisdiction(Base):
    __tablename__ = "jurisdictions"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(2), unique=True, nullable=False)  # SK, CZ, PL, etc.
    name = Column(String(100), nullable=False)  # Slovenská Republika, Česká Republika, etc.
    flag_emoji = Column(String(10))  # 🇸🇰, 🇨🇿, 🇵🇱
    is_active = Column(Boolean, default=True)
    documents = relationship("Document", back_populates="jurisdiction")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='client')  # client, lawyer, admin, partner_lawyer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Trial period fields
    trial_start_date = Column(DateTime, nullable=True)
    trial_end_date = Column(DateTime, nullable=True)
    trial_used = Column(Boolean, default=False)
    subscription_status = Column(String, default='trial')  # trial, active, expired, none
    # Usage tracking fields
    monthly_request_limit = Column(Integer, default=500)
    requests_used_this_month = Column(Integer, default=0)
    # UPL Consent tracking fields (legal protection)
    consent_ai_tool = Column(Boolean, nullable=False, default=False)
    consent_no_advice = Column(Boolean, nullable=False, default=False)
    consent_no_attorney = Column(Boolean, nullable=False, default=False)
    consent_timestamp = Column(DateTime, nullable=True)
    consent_ip_address = Column(String, nullable=True)
    # Version tracking for legal updates
    consent_terms_version = Column(String, default="1.0")
    consent_upl_version = Column(String, default="1.0")
    consent_user_agent = Column(String, nullable=True)
    documents = relationship("Document", back_populates="owner")
    messages = relationship("ChatMessage", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    document_type = Column(String)  # invoice, receipt, tax_form, etc.
    extracted_data = Column(JSON)  # OCR extracted data
    confidence = Column(Integer)  # OCR confidence score
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    jurisdiction_id = Column(Integer, ForeignKey("jurisdictions.id"), nullable=True)  # Link to jurisdiction
    owner = relationship("User", back_populates="documents")
    jurisdiction = relationship("Jurisdiction", back_populates="documents")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="messages")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(String, nullable=False)  # '1month', '6months', '1year', 'trial'
    amount = Column(Integer, nullable=False)  # Amount in EUR
    status = Column(String, default='pending')  # pending, active, expired, cancelled
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_trial = Column(Boolean, default=False)  # Whether this is a trial subscription
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    amount = Column(Integer, nullable=False)  # Amount in EUR
    currency = Column(String, default='EUR')
    status = Column(String, default='pending')  # pending, completed, failed, refunded
    payment_method = Column(String, nullable=True)  # stripe, paypal, bank_transfer, etc.
    transaction_id = Column(String, nullable=True)  # External payment gateway transaction ID
    payment_metadata = Column(JSON, nullable=True)  # Additional payment data (renamed from 'metadata' to avoid SQLAlchemy conflict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")

class UsageHistory(Base):
    __tablename__ = "usage_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    request_type = Column(String(50), nullable=False)
    tokens_used = Column(Integer)
    cost_estimate = Column(Integer)  # Using Integer for cents to avoid float issues
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    price_monthly = Column(Integer)  # In cents
    price_6months = Column(Integer)
    price_yearly = Column(Integer)
    request_limit = Column(Integer)
    features = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    issue_description = Column(Text, nullable=False)
    ai_response = Column(Text)
    logs_analyzed = Column(Integer, default=0)
    errors_found = Column(Integer, default=0)
    status = Column(String(50), default='ai_resolved')
    needs_human = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    user = relationship("User")

# Messaging Models
class Message(Base):
    """Messages between clients and lawyers"""
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    subject = Column(String(500))
    body = Column(Text, nullable=False)
    attachments = Column(JSON, default=[])
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    """User notifications"""
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    action_url = Column(String(500))
    action_label = Column(String(100))
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    related_order_id = Column(Integer, ForeignKey("orders.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

# Marketplace Payment Models
class Transaction(Base):
    """Marketplace payment transactions"""
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_number = Column(String(50), unique=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    type = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)  # In cents
    currency = Column(String(3), default='EUR')
    status = Column(String(20), default='pending')
    payment_method = Column(String(50))
    payment_id = Column(String(255))
    description = Column(Text)
    payment_metadata = Column(JSON)  # Renamed from 'metadata' (SQLAlchemy reserved word)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class Escrow(Base):
    """Escrow holdings for marketplace orders"""
    __tablename__ = "escrow"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    total_amount = Column(Integer, nullable=False)  # In cents
    platform_fee = Column(Integer, nullable=False)
    lawyer_payout = Column(Integer, nullable=False)
    status = Column(String(20), default='held')
    held_at = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime)
    auto_release_at = Column(DateTime)
    notes = Column(Text)

class LawyerWallet(Base):
    """Lawyer earnings and balances"""
    __tablename__ = "lawyer_wallets"
    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), unique=True)
    total_earnings = Column(Integer, default=0)  # In cents
    available_balance = Column(Integer, default=0)
    pending_balance = Column(Integer, default=0)
    total_withdrawn = Column(Integer, default=0)
    currency = Column(String(3), default='EUR')
    updated_at = Column(DateTime, default=datetime.utcnow)

class Withdrawal(Base):
    """Lawyer withdrawal requests"""
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True, index=True)
    withdrawal_number = Column(String(50), unique=True, nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"))
    amount = Column(Integer, nullable=False)  # In cents
    bank_account = Column(String(255), nullable=False)
    status = Column(String(20), default='pending')
    note = Column(Text)
    admin_note = Column(Text)
    approved_by = Column(Integer, ForeignKey("users.id"))
    requested_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime)
    completed_at = Column(DateTime)

class Dispute(Base):
    """Order disputes"""
    __tablename__ = "disputes"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    raised_by = Column(String(10))
    client_id = Column(Integer, ForeignKey("users.id"))
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"))
    reason = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    requested_refund_amount = Column(Integer)
    status = Column(String(20), default='open')
    resolution = Column(Text)
    refund_amount = Column(Integer)
    resolved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

class VisitorTracking(Base):
    """Відстеження відвідувачів сайту"""
    __tablename__ = "visitor_tracking"
    id = Column(Integer, primary_key=True, index=True)
    visitor_fingerprint = Column(String(255), unique=True, index=True, nullable=False)  # MD5 hash of IP + User Agent
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    first_visit = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_visit = Column(DateTime, default=datetime.utcnow, nullable=False)
    visit_count = Column(Integer, default=1)
    traffic_source = Column(String(100), nullable=True)  # google, facebook, direct, etc.
    utm_source = Column(String(255), nullable=True)
    utm_medium = Column(String(255), nullable=True)
    utm_campaign = Column(String(255), nullable=True)
    referrer = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)  # mobile, tablet, desktop
    browser = Column(String(100), nullable=True)
    os = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Якщо зареєструвався
    created_at = Column(DateTime, default=datetime.utcnow)

class PageView(Base):
    """Перегляди сторінок"""
    __tablename__ = "page_views"
    id = Column(Integer, primary_key=True, index=True)
    visitor_fingerprint = Column(String(255), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    page_url = Column(String(500), nullable=False)
    page_title = Column(String(500), nullable=True)
    referrer = Column(Text, nullable=True)
    utm_params = Column(JSON, nullable=True)
    device_type = Column(String(50), nullable=True)
    browser = Column(String(100), nullable=True)
    os = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class MarketingCampaign(Base):
    """Маркетингові кампанії для відстеження витрат та ROI"""
    __tablename__ = "marketing_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String(255), nullable=False)  # Назва кампанії
    utm_campaign = Column(String(255), nullable=True, index=True)  # UTM campaign parameter
    utm_source = Column(String(255), nullable=True, index=True)  # UTM source (google, facebook, etc.)
    utm_medium = Column(String(255), nullable=True)  # UTM medium (cpc, email, social)
    channel = Column(String(100), nullable=True)  # Канал: google_ads, facebook_ads, instagram_ads, linkedin_ads, email, organic
    cost = Column(Integer, default=0)  # Витрати на кампанію в EUR (cents)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)  # Додаткові нотатки
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# MARKETPLACE MODELS
# ============================================

class Lawyer(Base):
    """Lawyer profiles in the marketplace"""
    __tablename__ = "lawyers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Profile
    full_name = Column(String(255), nullable=False)
    title = Column(String(100))  # JUDr., Mgr., etc.
    license_number = Column(String(100), unique=True, nullable=False)
    bar_association = Column(String(255))
    
    # Jurisdiction - CRITICAL for multi-jurisdiction marketplace
    # Lawyer can have licenses in multiple jurisdictions
    # Example: ["SK", "CZ"] means lawyer is licensed in Slovakia and Czech Republic
    # Supported: SK, CZ, PL, EN, DE, FR, ES, IT, UK, RU, HU, AT, RO (expandable)
    jurisdictions = Column(JSON, default=["SK"])  # ["SK", "CZ", "PL"]
    
    # Professional details
    specializations = Column(JSON, default=[])  # ["civil_law", "criminal_law"]
    languages = Column(JSON, default=["sk"])  # ["sk", "en", "de"]
    experience_years = Column(Integer)
    education = Column(Text)
    certifications = Column(Text)
    
    # Contact and location
    office_address = Column(Text)
    city = Column(String(100))
    country = Column(String(2), default='SK')
    phone = Column(String(50))
    website = Column(String(500))
    
    # Pricing
    hourly_rate = Column(Integer)  # In cents
    consultation_fee = Column(Integer)  # In cents
    currency = Column(String(3), default='EUR')
    
    # Profile content
    bio = Column(Text)
    profile_image_url = Column(String(500))
    
    # Status and verification
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_date = Column(DateTime)
    verification_documents = Column(JSON)
    
    # Statistics
    total_cases = Column(Integer, default=0)
    success_rate = Column(Integer)  # Percentage
    average_rating = Column(Integer)  # Stored as int (rating * 100)
    total_reviews = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="lawyer_profile")


class Order(Base):
    """Service orders between users and lawyers"""
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    
    # Parties
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    case_id = Column(Integer, nullable=True)  # Optional reference to legal_cases
    
    # Order details
    service_type = Column(String(100), nullable=False)  # consultation, case_handling, document_review
    description = Column(Text)
    
    # Pricing
    amount = Column(Integer, nullable=False)  # In cents
    currency = Column(String(3), default='EUR')
    payment_status = Column(String(50), default='pending')  # pending, paid, refunded, cancelled
    
    # Status
    status = Column(String(50), default='pending')  # pending, accepted, in_progress, completed, cancelled
    
    # Metadata
    terms_agreed = Column(Boolean, default=False)
    terms_agreed_at = Column(DateTime)
    contract_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    accepted_at = Column(DateTime)
    completed_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", backref="orders")
    lawyer = relationship("Lawyer", backref="orders")


class Review(Base):
    """User reviews and ratings for lawyers"""
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    
    # Parties
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    
    # Review content
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255))
    comment = Column(Text)
    
    # Review aspects (optional detailed ratings)
    professionalism_rating = Column(Integer)  # 1-5
    communication_rating = Column(Integer)  # 1-5
    expertise_rating = Column(Integer)  # 1-5
    value_rating = Column(Integer)  # 1-5
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    
    # Response from lawyer
    lawyer_response = Column(Text)
    lawyer_response_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="reviews_given")
    lawyer = relationship("Lawyer", backref="reviews_received")
    order = relationship("Order", backref="review")


# ============================================
# EDUCATIONAL PLATFORM MODELS
# ============================================

class University(Base):
    """Universities, vocational schools, language schools"""
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    name_local = Column(String(500))
    type = Column(String(50), default='university')  # university, language_school, vocational_school, conservatory, foundation_program
    
    # Location
    city = Column(String(100))
    country = Column(String(2), default='SK')
    address = Column(Text)
    jurisdiction_id = Column(Integer, ForeignKey("jurisdictions.id"), nullable=True)
    
    # Contact & Web
    website_url = Column(String(500))
    logo_url = Column(String(500))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    
    # Info
    description = Column(Text)
    founded_year = Column(Integer)
    student_count = Column(Integer)
    ranking_position = Column(Integer)
    
    # System
    data_container_path = Column(String(500))  # MinIO path
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    programs = relationship("Program", back_populates="university")


class Program(Base):
    """Educational programs offered by universities"""
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    name = Column(String(500), nullable=False)
    name_local = Column(String(500))
    degree_level = Column(String(50), nullable=False)  # bachelor, master, phd, vocational, language_course
    field_of_study = Column(String(200))
    language = Column(String(10), default='sk')
    duration_years = Column(Integer)
    duration_months = Column(Integer)
    tuition_fee = Column(Integer, default=0)  # in EUR cents
    description = Column(Text)
    admission_requirements = Column(JSON)
    application_deadline = Column(DateTime)
    start_date = Column(DateTime)
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    university = relationship("University", back_populates="programs")
    applications = relationship("Application", back_populates="program")


class StudentProfile(Base):
    """Student academic profiles and preferences"""
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Academic Information
    current_education_level = Column(String(50))
    gpa = Column(Integer)  # Stored as integer (GPA * 100)
    graduation_year = Column(Integer)
    field_of_interest = Column(String(200))
    
    # Language Proficiency (JSON)
    language_proficiency = Column(JSON)
    
    # Achievements
    achievements = Column(JSON)  # Array of strings
    extracurricular = Column(JSON)  # Array of strings
    work_experience = Column(Text)
    
    # Documents
    documents = Column(JSON)
    
    # Preferences
    preferred_countries = Column(JSON)  # Array of country codes
    preferred_degree_level = Column(String(50))
    budget_max = Column(Integer)  # in EUR cents
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="student_profile")


class UserUniversity(Base):
    """User's saved/favorite universities"""
    __tablename__ = "user_universities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id", ondelete="CASCADE"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    is_favorite = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", backref="saved_universities")
    university = relationship("University")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'university_id', name='_user_university_uc'),
    )


class UniversityNote(Base):
    """User's notes about universities"""
    __tablename__ = "university_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id", ondelete="CASCADE"), nullable=False)
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="university_notes")
    university = relationship("University")



class Application(Base):
    """Student applications to university programs"""
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    
    # Status
    status = Column(String(50), default='draft')  # draft, submitted, under_review, accepted, rejected
    
    # Documents and AI Assistance
    documents = Column(JSON)
    ai_guidance = Column(JSON)
    ai_chat_history = Column(JSON)
    probability_score = Column(Integer)  # 0-100
    
    # Dates
    submitted_at = Column(DateTime)
    reviewed_at = Column(DateTime)
    decision_date = Column(DateTime)
    
    # Notes
    student_notes = Column(Text)
    admin_notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="applications")
    program = relationship("Program", back_populates="applications")


class UniversityChatSession(Base):
    """Chat sessions with AI about specific universities"""
    __tablename__ = "university_chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    university_id = Column(Integer, ForeignKey("universities.id"))
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    
    # Chat Data
    messages = Column(JSON)  # Array of {role, content, timestamp}
    context = Column(JSON)  # University data context
    
    # Session Info
    session_started = Column(DateTime, default=datetime.utcnow)
    session_ended = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    university = relationship("University")


class RealEstateAgency(Base):
    """Real estate agencies for student housing"""
    __tablename__ = "real_estate_agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    website_url = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    country_code = Column(String(2), nullable=False, index=True)
    description = Column(Text)
    specialization = Column(String(100))  # student_housing, general, luxury
    phone = Column(String(50))
    email = Column(String(255))
    is_verified = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class JobAgency(Base):
    """Job agencies for student part-time work"""
    __tablename__ = "job_agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    website_url = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    country_code = Column(String(2), nullable=False, index=True)
    description = Column(Text)
    specialization = Column(String(100))  # student_jobs, general, seasonal
    phone = Column(String(50))
    email = Column(String(255))
    is_verified = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



# RAG Models
class UniversityContent(Base):
    """Scraped content from university websites"""
    __tablename__ = "university_content"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    url = Column(String, nullable=False)
    title = Column(String)
    content = Column(Text, nullable=False)
    content_type = Column(String(50))  # 'admission', 'programs', 'fees', etc.
    language = Column(String(10))
    scraped_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    university = relationship("University")


class UniversityEmbedding(Base):
    """Vector embeddings for university content"""
    __tablename__ = "university_embeddings"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("university_content.id"))
    embedding = Column(String)  # Will store as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    content = relationship("UniversityContent")


class UniversityScrapingStatus(Base):
    """Tracks scraping status for each university"""
    __tablename__ = "university_scraping_status"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), unique=True)
    last_scraped_at = Column(DateTime)
    scraping_status = Column(String(20), default='pending')  # pending, in_progress, completed, failed
    error_message = Column(Text)
    pages_scraped = Column(Integer, default=0)
    embeddings_generated = Column(Integer, default=0)
    next_scrape_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    university = relationship("University")


class PlatformSettings(Base):
    """Platform configuration settings"""
    __tablename__ = "platform_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    platform_name = Column(String(200), default="Student Platform")
    support_email = Column(String(255), default="support@example.com")
    maintenance_mode = Column(Boolean, default=False)
    openai_api_key = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    # Mandatory UPL consent fields
    consent_ai_tool: bool
    consent_no_advice: bool
    consent_no_attorney: bool


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ChatRequest(BaseModel):
    message: str
    jurisdiction_code: Optional[str] = 'SK'  # Default to Slovakia

class ChatResponse(BaseModel):
    response: str

class JurisdictionResponse(BaseModel):
    id: int
    code: str
    name: str
    flag_emoji: str
    is_active: bool

class DocumentResponse(BaseModel):
    id: int
    filename: str

class SubscriptionCreate(BaseModel):
    plan_type: str  # '1month', '6months', '1year'
    amount: int

class SubscriptionResponse(BaseModel):
    id: int
    plan_type: str
    amount: int
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime

class PaymentCreate(BaseModel):
    plan_type: str
    amount: int

class PaymentResponse(BaseModel):
    id: int
    amount: int
    currency: str
    status: str
    payment_method: Optional[str]
    transaction_id: Optional[str]
    created_at: datetime

class UniversityChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class UniversityChatResponse(BaseModel):
    response: str
    session_id: str



# Initialize FastAPI app
app = FastAPI(title="Student Educational Platform API", version="1.0.0")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timing information and track analytics"""
    start = time.time()
    
    # Get user ID if available (from token)
    user_id = None
    try:
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            from jose import jwt
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email:
                # Quick DB lookup to get user_id
                db = SessionLocal()
                user = db.query(User).filter(User.email == email).first()
                if user:
                    user_id = user.id
                db.close()
    except Exception:
        pass  # Ignore errors in user extraction
    
    # Track page view for analytics (only for GET requests to avoid duplicates)
    if request.method == "GET" and not request.url.path.startswith("/api/owner/analytics"):
        try:
            from middleware.analytics_middleware import AnalyticsMiddleware
            db = SessionLocal()
            await AnalyticsMiddleware.track_page_view(request, db, user_id)
            db.close()
        except Exception as e:
            # Don't fail the request if analytics fails
            print(f"Analytics tracking error: {e}")
    
    # Process request
    try:
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        
        # Log successful request
        logger.info("api_request",
                   method=request.method,
                   path=str(request.url.path),
                   status_code=response.status_code,
                   duration_ms=round(duration, 2),
                   user_id=user_id,
                   client_host=request.client.host if request.client else None)
        
        return response
    except Exception as e:
        duration = (time.time() - start) * 1000
        
        # Log failed request
        logger.error("api_request_error",
                    method=request.method,
                    path=str(request.url.path),
                    duration_ms=round(duration, 2),
                    user_id=user_id,
                    error=str(e),
                    error_type=type(e).__name__)
        raise



# WebSocket Connection Manager
class ConnectionManager:
    """Manages active WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, document_id: int):
        """Accept and store WebSocket connection"""
        await websocket.accept()
        self.active_connections[document_id] = websocket
        print(f"✅ WebSocket connected for document {document_id}")
    
    def disconnect(self, document_id: int):
        """Remove WebSocket connection"""
        if document_id in self.active_connections:
            del self.active_connections[document_id]
            print(f"❌ WebSocket disconnected for document {document_id}")
    
    async def send_progress(self, document_id: int, data: dict):
        """Send progress update to specific document's WebSocket"""
        if document_id in self.active_connections:
            try:
                await self.active_connections[document_id].send_json(data)
            except Exception as e:
                print(f"Error sending to WebSocket {document_id}: {e}")
                self.disconnect(document_id)

# Initialize connection manager
ws_manager = ConnectionManager()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth helpers
def verify_password(plain_password, hashed_password):
    import bcrypt
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password):
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    # Admin users bypass trial checks
    if user.role != 'admin':
        # Check trial status and block access if expired (only for non-admin users)
        from middleware.trial_checker import check_trial_status, get_trial_info
        has_access = await check_trial_status(user, db)
        
        if not has_access:
            trial_info = get_trial_info(user)
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail={
                    "message": "Your trial period has expired. Please subscribe to continue using Student Platform.",
                    "trial_end_date": trial_info.get("trial_end_date"),
                    "subscription_status": "expired",
                    "days_remaining": 0
                }
            )
    
    return user


# Helper for lawyer-only endpoints
async def get_current_lawyer(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user and verify they are a lawyer"""
    if current_user.role != 'lawyer':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only lawyers can access this endpoint / Iba advokáti môžu pristupovať"
        )
    
    # Get lawyer profile
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer profile not found / Profil advokáta nenájdený"
        )
    
    return {
        "id": lawyer.id,
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": lawyer.full_name,
        "is_verified": lawyer.is_verified
    }

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to Student Platform API"}

@app.post("/api/log-error")
async def log_frontend_error(
    error: dict,
    request: Request
):
    """Логувати помилки з frontend"""
    logger.error("frontend_error",
                error_message=error.get('error'),
                stack=error.get('stack'),
                component_stack=error.get('componentStack'),
                user_agent=request.headers.get('user-agent'),
                client_host=request.client.host if request.client else None)
    
    return {"status": "logged"}

@app.get("/api/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user info including admin status.
    Used by frontend to check if user has admin access.
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_admin": current_user.role == "admin",
        "is_active": current_user.is_active,
        "is_verified": getattr(current_user, 'is_verified', False),
        "subscription_status": current_user.subscription_status,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

# Auth endpoints
@app.post("/api/auth/register", response_model=Token)
def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    # Validate email not already registered
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # CRITICAL: Validate ALL consent checkboxes are TRUE (UPL protection)
    if not (user_data.consent_ai_tool and 
            user_data.consent_no_advice and 
            user_data.consent_no_attorney):
        raise HTTPException(
            status_code=400,
            detail="All consent acknowledgments are mandatory. You must accept that Student Platform is an AI tool, does not provide professional advice, and does not create professional relationship."
        )
    
    hashed_password = get_password_hash(user_data.password)
    
    # Calculate trial period dates
    trial_start = datetime.utcnow()
    trial_end = trial_start + timedelta(days=7)
    
    # Get client IP address for consent tracking
    client_ip = request.client.host if request.client else "unknown"
    
    # Get User Agent for legal evidence
    user_agent = request.headers.get('user-agent', 'unknown')
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        trial_start_date=trial_start,
        trial_end_date=trial_end,
        trial_used=True,
        subscription_status='trial',
        # Store UPL consent (legal protection)
        consent_ai_tool=user_data.consent_ai_tool,
        consent_no_advice=user_data.consent_no_advice,
        consent_no_attorney=user_data.consent_no_attorney,
        consent_timestamp=datetime.utcnow(),
        consent_ip_address=client_ip,
        consent_terms_version="1.0",
        consent_upl_version="1.0",
        consent_user_agent=user_agent
    )
    db.add(new_user)
    db.flush()  # Get user ID without committing
    
    # Create trial subscription
    trial_subscription = Subscription(
        user_id=new_user.id,
        plan_type='trial',
        amount=0,
        status='active',
        start_date=trial_start,
        end_date=trial_end,
        is_trial=True
    )
    db.add(trial_subscription)
    
    db.commit()
    db.refresh(new_user)
    
    # Log user registration with consent tracking
    logger.info("user_registered",
                user_id=new_user.id,
                email=new_user.email,
                trial_start=trial_start.isoformat(),
                trial_end=trial_end.isoformat(),
                trial_days=7,
                consent_ai_tool=True,
                consent_no_advice=True,
                consent_no_attorney=True,
                consent_ip=client_ip)
    
    access_token = create_access_token(data={"sub": new_user.email})
    user_response = UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        role=new_user.role or "user",
        created_at=new_user.created_at
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_response}

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(func.lower(User.email) == func.lower(form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning("login_failed", 
                      email=form_data.username,
                      reason="invalid_credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role or "user",
        created_at=user.created_at
    )
    
    # Log successful login
    logger.info("user_login", 
                user_id=user.id, 
                email=user.email,
                role=user.role,
                subscription_status=user.subscription_status)
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_response}

# Jurisdiction endpoints
@app.get("/api/jurisdictions", response_model=List[JurisdictionResponse])
def get_jurisdictions(db: Session = Depends(get_db)):
    """Get all active jurisdictions"""
    jurisdictions = db.query(Jurisdiction).filter(Jurisdiction.is_active == True).all()
    
    # Initialize default jurisdictions if none exist
    if not jurisdictions:
        default_jurisdictions = [
            Jurisdiction(code="SK", name="Slovenská Republika", flag_emoji="🇸🇰", is_active=True),
            Jurisdiction(code="CZ", name="Česká Republika", flag_emoji="🇨🇿", is_active=True),
            Jurisdiction(code="PL", name="Polska", flag_emoji="🇵🇱", is_active=True),
        ]
        db.add_all(default_jurisdictions)
        db.commit()
        jurisdictions = default_jurisdictions
    
    return jurisdictions

# Documents endpoints
@app.get("/api/documents", response_model=List[DocumentResponse])
@limiter.limit("30/minute")
def get_documents(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@app.post("/api/documents/upload")
@limiter.limit("20/minute")
async def upload_document(
    request: Request,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload documents and queue them for async processing with Celery
    """
    from services.doc_processor.tasks import process_document_task
    from services.doc_processor.storage import MinIOStorage
    
    storage = MinIOStorage()
    uploaded_jobs = []
    
    for file in files:
        # Read file content
        content = await file.read()
        
        # Upload to MinIO
        object_name = f"uploads/{current_user.id}/{file.filename}"
        storage.upload_file(content, object_name)
        
        # Create processing job in database
        job = DocumentProcessingJob(
            user_id=current_user.id,
            filename=file.filename,
            raw_object_name=object_name,
            status="pending",
            progress=0
        )
        db.add(job)
        db.flush()  # Get job.document_id
        
        # Queue Celery task for async processing
        task = process_document_task.delay(job.document_id)
        
        # Log document upload
        logger.info("document_upload",
                    user_id=current_user.id,
                    document_id=job.document_id,
                    filename=file.filename,
                    size_bytes=len(content),
                    task_id=task.id)
        
        uploaded_jobs.append({
            "filename": file.filename,
            "job_id": job.document_id,
            "task_id": task.id,
            "status": "pending",
            "message": "Document queued for processing"
        })
    
    db.commit()
    
    return {
        "message": f"{len(files)} file(s) uploaded and queued for processing",
        "jobs": uploaded_jobs
    }


@app.get("/api/documents/{document_id}/progress")
def get_document_progress(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get processing progress for a document
    """
    job = db.query(DocumentProcessingJob).filter(
        DocumentProcessingJob.document_id == document_id,
        DocumentProcessingJob.user_id == current_user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "document_id": document_id,
        "filename": job.filename,
        "status": job.status,
        "progress": job.progress,
        "document_type": job.document_type,
        "confidence": job.confidence,
        "error_message": job.error_message,
        "processed_at": job.processed_at
    }

@app.websocket("/ws/document/{document_id}")
async def websocket_document_progress(
    websocket: WebSocket,
    document_id: int
):
    """
    WebSocket endpoint for real-time document processing progress
    
    Sends updates every 500ms until processing is complete
    """
    # Get database session
    db = SessionLocal()
    
    try:
        # Connect WebSocket
        await ws_manager.connect(websocket, document_id)
        
        # Send updates until processing complete
        while True:
            # Get current job status from database
            job = db.query(DocumentProcessingJob).filter_by(document_id=document_id).first()
            
            if job:
                # Send progress update
                await websocket.send_json({
                    "document_id": document_id,
                    "filename": job.filename,
                    "status": job.status,
                    "progress": job.progress,
                    "document_type": job.document_type,
                    "confidence": job.confidence,
                    "error_message": job.error_message
                })
                
                # If completed or failed, close connection
                if job.status in ['completed', 'failed']:
                    print(f"✅ Document {document_id} processing {job.status}")
                    break
            else:
                # Job not found
                await websocket.send_json({
                    "error": "Job not found",
                    "document_id": document_id
                })
                break
            
            # Wait 500ms before next update
            await asyncio.sleep(0.5)
            
    except WebSocketDisconnect:
        print(f"Client disconnected from document {document_id}")
    except Exception as e:
        print(f"WebSocket error for document {document_id}: {e}")
    finally:
        ws_manager.disconnect(document_id)
        db.close()

@app.get("/api/documents/{document_id}")
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import time
    start_time = time.time()
    
    # Check monthly usage limit
    from middleware.usage_limiter import UsageLimiter
    usage_info = await UsageLimiter.check_monthly_limit(current_user, db)
    
    # Log usage check
    logger.info("monthly_limit_check",
                user_id=current_user.id,
                used=usage_info['used'],
                limit=usage_info['limit'],
                remaining=usage_info['remaining'],
                usage_percent=round((usage_info['used'] / usage_info['limit']) * 100, 2))
    
    # Save user message
    user_message = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    
    # Get user's documents for context
    recent_docs = db.query(Document).filter(
        Document.user_id == current_user.id
    ).order_by(Document.uploaded_at.desc()).limit(5).all()
    
    # Build context from documents
    context = "Dokumenty používateľa:\\n"
    for doc in recent_docs:
        if doc.extracted_data:
            context += f"- {doc.filename} ({doc.document_type}): {doc.extracted_data.get('total_amount', 'N/A')} EUR\\n"
    
    # Get AI response
    try:
        openai_start = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Ste odborný daňový konzultant pre Slovensko. Odpovedajte na otázky o slovenskom daňovom systéme presne a profesionálne.\\n\\n{context}"},
                {"role": "user", "content": chat_request.message}
            ]
        )
        ai_response = response.choices[0].message.content
        openai_duration = int((time.time() - openai_start) * 1000)
        
        # Log OpenAI API call
        logger.info("openai_api_call",
                    user_id=current_user.id,
                    model="gpt-4",
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    cost_usd=round((response.usage.prompt_tokens * 0.00003 + response.usage.completion_tokens * 0.00006), 4),
                    duration_ms=openai_duration)
    except Exception as e:
        logger.error("openai_api_error",
                     user_id=current_user.id,
                     error=str(e),
                     error_type=type(e).__name__)
        ai_response = "Prepáčte, momentálne nemôžem spracovať vašu otázku. Skúste to prosím neskôr."
    
    # Save AI response
    assistant_message = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=ai_response
    )
    db.add(assistant_message)
    db.commit()
    
    return ChatResponse(response=ai_response)



# Usage tracking endpoint
@app.get("/api/usage")
async def get_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current usage statistics for the authenticated user"""
    
    # Auto-reset on 1st of month
    if datetime.now().day == 1 and current_user.requests_used_this_month > 0:
        current_user.requests_used_this_month = 0
        db.commit()
    
    remaining = current_user.monthly_request_limit - current_user.requests_used_this_month
    usage_percent = (current_user.requests_used_this_month / current_user.monthly_request_limit) * 100
    
    # Calculate next reset date (1st of next month)
    now = datetime.now()
    if now.month == 12:
        next_month = 1
        next_year = now.year + 1
    else:
        next_month = now.month + 1
        next_year = now.year
    
    next_reset = datetime(next_year, next_month, 1)
    
    warning = None
    if usage_percent >= 80:
        warning = f"⚠️ Ви використали {current_user.requests_used_this_month}/{current_user.monthly_request_limit} запитів. Залишилось: {remaining}"
    
    return {
        "used": current_user.requests_used_this_month,
        "limit": current_user.monthly_request_limit,
        "remaining": remaining,
        "usage_percent": round(usage_percent, 1),
        "reset_date": next_reset.isoformat(),
        "warning": warning
    }


# ============================================
# EDUCATIONAL PLATFORM ENDPOINTS
# ============================================

@app.get("/api/universities")
def get_universities(
    jurisdiction_code: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all universities, optionally filtered by jurisdiction and type (with caching)"""
    
    # Generate cache key
    cache_key = f"universities:{jurisdiction_code or 'all'}:{type or 'all'}"
    
    # Try to get from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    # Query database
    query = db.query(University).filter(University.is_active == True)
    
    if jurisdiction_code:
        # Filter by jurisdiction code through join with jurisdictions table
        query = query.join(Jurisdiction, University.jurisdiction_id == Jurisdiction.id).filter(Jurisdiction.code == jurisdiction_code)
    
    if type:
        query = query.filter(University.type == type)
    
    universities = query.all()
    
    result = {
        "universities": [
            {
                "id": u.id,
                "name": u.name,
                "name_local": u.name_local,
                "type": u.type,
                "city": u.city,
                "country": u.country,
                "description": u.description,
                "website_url": u.website_url,
                "logo_url": u.logo_url,
                "student_count": u.student_count,
                "ranking_position": u.ranking_position,
                "programs_count": len(u.programs) if u.programs else 0
            }
            for u in universities
        ]
    }
    
    # Cache for 1 hour
    cache.set(cache_key, result, ttl=3600)
    
    return result


@app.get("/api/universities/{university_id}")
def get_university(
    university_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific university"""
    university = db.query(University).filter_by(id=university_id, is_active=True).first()
    
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    return {
        "id": university.id,
        "name": university.name,
        "name_local": university.name_local,
        "type": university.type,
        "city": university.city,
        "country": university.country,
        "description": university.description,
        "website_url": university.website_url,
        "logo_url": university.logo_url,
        "contact_email": university.contact_email,
        "contact_phone": university.contact_phone,
        "address": university.address,
        "student_count": university.student_count,
        "ranking_position": university.ranking_position,
        "programs": [
            {
                "id": p.id,
                "name": p.name,
                "name_local": p.name_local,
                "degree_level": p.degree_level,
                "field_of_study": p.field_of_study,
                "language": p.language,
                "duration_years": p.duration_years,
                "tuition_fee": p.tuition_fee,
                "description": p.description,
                "admission_requirements": p.admission_requirements,
                "application_deadline": p.application_deadline.isoformat() if p.application_deadline else None,
                "capacity": p.capacity
            }
            for p in university.programs if p.is_active
        ]
    }



# University chat endpoints moved to api/university_chat.py router
# See below for router inclusion




@app.get("/api/programs")
def get_programs(
    university_id: Optional[int] = None,
    degree_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get programs, optionally filtered by university or degree level"""
    query = db.query(Program).filter(Program.is_active == True)
    
    if university_id:
        query = query.filter(Program.university_id == university_id)
    
    if degree_level:
        query = query.filter(Program.degree_level == degree_level)
    
    programs = query.all()
    
    return {
        "programs": [
            {
                "id": p.id,
                "university_id": p.university_id,
                "university_name": p.university.name if p.university else None,
                "name": p.name,
                "name_local": p.name_local,
                "degree_level": p.degree_level,
                "field_of_study": p.field_of_study,
                "language": p.language,
                "duration_years": p.duration_years,
                "tuition_fee": p.tuition_fee,
                "description": p.description
            }
            for p in programs
        ]
    }


# Import and include Case Management routers
try:
    from api.case_assignments import router as assignments_router
    app.include_router(assignments_router)
except ImportError as e:
    print(f'Warning: Could not import case_assignments router: {e}')

try:
    from api.case_comments import router as comments_router
    app.include_router(comments_router)
except ImportError as e:
    print(f'Warning: Could not import case_comments router: {e}')

try:
    from api.case_deadlines import router as deadlines_router
    app.include_router(deadlines_router)
except ImportError as e:
    print(f'Warning: Could not import case_deadlines router: {e}')

try:
    from api.notifications import router as notifications_router
    app.include_router(notifications_router)
except ImportError as e:
    print(f'Warning: Could not import notifications router: {e}')

# Import and include Cases v2 router
try:
    from api.cases_v2 import router as cases_v2_router
    app.include_router(cases_v2_router)
except ImportError as e:
    print(f'Warning: Could not import cases_v2 router: {e}')

# Import AI Cases router
try:
    from api.ai_cases import router as ai_cases_router
    app.include_router(ai_cases_router)
    print("✅ AI Cases router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import ai_cases router: {e}')
    traceback.print_exc()

# Import Payments router
try:
    from api.payments import router as payments_router
    # Override the dependencies with actual implementations
    from api.payments import router as payments_router_module
    payments_router_module.get_db = get_db
    payments_router_module.get_current_user = get_current_user
    app.include_router(payments_router)
    print("✅ Payments router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import payments router: {e}')
    traceback.print_exc()

# Import Subscription Status router
try:
    from api.subscription_status import router as subscription_status_router
    from api import subscription_status as subscription_status_module
    subscription_status_module.get_db = get_db
    subscription_status_module.get_current_user = get_current_user
    app.include_router(subscription_status_router)
    print("✅ Subscription Status router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import subscription_status router: {e}')
    traceback.print_exc()

# Import AI Support router
try:
    from routers.ai_support import router as ai_support_router
    from routers import ai_support as ai_support_module
    ai_support_module.get_db = get_db
    ai_support_module.get_current_user = get_current_user
    app.include_router(ai_support_router)
    print("✅ AI Support router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import ai_support router: {e}')
    traceback.print_exc()

# Import Price Monitoring router
try:
    from routers.price_monitoring import router as price_monitoring_router
    from routers import price_monitoring as price_monitoring_module
    price_monitoring_module.get_db = get_db
    price_monitoring_module.get_current_user = get_current_user
    app.include_router(price_monitoring_router)
    print("✅ Price Monitoring router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import price_monitoring router: {e}')
    traceback.print_exc()

# Import Health Check router
try:
    from routers.health import router as health_router
    app.include_router(health_router, tags=["health"])
    print("✅ Health Check router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import health router: {e}')
    traceback.print_exc()

# Import Platform Owner Analytics router
try:
    from api.platform_owner_analytics import router as analytics_router
    app.include_router(analytics_router)
    print("✅ Platform Owner Analytics router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import analytics router: {e}')
    traceback.print_exc()

# Import Marketplace Lawyers router
try:
    from api.marketplace.lawyers import router as marketplace_lawyers_router
    app.include_router(marketplace_lawyers_router)
    print("✅ Marketplace Lawyers router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import marketplace lawyers router: {e}')
    traceback.print_exc()

# Import Client router (Krok 3)
try:
    from api.client import router as client_router
    app.include_router(client_router)
    print("✅ Client router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import client router: {e}')
    traceback.print_exc()

# Import Messages router (Krok 4)
try:
    from api.messages import router as messages_router
    app.include_router(messages_router)
    print("✅ Messages router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import messages router: {e}')
    traceback.print_exc()

# Import Marketplace Payments router (Krok 5)
try:
    from api.marketplace_payments import router as marketplace_payments_router
    app.include_router(marketplace_payments_router)
    print("✅ Marketplace Payments router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import marketplace payments router: {e}')
    traceback.print_exc()


# ============================================================================
# RAG ADMIN ENDPOINTS
# ============================================================================

@app.post("/api/admin/scrape-university/{university_id}")
async def trigger_university_scraping(
    university_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Trigger scraping for specific university (Admin only)
    """
    from tasks.university_scraping import scrape_university_task
    
    # Check if university exists
    university = db.query(University).filter_by(id=university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Queue scraping task
    task = scrape_university_task.delay(university_id)
    
    return {
        "message": f"Scraping queued for {university.name}",
        "task_id": task.id,
        "university_id": university_id
    }


@app.post("/api/admin/scrape-all-universities")
async def trigger_all_universities_scraping(
    current_user: dict = Depends(get_current_user)
):
    """
    Trigger scraping for all universities (Admin only)
    """
    from tasks.university_scraping import scrape_all_universities_task
    
    task = scrape_all_universities_task.delay()
    
    return {
        "message": "Scraping queued for all universities",
        "task_id": task.id
    }


@app.get("/api/admin/rag-status")
async def get_rag_status(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get RAG readiness status for all universities
    """
    result = db.execute(text("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN rag_ready THEN 1 END) as ready,
            COUNT(CASE WHEN scraping_status = 'pending' THEN 1 END) as pending,
            COUNT(CASE WHEN scraping_status = 'in_progress' THEN 1 END) as in_progress,
            COUNT(CASE WHEN scraping_status = 'failed' THEN 1 END) as failed
        FROM university_rag_status
    """))
    
    row = result.first()
    
    return {
        "total_universities": row[0],
        "rag_ready": row[1],
        "pending": row[2],
        "in_progress": row[3],
        "failed": row[4]
    }


@app.get("/api/admin/rag-status/{university_id}")
async def get_university_rag_status(
    university_id: int,
    db: Session = Depends(get_db)
):
    """
    Get RAG status for specific university
    """
    status = db.query(UniversityScrapingStatus).filter_by(
        university_id=university_id
    ).first()
    
    if not status:
        return {
            "university_id": university_id,
            "status": "not_started",
            "rag_ready": False
        }
    
    return {
        "university_id": university_id,
        "status": status.scraping_status,
        "pages_scraped": status.pages_scraped,
        "embeddings_generated": status.embeddings_generated,
        "last_scraped_at": status.last_scraped_at,
        "error_message": status.error_message,
        "rag_ready": status.embeddings_generated > 0
    }


# Import Housing Search router

try:
    from api.housing import router as housing_router
    from api import housing as housing_module
    housing_module.get_db = get_db
    housing_module.get_current_user = get_current_user
    app.include_router(housing_router)
    print("✅ Housing Search router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import housing router: {e}')
    traceback.print_exc()

# Import University Chat router
try:
    from api.university_chat import router as university_chat_router
    app.include_router(university_chat_router)
    print("✅ University Chat router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import university_chat router: {e}')
    traceback.print_exc()

# Import Metrics router
try:
    from api.metrics import router as metrics_router
    app.include_router(metrics_router)
    print("✅ Metrics router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import metrics router: {e}')
    traceback.print_exc()

# Import Jobs router
try:
    from api.jobs import router as jobs_router
    from api import jobs as jobs_module
    jobs_module.get_db = get_db
    jobs_module.get_current_user = get_current_user
    app.include_router(jobs_router)
    print("✅ Jobs router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import jobs router: {e}')
    traceback.print_exc()

# Import Admin API router
try:
    from routers.admin_api import router as admin_router
    from routers import admin_api as admin_module
    admin_module.get_db = get_db
    admin_module.get_current_user = get_current_user
    app.include_router(admin_router)
    print("✅ Admin API router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import admin router: {e}')
    traceback.print_exc()

# Import Admin Stats router
try:
    from routers import admin
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
    print("✅ Admin stats router loaded successfully!")
except ImportError as e:
    import traceback
    print(f'❌ Warning: Could not import admin stats router: {e}')
    traceback.print_exc()
