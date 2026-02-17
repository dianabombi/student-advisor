"""
MARKETPLACE PAYMENT MODELS
Pydantic schemas for marketplace payment system
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ============================================
# ENUMS
# ============================================

class TransactionType(str, Enum):
    PAYMENT = "payment"
    PAYOUT = "payout"
    REFUND = "refund"
    PLATFORM_FEE = "platform_fee"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DisputeReason(str, Enum):
    QUALITY_ISSUE = "quality_issue"
    INCOMPLETE_WORK = "incomplete_work"
    WRONG_SERVICE = "wrong_service"
    LAWYER_UNRESPONSIVE = "lawyer_unresponsive"
    OTHER = "other"

# ============================================
# REQUEST MODELS
# ============================================

class CreatePaymentRequest(BaseModel):
    """Schema for initiating marketplace payment"""
    order_id: int = Field(..., description="ID objednávky")
    return_url: Optional[str] = Field(None, description="URL kam presmerovať")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 123,
                "return_url": "https://codex.app/orders/123"
            }
        }

class WithdrawRequest(BaseModel):
    """Schema for lawyer withdrawal"""
    amount: float = Field(..., gt=0, description="Suma na výber")
    bank_account: str = Field(..., description="Číslo účtu")
    note: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "amount": 150.00,
                "bank_account": "SK31 1200 0000 1987 4263 7541",
                "note": "Výber zárobkov"
            }
        }

class CreateDisputeRequest(BaseModel):
    """Schema for creating dispute"""
    order_id: int
    reason: DisputeReason
    description: str = Field(..., min_length=50, max_length=2000)
    requested_refund_amount: Optional[float] = None

class ResolveDisputeRequest(BaseModel):
    """Schema for resolving dispute (admin)"""
    dispute_id: int
    resolution: str = Field(..., min_length=20, max_length=2000)
    refund_amount: float = Field(0, ge=0)
    refund_to_client: bool = False

# ============================================
# RESPONSE MODELS
# ============================================

class PaymentIntentResponse(BaseModel):
    """Payment intent details"""
    payment_intent_id: str
    client_secret: Optional[str] = None
    amount: float
    currency: str
    status: str
    checkout_url: Optional[str] = None

class TransactionResponse(BaseModel):
    """Transaction details"""
    id: int
    transaction_number: str
    order_id: Optional[int] = None
    type: str
    amount: float
    currency: str
    status: str
    description: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WalletResponse(BaseModel):
    """Lawyer wallet"""
    lawyer_id: int
    total_earnings: float
    available_balance: float
    pending_balance: float
    total_withdrawn: float
    currency: str

class WithdrawalResponse(BaseModel):
    """Withdrawal details"""
    id: int
    withdrawal_number: str
    amount: float
    bank_account: str
    status: str
    requested_at: datetime
    completed_at: Optional[datetime] = None

class DisputeResponse(BaseModel):
    """Dispute details"""
    id: int
    order_id: int
    raised_by: str
    reason: str
    description: str
    status: str
    resolution: Optional[str] = None
    refund_amount: Optional[float] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ApiResponse(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[dict] = None
