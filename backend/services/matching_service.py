"""
MATCHING SERVICE
Smart algorithm for matching clients with lawyers
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import Optional, List
from models.client import LawyerMatchResponse, Top3LawyersResponse

async def find_best_match(db: Session, case, service_type: str) -> Optional[LawyerMatchResponse]:
    """
    SCENARIO 1: Find best matching lawyer
    
    Scoring algorithm:
    - Specialization match: 40 points
    - Rating: 25 points
    - Success rate: 20 points
    - Availability: 10 points
    - Price competitiveness: 5 points
    """
    from main import Lawyer
    
    # Get all verified and active lawyers
    lawyers = db.query(Lawyer).filter(
        Lawyer.is_verified == True,
        Lawyer.is_active == True
    ).all()
    
    if not lawyers:
        return None
    
    # Score each lawyer
    scored_lawyers = []
    for lawyer in lawyers:
        score = _calculate_match_score(lawyer, case, service_type)
        scored_lawyers.append((lawyer, score))
    
    # Sort by score
    scored_lawyers.sort(key=lambda x: x[1], reverse=True)
    
    # Return best match
    if scored_lawyers:
        best_lawyer, best_score = scored_lawyers[0]
        return _lawyer_to_match_response(best_lawyer, best_score, service_type)
    
    return None


async def find_top_3(db: Session, case, service_type: str) -> Top3LawyersResponse:
    """
    SCENARIO 2: Find top 3 lawyers with different profiles
    
    Returns:
    1. Best overall (highest score)
    2. Fastest delivery
    3. Best price
    """
    from main import Lawyer
    
    # Get all verified and active lawyers
    lawyers = db.query(Lawyer).filter(
        Lawyer.is_verified == True,
        Lawyer.is_active == True
    ).all()
    
    if not lawyers:
        return Top3LawyersResponse(
            lawyers=[],
            total_available=0,
            recommendation={}
        )
    
    # Score all lawyers
    scored_lawyers = []
    for lawyer in lawyers:
        score = _calculate_match_score(lawyer, case, service_type)
        scored_lawyers.append((lawyer, score))
    
    # Sort by score
    scored_lawyers.sort(key=lambda x: x[1], reverse=True)
    
    # Select top 3 with different profiles
    top_3_lawyers = []
    
    # 1. Best overall
    if scored_lawyers:
        best_lawyer, best_score = scored_lawyers[0]
        match = _lawyer_to_match_response(best_lawyer, best_score, service_type)
        top_3_lawyers.append(match)
    
    # 2. Fastest (mock - would check average_response_time)
    if len(scored_lawyers) > 1:
        fast_lawyer, fast_score = scored_lawyers[1]
        match = _lawyer_to_match_response(fast_lawyer, fast_score, service_type)
        top_3_lawyers.append(match)
    
    # 3. Best price (mock - would check hourly_rate)
    if len(scored_lawyers) > 2:
        cheap_lawyer, cheap_score = scored_lawyers[2]
        match = _lawyer_to_match_response(cheap_lawyer, cheap_score, service_type)
        top_3_lawyers.append(match)
    
    return Top3LawyersResponse(
        lawyers=top_3_lawyers,
        total_available=len(lawyers),
        recommendation={
            "lawyer_id": top_3_lawyers[0].lawyer_id if top_3_lawyers else None,
            "reason": "Highest success rate for similar cases"
        }
    )


async def find_all_available(
    db: Session,
    case,
    service_type: str,
    sort: str = "recommended",
    limit: int = 20,
    offset: int = 0
) -> List[LawyerMatchResponse]:
    """
    SCENARIO 3: Get all available lawyers with sorting
    """
    from main import Lawyer
    
    query = db.query(Lawyer).filter(
        Lawyer.is_verified == True,
        Lawyer.is_active == True
    )
    
    # Apply sorting
    if sort == "rating":
        query = query.order_by(Lawyer.average_rating.desc().nullslast())
    elif sort == "price":
        query = query.order_by(Lawyer.hourly_rate.asc())
    elif sort == "speed":
        # Mock - would sort by average_response_time
        query = query.order_by(Lawyer.created_at.desc())
    else:  # recommended
        # Score-based sorting (mock - would calculate scores)
        query = query.order_by(Lawyer.average_rating.desc().nullslast())
    
    lawyers = query.offset(offset).limit(limit).all()
    
    # Convert to response models
    result = []
    for lawyer in lawyers:
        score = _calculate_match_score(lawyer, case, service_type)
        match = _lawyer_to_match_response(lawyer, score, service_type)
        result.append(match)
    
    return result


def _calculate_match_score(lawyer, case, service_type: str) -> int:
    """
    Calculate match score (0-100)
    
    Scoring:
    - Specialization match: 40 points
    - Rating: 25 points
    - Success rate: 20 points
    - Availability: 10 points
    - Price: 5 points
    """
    score = 0
    
    # 1. Specialization match (40 points)
    if hasattr(case, 'category') and hasattr(lawyer, 'specializations'):
        if case.category in (lawyer.specializations or []):
            score += 40
        else:
            score += 10  # Partial credit
    
    # 2. Rating (25 points)
    if lawyer.average_rating:
        score += int((lawyer.average_rating / 5.0) * 25)
    
    # 3. Success rate (20 points) - mock
    # Would calculate from historical data
    score += 15  # Default
    
    # 4. Availability (10 points)
    if lawyer.is_active:
        score += 10
    
    # 5. Price competitiveness (5 points)
    # Mock - would compare with average
    score += 3
    
    return min(score, 100)


def _lawyer_to_match_response(lawyer, match_score: int, service_type: str) -> LawyerMatchResponse:
    """Convert Lawyer model to LawyerMatchResponse"""
    
    # Calculate price based on service type
    price_map = {
        'document_review': lawyer.hourly_rate * 2 if lawyer.hourly_rate else 150.00,
        'consultation': lawyer.consultation_fee if lawyer.consultation_fee else 100.00,
        'full_service': lawyer.hourly_rate * 10 if lawyer.hourly_rate else 500.00
    }
    price = price_map.get(service_type, 150.00)
    
    # Estimate delivery time
    delivery_map = {
        'document_review': "2-3 days",
        'consultation': "1 day",
        'full_service': "1-2 weeks"
    }
    estimated_delivery = delivery_map.get(service_type, "3 days")
    
    return LawyerMatchResponse(
        lawyer_id=lawyer.id,
        full_name=lawyer.full_name,
        title=lawyer.title or "JUDr.",
        rating=lawyer.average_rating or 0.0,
        total_reviews=lawyer.total_reviews or 0,
        success_rate=85.0,  # Mock - would calculate from data
        average_response_time=24,  # Mock - hours
        specializations=lawyer.specializations or [],
        languages=lawyer.languages or ["sk"],
        years_of_experience=lawyer.experience_years or 5,
        bio=lawyer.bio,
        match_percentage=match_score,
        price=price,
        estimated_delivery=estimated_delivery
    )
