"""
CLIENT PYDANTIC MODELS
Data validation schemas for client endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ============================================
# ENUMS
# ============================================

class CaseCategory(str, Enum):
    CIVIL_LAW = "civil_law"
    LABOR_LAW = "labor_law"
    CONSUMER_PROTECTION = "consumer_protection"
    TRANSPORT_LAW = "transport_law"
    FAMILY_LAW = "family_law"
    REAL_ESTATE = "real_estate"
    CRIMINAL_LAW = "criminal_law"
    ADMINISTRATIVE_LAW = "administrative_law"

class CaseUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CaseStatus(str, Enum):
    DRAFT = "draft"
    AI_ANALYSIS = "ai_analysis"
    AI_COMPLETED = "ai_completed"
    PAYMENT_PENDING = "payment_pending"
    SEEKING_LAWYER = "seeking_lawyer"
    LAWYER_ASSIGNED = "lawyer_assigned"
    IN_PROGRESS = "in_progress"
    PENDING_CLIENT = "pending_client"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# ============================================
# REQUEST MODELS
# ============================================

class CreateCaseRequest(BaseModel):
    """Schema for creating a new legal case"""
    title: str = Field(..., min_length=10, max_length=255, description="Názov prípadu")
    description: str = Field(..., min_length=50, max_length=5000, description="Detailný popis situácie")
    category: CaseCategory = Field(..., description="Kategória prípadu")
    case_type: str = Field(..., max_length=50, description="Typ prípadu")
    urgency: CaseUrgency = Field(CaseUrgency.MEDIUM, description="Naliehavosť")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Nezákonná pokuta v MHD",
                "description": "Dostal som pokutu 50€ za cestovanie bez lístka, ale lístok som mal. Kontrolór ho neuznал a vystavil pokutu. Mám fotku lístka a chcem sa odvolať.",
                "category": "transport_law",
                "case_type": "transport_fine",
                "urgency": "medium"
            }
        }

class CreateOrderRequest(BaseModel):
    """Schema for creating an order for legal service"""
    case_id: int = Field(..., description="ID prípadu")
    service_type: str = Field(..., description="Typ služby (document_review, consultation, full_service)")
    preferred_lawyer_id: Optional[int] = Field(None, description="ID preferovaného advokáta")
    auto_match: bool = Field(True, description="Automaticky priradiť najlepšieho advokáta")
    
    class Config:
        json_schema_extra = {
            "example": {
                "case_id": 123,
                "service_type": "document_review",
                "auto_match": True
            }
        }

class ReviewRequest(BaseModel):
    """Schema for submitting a review"""
    order_id: int
    rating: int = Field(..., ge=1, le=5, description="Hodnotenie 1-5")
    communication_rating: Optional[int] = Field(None, ge=1, le=5)
    professionalism_rating: Optional[int] = Field(None, ge=1, le=5)
    result_satisfaction: Optional[int] = Field(None, ge=1, le=5)
    speed_rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=2000, description="Komentár")
    is_public: bool = Field(True, description="Verejná recenzia?")

# ============================================
# RESPONSE MODELS
# ============================================

class AIAnalysisResponse(BaseModel):
    """AI analysis result for a case"""
    complexity_score: int = Field(..., ge=1, le=10, description="Zložitosť 1-10")
    success_probability: float = Field(..., ge=0, le=100, description="Pravdepodobnosť úspechu %")
    recommended_action: str
    estimated_time: str
    estimated_cost_range: dict
    key_points: List[str]
    required_documents: List[str]
    options: List[dict]

class LawyerMatchResponse(BaseModel):
    """Matched lawyer for auto-match scenario"""
    lawyer_id: int
    full_name: str
    title: str
    rating: float
    total_reviews: int
    success_rate: float
    average_response_time: int
    specializations: List[str]
    languages: List[str]
    years_of_experience: int
    bio: Optional[str] = None
    match_percentage: int = Field(..., ge=0, le=100, description="Ako dobre sedí")
    price: float
    estimated_delivery: str

class Top3LawyersResponse(BaseModel):
    """Top 3 lawyers for client selection"""
    lawyers: List[LawyerMatchResponse]
    total_available: int
    recommendation: dict

class CaseResponse(BaseModel):
    """Legal case details"""
    id: int
    case_number: str
    title: str
    description: str
    category: str
    case_type: str
    status: str
    urgency: str
    ai_summary: Optional[str] = None
    ai_complexity_score: Optional[int] = None
    ai_success_probability: Optional[float] = None
    ai_recommended_action: Optional[str] = None
    ai_generated_document_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    """Order details"""
    id: int
    order_number: str
    case_id: int
    service_type: str
    status: str
    service_price: float
    lawyer_id: Optional[int] = None
    lawyer_name: Optional[str] = None
    lawyer_rating: Optional[float] = None
    created_at: datetime
    deadline: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ApiResponse(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[dict] = None
