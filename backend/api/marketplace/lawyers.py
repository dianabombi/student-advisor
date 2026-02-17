"""
LAWYER ROUTES
API endpoints for lawyer functionality

Base path: /api/marketplace/lawyers
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from typing import List, Optional
from sqlalchemy.orm import Session
import json

from models.marketplace import (
    LawyerRegistrationRequest,
    LawyerUpdateRequest,
    AvailabilityRequest,
    LawyerPublicProfile,
    LawyerPrivateProfile,
    DashboardStats,
    ApiResponse
)
from main import get_db, get_current_user
from config.jurisdictions import (
    validate_jurisdictions,
    get_active_jurisdiction_codes,
    ACTIVE_JURISDICTION_CODES
)

router = APIRouter(prefix="/api/marketplace/lawyers", tags=["Marketplace - Lawyers"])


# ============================================
# PUBLIC ROUTES
# ============================================

@router.post("/register", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def register_lawyer(
    # Form data
    user_id: int = Form(...),
    full_name: str = Form(...),
    title: str = Form(...),
    license_number: str = Form(...),
    bar_association: Optional[str] = Form(None),
    specializations: str = Form(..., description="JSON array: [\"civil_law\", \"labor_law\"]"),
    jurisdictions: str = Form(..., description="JSON array of jurisdictions: [\"SK\", \"CZ\"]"),
    languages: str = Form(default='["sk"]', description="JSON array: [\"sk\", \"en\"]"),
    experience_years: int = Form(0),
    bio: Optional[str] = Form(None),
    education: Optional[str] = Form(None),
    hourly_rate: Optional[float] = Form(100.00),
    consultation_fee: Optional[float] = Form(49.00),
    # File uploads
    diploma: Optional[UploadFile] = File(None),
    license_file: Optional[UploadFile] = File(None),
    id_document: Optional[UploadFile] = File(None),
    # Dependencies
    db: Session = Depends(get_db)
):
    """
    Register new lawyer (pre-verification)
    
    **Registrácia nového advokáta (pred overením)**
    
    - **user_id**: ID používateľa z tabuľky users
    - **full_name**: Celé meno advokáta
    - **license_number**: Číslo advokátskej licencie (musí byť unikátne)
    - **specializations**: JSON pole špecializácií
    - **diploma, license_file, id_document**: Dokumenty na overenie (PDF alebo obrázky)
    """
    try:
        from main import Lawyer
        import structlog
        
        logger = structlog.get_logger()
        
        # Parse JSON arrays
        try:
            specializations_list = json.loads(specializations)
            jurisdictions_list = json.loads(jurisdictions)
            languages_list = json.loads(languages)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Neplatný formát JSON pre specializations, jurisdictions alebo languages / Invalid JSON format"
            )
        
        # Validate jurisdictions
        try:
            validate_jurisdictions(jurisdictions_list)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Neplatná jurisdikcia / Invalid jurisdiction: {str(e)}"
            )
        
        # Check if lawyer already exists
        existing = db.query(Lawyer).filter(Lawyer.license_number == license_number).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Advokát s týmto číslom licencie už existuje / Lawyer with this license number already exists"
            )
        
        # Create lawyer record
        new_lawyer = Lawyer(
            user_id=user_id,
            full_name=full_name,
            title=title,
            license_number=license_number,
            bar_association=bar_association,
            jurisdictions=jurisdictions_list,
            specializations=specializations_list,
            languages=languages_list,
            experience_years=experience_years,
            bio=bio,
            education=education,
            hourly_rate=hourly_rate,
            consultation_fee=consultation_fee,
            is_verified=False,
            is_active=True
        )
        
        db.add(new_lawyer)
        db.commit()
        db.refresh(new_lawyer)
        
        logger.info("lawyer_registered",
                   lawyer_id=new_lawyer.id,
                   license_number=license_number,
                   user_id=user_id)
        
        return ApiResponse(
            success=True,
            message="Registrácia úspešná. Vaša žiadosť bude overená do 48 hodín. / Registration successful. Your application will be verified within 48 hours.",
            data={
                "lawyer_id": new_lawyer.id,
                "status": "pending_verification"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri registrácii / Registration error: {str(e)}"
        )


@router.get("/search", response_model=List[LawyerPublicProfile])
async def search_lawyers(
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction (e.g., SK, CZ, PL)"),
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    rating_min: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    available: Optional[bool] = Query(None, description="Only available lawyers"),
    language: Optional[str] = Query(None, description="Filter by language"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Search for lawyers (for clients)
    
    **Vyhľadávanie advokátov (pre klientov)**
    
    Returns list of verified and available lawyers matching criteria.
    Lawyers are filtered by jurisdiction - only lawyers licensed in the specified jurisdiction are returned.
    """
    try:
        from main import Lawyer
        from sqlalchemy import and_, or_
        
        query = db.query(Lawyer).filter(
            Lawyer.is_verified == True,
            Lawyer.is_active == True
        )
        
        # CRITICAL: Filter by jurisdiction
        # Only show lawyers who are licensed in the requested jurisdiction
        if jurisdiction:
            jurisdiction_upper = jurisdiction.upper()
            # Validate jurisdiction
            if jurisdiction_upper not in ACTIVE_JURISDICTION_CODES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Neplatná alebo neaktívna jurisdikcia / Invalid or inactive jurisdiction: {jurisdiction}"
                )
            # PostgreSQL JSONB contains
            query = query.filter(Lawyer.jurisdictions.contains([jurisdiction_upper]))
        
        # Apply other filters
        if specialization:
            # PostgreSQL JSONB contains
            query = query.filter(Lawyer.specializations.contains([specialization]))
        
        if rating_min:
            query = query.filter(Lawyer.average_rating >= rating_min)
        
        if language:
            # PostgreSQL JSONB contains - need to cast the array to JSONB
            from sqlalchemy import cast
            from sqlalchemy.dialects.postgresql import JSONB
            query = query.filter(Lawyer.languages.op('@>')(cast([language], JSONB)))
        
        # Order by rating
        query = query.order_by(Lawyer.average_rating.desc().nullslast())
        
        # Pagination
        lawyers = query.offset(offset).limit(limit).all()
        
        return lawyers
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri vyhľadávaní / Search error: {str(e)}"
        )


