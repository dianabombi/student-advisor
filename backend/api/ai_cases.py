"""
AI-Enhanced Cases API

Integrates AI Case Analyzer with case management.
Automatically analyzes cases and provides AI-driven recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from auth.rbac import get_current_user
from api.cases_v2 import Case, CaseLog, get_db
from services.ai_case_analyzer import AICaseAnalyzer

router = APIRouter(prefix="/api/ai/cases", tags=["AI Cases"])


class AIAnalysisRequest(BaseModel):
    """Request for AI case analysis."""
    case_id: str


class AIChatRequest(BaseModel):
    """Request for AI chat with case context."""
    message: str
    case_id: Optional[str] = None


class DocumentGenerationRequest(BaseModel):
    """Request for document generation."""
    case_id: str
    document_type: str = "lawsuit"  # lawsuit, demand_letter, contract


@router.post("/analyze/{case_id}")
async def analyze_case_with_ai(
    case_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze case using AI and get recommendations with legal citations.
    
    Returns:
    - Legal analysis with citations
    - Confidence score
    - Whether lawyer is needed
    - Recommended documents
    - Suggested next status
    """
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if current_user.role not in ['admin', 'partner_lawyer', 'lawyer']:
        if case.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    # Prepare case data for AI
    case_data = {
        "title": case.title,
        "description": case.description,
        "claim_amount": float(case.claim_amount) if case.claim_amount else None,
        "client_name": case.client_name,
        "client_email": case.client_email,
        "client_phone": case.client_phone
    }
    
    # Create analyzer with DB session for RAG
    analyzer = AICaseAnalyzer(db)
    analysis = await analyzer.analyze_case(case_data)
    
    # Log AI analysis
    log_entry = CaseLog(
        case_id=case_id,
        event_type='ai_analysis',
        new_value=f"Confidence: {analysis['confidence']}",
        created_by=current_user.id,
        comment=f"AI analyzed case. Citations: {len(analysis['citations'])}"
    )
    db.add(log_entry)
    db.commit()
    
    return {
        "success": True,
        "case_id": case_id,
        "analysis": analysis
    }


@router.post("/generate-document/{case_id}")
async def generate_legal_document(
    case_id: str,
    request: DocumentGenerationRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate legal document for case with AI.
    
    Document includes:
    - Proper legal formatting
    - Citations to relevant laws
    - Case-specific content
    """
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if current_user.role not in ['admin', 'partner_lawyer', 'lawyer']:
        if case.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    # Prepare case data
    case_data = {
        "title": case.title,
        "description": case.description,
        "claim_amount": float(case.claim_amount) if case.claim_amount else None,
        "client_name": case.client_name,
        "client_email": case.client_email,
        "deadline": case.deadline
    }
    
    # Generate document
    document = ai_analyzer.generate_legal_document(case_data, request.document_type)
    
    # Log document generation
    log_entry = CaseLog(
        case_id=case_id,
        event_type='document_generated',
        new_value=request.document_type,
        created_by=current_user.id,
        comment=f"AI generated {request.document_type} with {len(document['citations'])} citations"
    )
    db.add(log_entry)
    db.commit()
    
    return {
        "success": True,
        "document": document
    }


@router.post("/chat")
async def chat_with_ai(
    request: AIChatRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI legal assistant.
    
    ALWAYS includes legal citations in responses.
    Can use case context for better answers.
    """
    case_context = None
    
    # Get case context if provided
    if request.case_id:
        case = db.query(Case).filter(Case.id == request.case_id).first()
        
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Check permissions
        if current_user.role not in ['admin', 'partner_lawyer', 'lawyer']:
            if case.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
        
        case_context = {
            "title": case.title,
            "description": case.description,
            "status": case.status
        }
    
    # Get AI response with citations
    response = ai_analyzer.chat_with_citations(request.message, case_context)
    
    # Log chat interaction if case context provided
    if request.case_id:
        log_entry = CaseLog(
            case_id=request.case_id,
            event_type='ai_chat',
            created_by=current_user.id,
            comment=f"User asked: {request.message[:100]}..."
        )
        db.add(log_entry)
        db.commit()
    
    return response


@router.post("/auto-process/{case_id}")
async def auto_process_case(
    case_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Automatically process case with AI (99% automation).
    
    Steps:
    1. Analyze case
    2. Generate documents
    3. Update status if confidence high
    4. Assign lawyer only if needed (1%)
    """
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Step 1: Analyze
    case_data = {
        "title": case.title,
        "description": case.description,
        "claim_amount": float(case.claim_amount) if case.claim_amount else None,
        "client_name": case.client_name
    }
    
    analysis = ai_analyzer.analyze_case(case_data)
    
    # Step 2: Generate lawsuit document
    document = ai_analyzer.generate_legal_document(case_data, "lawsuit")
    
    # Step 3: Update status based on confidence
    if analysis['confidence'] > 0.8 and not analysis['needs_lawyer']:
        # High confidence - auto-submit
        case.status = 'submitted'
        status_log = CaseLog(
            case_id=case_id,
            event_type='status_change',
            old_value='draft',
            new_value='submitted',
            created_by=current_user.id,
            comment=f"AI auto-submitted (confidence: {analysis['confidence']})"
        )
        db.add(status_log)
    else:
        # Low confidence - needs review
        case.status = 'needs_review'
        review_log = CaseLog(
            case_id=case_id,
            event_type='status_change',
            old_value='draft',
            new_value='needs_review',
            created_by=current_user.id,
            comment=f"AI flagged for review (confidence: {analysis['confidence']})"
        )
        db.add(review_log)
    
    db.commit()
    
    return {
        "success": True,
        "case_id": case_id,
        "analysis": analysis,
        "document": document,
        "new_status": case.status,
        "needs_lawyer": analysis['needs_lawyer']
    }
