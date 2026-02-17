"""
MARKETPLACE PYDANTIC MODELS
Data validation schemas for marketplace endpoints (lawyers, orders, reviews)
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============================================
# ENUMS
# ============================================

class ServiceType(str, Enum):
    DOCUMENT_REVIEW = "document_review"
    CONSULTATION = "consultation"
    FULL_SERVICE = "full_service"


class Specialization(str, Enum):
    CIVIL_LAW = "civil_law"
    LABOR_LAW = "labor_law"
    CONSUMER_PROTECTION = "consumer_protection"
    TRANSPORT_LAW = "transport_law"
    FAMILY_LAW = "family_law"
    REAL_ESTATE = "real_estate"
    CRIMINAL_LAW = "criminal_law"
    ADMINISTRATIVE_LAW = "administrative_law"
    COMMERCIAL_LAW = "commercial_law"
    TAX_LAW = "tax_law"


class Language(str, Enum):
    SK = "sk"
    EN = "en"
    CZ = "cs"
    PL = "pl"
    HU = "hu"
    DE = "de"
    FR = "fr"
    ES = "es"
    IT = "it"
    RU = "ru"
    UK = "uk"


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


# ============================================
# LAWYER REQUEST MODELS
# ============================================

class LawyerRegistrationRequest(BaseModel):
    """Schema for lawyer registration"""
    user_id: int = Field(..., description="ID používateľa z tabuľky users")
    full_name: str = Field(..., min_length=3, max_length=255, description="Celé meno advokáta")
    title: str = Field(..., max_length=100, description="Titul (JUDr., Mgr., atď.)")
    license_number: str = Field(..., min_length=5, max_length=100, description="Číslo advokátskej licencie")
    bar_association: Optional[str] = Field(None, max_length=255, description="Advokátska komora")
    
    # Jurisdictions - lawyer can have licenses in multiple countries
    jurisdictions: List[str] = Field(..., min_items=1, description="Jurisdikcie kde má advokát licenciu (napr. ['SK', 'CZ'])")
    
    specializations: List[str] = Field(..., min_items=1, description="Špecializácie")
    languages: List[str] = Field(default=["sk"], description="Jazyky")
    experience_years: int = Field(0, ge=0, le=70, description="Roky praxe")
    bio: Optional[str] = Field(None, max_length=2000, description="Krátky opis o advokátovi")
    education: Optional[str] = Field(None, max_length=1000, description="Vzdelanie")
    hourly_rate: Optional[float] = Field(100.00, ge=10, le=1000, description="Hodinová sadzba v EUR")
    consultation_fee: Optional[float] = Field(49.00, ge=10, le=500, description="Cena za konzultáciu")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "full_name": "JUDr. Mária Kováčová",
                "title": "JUDr.",
                "license_number": "SK-ADV-12345",
                "bar_association": "Slovak Bar Association",
                "jurisdictions": ["SK", "CZ"],
                "specializations": ["civil_law", "consumer_protection"],
                "languages": ["sk", "en"],
                "experience_years": 8,
                "bio": "Špecializujem sa na občianske právo a ochranu spotrebiteľa.",
                "education": "Univerzita Komenského, Právnická fakulta"
            }
        }


class LawyerUpdateRequest(BaseModel):
    """Schema for updating lawyer profile"""
    bio: Optional[str] = Field(None, max_length=2000)
    hourly_rate: Optional[float] = Field(None, ge=10, le=1000)
    consultation_fee: Optional[float] = Field(None, ge=10, le=500)
    is_active: Optional[bool] = None
    languages: Optional[List[str]] = None
    specializations: Optional[List[str]] = None


class AvailabilityRequest(BaseModel):
    """Schema for setting availability"""
    is_active: bool = Field(..., description="Či je advokát dostupný")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_active": True
            }
        }


# ============================================
# LAWYER RESPONSE MODELS
# ============================================

class LawyerPublicProfile(BaseModel):
    """Public lawyer profile (for clients)"""
    id: int
    full_name: str
    title: str
    jurisdictions: List[str]  # Jurisdictions where lawyer is licensed
    specializations: List[str]
    languages: List[str]
    experience_years: int
    bio: Optional[str]
    average_rating: Optional[float]
    total_reviews: int
    hourly_rate: Optional[float]
    consultation_fee: Optional[float]
    is_active: bool
    
    class Config:
        from_attributes = True


class LawyerPrivateProfile(BaseModel):
    """Private lawyer profile (for lawyer themselves)"""
    id: int
    user_id: int
    full_name: str
    title: str
    license_number: str
    bar_association: Optional[str]
    jurisdictions: List[str]  # Jurisdictions where lawyer is licensed
    specializations: List[str]
    languages: List[str]
    experience_years: int
    bio: Optional[str]
    education: Optional[str]
    is_verified: bool
    is_active: bool
    average_rating: Optional[float]
    total_reviews: int
    total_cases: int
    hourly_rate: Optional[float]
    consultation_fee: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Lawyer dashboard statistics"""
    average_rating: Optional[float]
    total_reviews: int
    total_cases: int
    active_orders: int = 0
    completed_orders: int = 0


# ============================================
# ORDER MODELS
# ============================================

class OrderCreate(BaseModel):
    """Create new order"""
    lawyer_id: int
    case_id: Optional[int] = None
    service_type: str
    description: str
    amount: float = Field(..., ge=0)
    currency: str = Field(default="EUR")


class OrderResponse(BaseModel):
    """Order response"""
    id: int
    order_number: str
    user_id: int
    lawyer_id: int
    service_type: str
    amount: float
    currency: str
    status: str
    payment_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# REVIEW MODELS
# ============================================

class ReviewCreate(BaseModel):
    """Create review"""
    lawyer_id: int
    order_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    comment: Optional[str] = None
    professionalism_rating: Optional[int] = Field(None, ge=1, le=5)
    communication_rating: Optional[int] = Field(None, ge=1, le=5)
    expertise_rating: Optional[int] = Field(None, ge=1, le=5)
    value_rating: Optional[int] = Field(None, ge=1, le=5)


class ReviewResponse(BaseModel):
    """Review response"""
    id: int
    user_id: int
    lawyer_id: int
    rating: int
    title: Optional[str]
    comment: Optional[str]
    is_verified: bool
    is_visible: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# STANDARD API RESPONSE
# ============================================

class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None