@router.get("/{lawyer_id}/profile", response_model=LawyerPublicProfile)
async def get_public_profile(
    lawyer_id: int,
    db: Session = Depends(get_db)
):
    """
    Get public lawyer profile
    
    **Získať verejný profil advokáta**
    """
    try:
        from main import Lawyer
        
        lawyer = db.query(Lawyer).filter(
            Lawyer.id == lawyer_id,
            Lawyer.is_verified == True
        ).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advokát nenájdený / Lawyer not found"
            )
        
        return lawyer
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/{lawyer_id}/reviews")
async def get_lawyer_reviews(
    lawyer_id: int,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get lawyer reviews
    
    **Získať recenzie advokáta**
    """
    try:
        from main import Review
        
        reviews = db.query(Review).filter(
            Review.lawyer_id == lawyer_id,
            Review.is_visible == True
        ).order_by(Review.created_at.desc()).offset(offset).limit(limit).all()
        
        return {"success": True, "data": [
            {
                "id": r.id,
                "rating": r.rating,
                "title": r.title,
                "comment": r.comment,
                "created_at": r.created_at
            } for r in reviews
        ]}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# PROTECTED ROUTES (authentication required)
# ============================================

@router.get("/me", response_model=LawyerPrivateProfile)
async def get_my_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current lawyer's private profile
    
    **Získať súkromný profil aktuálneho advokáta**
    """
    try:
        from main import Lawyer
        
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil advokáta nenájdený / Lawyer profile not found"
            )
        
        return lawyer
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.put("/me", response_model=ApiResponse)
async def update_profile(
    bio: Optional[str] = Form(None),
    hourly_rate: Optional[float] = Form(None),
    consultation_fee: Optional[float] = Form(None),
    is_active: Optional[bool] = Form(None),
    profile_photo: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update lawyer profile
    
    **Aktualizovať profil advokáta**
    """
    try:
        from main import Lawyer
        
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil advokáta nenájdený / Lawyer profile not found"
            )
        
        # Update fields
        if bio is not None:
            lawyer.bio = bio
        if hourly_rate is not None:
            lawyer.hourly_rate = hourly_rate
        if consultation_fee is not None:
            lawyer.consultation_fee = consultation_fee
        if is_active is not None:
            lawyer.is_active = is_active
        
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Profil úspešne aktualizovaný / Profile updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri aktualizácii / Update error: {str(e)}"
        )


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get lawyer dashboard statistics
    
    **Získať štatistiky pre dashboard advokáta**
    """
    try:
        from main import Lawyer, Order
        from sqlalchemy import func
        
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil advokáta nenájdený / Lawyer profile not found"
            )
        
        # Count active orders
        active_orders = db.query(func.count(Order.id)).filter(
            Order.lawyer_id == lawyer.id,
            Order.status.in_(['accepted', 'in_progress'])
        ).scalar() or 0
        
        # Count completed orders
        completed_orders = db.query(func.count(Order.id)).filter(
            Order.lawyer_id == lawyer.id,
            Order.status == 'completed'
        ).scalar() or 0
        
        return DashboardStats(
            average_rating=lawyer.average_rating or 0.0,
            total_reviews=lawyer.total_reviews or 0,
            total_cases=lawyer.total_cases or 0,
            active_orders=active_orders,
            completed_orders=completed_orders
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri načítaní štatistík / Error loading statistics: {str(e)}"
        )


@router.post("/availability", response_model=ApiResponse)
async def set_availability(
    is_active: bool = Form(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set lawyer availability
    
    **Nastaviť dostupnosť advokáta**
    """
    try:
        from main import Lawyer
        
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil advokáta nenájdený / Lawyer profile not found"
            )
        
        lawyer.is_active = is_active
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Dostupnosť úspešne aktualizovaná / Availability updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# ADMIN ROUTES
# ============================================

@router.get("/admin/pending-verification")
async def get_pending_verification(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get lawyers pending verification (Admin only)
    
    **Získať advokátov čakajúcich na overenie (iba Admin)**
    """
    # Check if user is admin
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Prístup zamietnutý / Access denied"
        )
    
    try:
        from main import Lawyer
        
        lawyers = db.query(Lawyer).filter(
            Lawyer.is_verified == False
        ).order_by(Lawyer.created_at.desc()).offset(offset).limit(limit).all()
        
        return {"success": True, "data": lawyers}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/admin/{lawyer_id}/verify", response_model=ApiResponse)
async def verify_lawyer(
    lawyer_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify a lawyer (Admin only)
    
    **Overiť advokáta (iba Admin)**
    """
    # Check if user is admin
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Prístup zamietnutý / Access denied"
        )
    
    try:
        from main import Lawyer
        from datetime import datetime
        
        lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advokát nenájdený / Lawyer not found"
            )
        
        lawyer.is_verified = True
        lawyer.verification_date = datetime.utcnow()
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Advokát úspešne overený / Lawyer verified successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/admin/{lawyer_id}/reject", response_model=ApiResponse)
async def reject_lawyer(
    lawyer_id: int,
    reason: str = Form(..., min_length=10),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reject a lawyer application (Admin only)
    
    **Zamietnuť žiadosť advokáta (iba Admin)**
    """
    # Check if user is admin
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Prístup zamietnutý / Access denied"
        )
    
    try:
        from main import Lawyer
        
        lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
        
        if not lawyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advokát nenájdený / Lawyer not found"
            )
        
        # Delete lawyer record
        db.delete(lawyer)
        db.commit()
        
        return ApiResponse(
            success=True,
            message="Žiadosť zamietnutá / Application rejected"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )
