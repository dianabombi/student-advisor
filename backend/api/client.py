"""
CLIENT ROUTES
API endpoints for client functionality

Base path: /api/client
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models.client import (
    CreateCaseRequest,
    CreateOrderRequest,
    ReviewRequest,
    AIAnalysisResponse,
    LawyerMatchResponse,
    Top3LawyersResponse,
    CaseResponse,
    OrderResponse,
    ApiResponse
)
from main import get_current_user, get_db, logger

router = APIRouter(prefix="/api/client", tags=["Client"])

# ============================================
# CASE MANAGEMENT
# ============================================

@router.post("/cases", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CreateCaseRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new legal case
    
    **Vytvoriť nový právny prípad**
    
    This is the first step in the client journey.
    """
    try:
        from services import client_service
        
        case = await client_service.create_case(
            db=db,
            client_id=current_user.id,
            case_data=case_data.dict()
        )
        
        logger.info("case_created", case_id=case.id, client_id=current_user.id)
        return case
        
    except Exception as e:
        logger.error("case_creation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri vytváraní prípadu / Error creating case: {str(e)}"
        )


@router.post("/cases/{case_id}/upload-attachments")
async def upload_case_attachments(
    case_id: int,
    files: List[UploadFile] = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload attachments to a case
    
    **Nahrať prílohy k prípadu**
    """
    try:
        from services import client_service
        
        # Verify ownership
        case = await client_service.get_case(db, case_id)
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Upload files (stub for now)
        attachments = []
        for file in files:
            attachments.append({
                "filename": file.filename,
                "size": file.size,
                "type": file.content_type,
                "uploaded_at": datetime.now().isoformat()
            })
        
        await client_service.add_attachments(db, case_id, attachments)
        
        return {
            "success": True,
            "message": "Súbory úspešne nahrané / Files uploaded successfully",
            "data": {"attachments": attachments}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri nahrávaní / Upload error: {str(e)}"
        )


@router.post("/cases/{case_id}/analyze", response_model=AIAnalysisResponse)
async def analyze_case(
    case_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI analysis of the case
    
    **Získať AI analýzu prípadu**
    
    STEP 2 in client journey. AI analyzes the case and provides recommendations.
    """
    try:
        from services import client_service, ai_service
        
        # Verify ownership
        case = await client_service.get_case(db, case_id)
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Update status
        await client_service.update_case_status(db, case_id, "ai_analysis")
        
        # Run AI analysis
        analysis = await ai_service.analyze_case(case)
        
        # Save analysis
        await client_service.save_ai_analysis(db, case_id, analysis)
        await client_service.update_case_status(db, case_id, "ai_completed")
        
        logger.info("case_analyzed", case_id=case_id)
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("analysis_error", case_id=case_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri analýze / Analysis error: {str(e)}"
        )


@router.get("/cases", response_model=List[CaseResponse])
async def get_my_cases(
    status_filter: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get client's cases
    
    **Získať prípady klienta**
    """
    try:
        from services import client_service
        
        cases = await client_service.get_my_cases(
            db=db,
            client_id=current_user.id,
            status_filter=status_filter,
            limit=limit,
            offset=offset
        )
        return cases
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get case details
    
    **Získať detaily prípadu**
    """
    try:
        from services import client_service
        
        case = await client_service.get_case(db, case_id)
        
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# LAWYER SELECTION (3 SCENARIOS)
# ============================================

@router.post("/cases/{case_id}/match-lawyer", response_model=LawyerMatchResponse)
async def auto_match_lawyer(
    case_id: int,
    service_type: str = Query(..., regex="^(document_review|consultation|full_service)$"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    SCENARIO 1: Auto-match best lawyer
    
    **SCENÁR 1: Automaticky priradiť najlepšieho advokáta**
    
    This is the default and recommended approach (80% of users).
    """
    try:
        from services import client_service, matching_service
        
        # Verify ownership
        case = await client_service.get_case(db, case_id)
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Find best matching lawyer
        best_lawyer = await matching_service.find_best_match(
            db=db,
            case=case,
            service_type=service_type
        )
        
        if not best_lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Žiadny dostupný advokát / No available lawyer found"
            )
        
        logger.info("lawyer_matched", case_id=case_id, lawyer_id=best_lawyer.lawyer_id)
        return best_lawyer
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("matching_error", case_id=case_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/cases/{case_id}/top-lawyers", response_model=Top3LawyersResponse)
async def get_top_3_lawyers(
    case_id: int,
    service_type: str = Query(..., regex="^(document_review|consultation|full_service)$"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    SCENARIO 2: Show top 3 lawyers for selection
    
    **SCENÁR 2: Zobraziť top 3 advokátov na výber**
    
    This is shown when client clicks "Show other lawyers" (15% of users).
    """
    try:
        from services import client_service, matching_service
        
        # Verify ownership
        case = await client_service.get_case(db, case_id)
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Find top 3 lawyers
        top_3 = await matching_service.find_top_3(
            db=db,
            case=case,
            service_type=service_type
        )
        
        return top_3
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/cases/{case_id}/all-lawyers")
async def get_all_available_lawyers(
    case_id: int,
    service_type: str = Query(..., regex="^(document_review|consultation|full_service)$"),
    sort: str = Query("recommended", regex="^(recommended|rating|price|speed)$"),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    SCENARIO 3: Show full list of lawyers
    
    **SCENÁR 3: Zobraziť úplný zoznam advokátov**
    
    This is shown when client clicks "Show all lawyers" (5% of users).
    """
    try:
        from services import client_service, matching_service
        
        # Verify ownership
        case = await client_service.get_case(db, case_id)
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Get all available lawyers
        lawyers = await matching_service.find_all_available(
            db=db,
            case=case,
            service_type=service_type,
            sort=sort,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "data": lawyers
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# ORDER MANAGEMENT
# ============================================

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: CreateOrderRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create an order for legal service
    
    **Vytvoriť objednávku právnej služby**
    """
    try:
        from services import client_service, matching_service
        
        # Verify ownership
        case = await client_service.get_case(db, order_data.case_id)
        if case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Assign lawyer if auto_match
        lawyer_id = order_data.preferred_lawyer_id
        if order_data.auto_match and not lawyer_id:
            best_match = await matching_service.find_best_match(
                db=db,
                case=case,
                service_type=order_data.service_type
            )
            lawyer_id = best_match.lawyer_id if best_match else None
        
        # Create order
        order = await client_service.create_order(
            db=db,
            case_id=order_data.case_id,
            client_id=current_user.id,
            lawyer_id=lawyer_id,
            service_type=order_data.service_type
        )
        
        logger.info("order_created", order_id=order.id, case_id=order_data.case_id)
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("order_creation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri vytváraní objednávky / Error creating order: {str(e)}"
        )


@router.get("/orders", response_model=List[OrderResponse])
async def get_my_orders(
    status_filter: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get client's orders
    
    **Získať objednávky klienta**
    """
    try:
        from services import client_service
        
        orders = await client_service.get_my_orders(
            db=db,
            client_id=current_user.id,
            status_filter=status_filter,
            limit=limit,
            offset=offset
        )
        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get order details
    
    **Získať detaily objednávky**
    """
    try:
        from services import client_service
        
        order = await client_service.get_order(db, order_id)
        
        if order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/orders/{order_id}/complete")
async def complete_order(
    order_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Confirm order completion
    
    **Potvrdiť dokončenie objednávky**
    """
    try:
        from services import client_service
        
        order = await client_service.get_order(db, order_id)
        
        if order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        if order.status != 'delivered':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Objednávka ešte nie je dodaná / Order not yet delivered"
            )
        
        await client_service.complete_order(db, order_id)
        
        logger.info("order_completed", order_id=order_id)
        return {
            "success": True,
            "message": "Objednávka dokončená / Order completed",
            "data": {"order_id": order_id}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# REVIEWS
# ============================================

@router.post("/reviews", status_code=status.HTTP_201_CREATED)
async def submit_review(
    review_data: ReviewRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a review for completed order
    
    **Odoslať recenziu za dokončenú objednávku**
    """
    try:
        from services import client_service
        
        # Verify ownership and status
        order = await client_service.get_order(db, review_data.order_id)
        
        if order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        if order.status != 'completed':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Môžete recenzovať len dokončené objednávky / Can only review completed orders"
            )
        
        # Create review
        review = await client_service.create_review(
            db=db,
            order_id=review_data.order_id,
            client_id=current_user.id,
            lawyer_id=order.lawyer_id,
            review_data=review_data.dict()
        )
        
        logger.info("review_submitted", order_id=review_data.order_id, rating=review_data.rating)
        return {
            "success": True,
            "message": "Recenzia odoslaná / Review submitted",
            "data": review
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("review_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )
