"""
CLIENT SERVICE
Business logic for client operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List, Dict
from datetime import datetime
import uuid

async def create_case(db: Session, client_id: int, case_data: dict):
    """Create a new legal case"""
    from main import LegalCase
    
    # Generate case number
    case_number = f"CASE-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
    
    case = LegalCase(
        client_id=client_id,
        case_number=case_number,
        title=case_data['title'],
        description=case_data['description'],
        category=case_data['category'],
        case_type=case_data['case_type'],
        urgency=case_data['urgency'],
        status='draft'
    )
    
    db.add(case)
    db.commit()
    db.refresh(case)
    
    return case


async def get_case(db: Session, case_id: int):
    """Get case by ID"""
    from main import LegalCase
    
    case = db.query(LegalCase).filter(LegalCase.id == case_id).first()
    if not case:
        raise ValueError("Case not found")
    
    return case


async def get_my_cases(
    db: Session,
    client_id: int,
    status_filter: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List:
    """Get client's cases"""
    from main import LegalCase
    
    query = db.query(LegalCase).filter(LegalCase.client_id == client_id)
    
    if status_filter:
        query = query.filter(LegalCase.status == status_filter)
    
    query = query.order_by(LegalCase.created_at.desc())
    cases = query.offset(offset).limit(limit).all()
    
    return cases


async def update_case_status(db: Session, case_id: int, status: str):
    """Update case status"""
    from main import LegalCase
    
    case = db.query(LegalCase).filter(LegalCase.id == case_id).first()
    if case:
        case.status = status
        case.updated_at = datetime.now()
        db.commit()


async def save_ai_analysis(db: Session, case_id: int, analysis: dict):
    """Save AI analysis results to case"""
    from main import LegalCase
    
    case = db.query(LegalCase).filter(LegalCase.id == case_id).first()
    if case:
        case.ai_summary = analysis.get('recommended_action')
        case.ai_complexity_score = analysis.get('complexity_score')
        case.ai_success_probability = analysis.get('success_probability')
        case.ai_recommended_action = analysis.get('recommended_action')
        case.ai_analysis_completed_at = datetime.now()
        db.commit()


async def add_attachments(db: Session, case_id: int, attachments: List[dict]):
    """Add attachments to case"""
    from main import LegalCase
    
    case = db.query(LegalCase).filter(LegalCase.id == case_id).first()
    if case:
        # Store attachments in JSON field (if exists) or create new field
        if not hasattr(case, 'attachments'):
            # For now, just log it
            pass
        db.commit()


async def create_order(
    db: Session,
    case_id: int,
    client_id: int,
    lawyer_id: Optional[int],
    service_type: str
):
    """Create a new order"""
    from main import Order
    
    # Generate order number
    order_number = f"ORD-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
    
    # Calculate service price based on type
    price_map = {
        'document_review': 150.00,
        'consultation': 100.00,
        'full_service': 500.00
    }
    service_price = price_map.get(service_type, 150.00)
    
    order = Order(
        order_number=order_number,
        case_id=case_id,
        client_id=client_id,
        lawyer_id=lawyer_id,
        service_type=service_type,
        service_price=service_price,
        status='pending' if lawyer_id else 'seeking_lawyer',
        payment_status='pending'
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return order


async def get_order(db: Session, order_id: int):
    """Get order by ID"""
    from main import Order
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")
    
    return order


async def get_my_orders(
    db: Session,
    client_id: int,
    status_filter: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List:
    """Get client's orders"""
    from main import Order
    
    query = db.query(Order).filter(Order.client_id == client_id)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    query = query.order_by(Order.created_at.desc())
    orders = query.offset(offset).limit(limit).all()
    
    return orders


async def complete_order(db: Session, order_id: int):
    """Mark order as completed"""
    from main import Order
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = 'completed'
        order.completed_at = datetime.now()
        order.payment_status = 'completed'
        db.commit()


async def create_review(
    db: Session,
    order_id: int,
    client_id: int,
    lawyer_id: int,
    review_data: dict
):
    """Create a review for completed order"""
    from main import Review
    
    review = Review(
        order_id=order_id,
        client_id=client_id,
        lawyer_id=lawyer_id,
        rating=review_data['rating'],
        communication_rating=review_data.get('communication_rating'),
        professionalism_rating=review_data.get('professionalism_rating'),
        result_satisfaction=review_data.get('result_satisfaction'),
        speed_rating=review_data.get('speed_rating'),
        comment=review_data.get('comment'),
        is_visible=review_data.get('is_public', True)
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Update lawyer's average rating
    await _update_lawyer_rating(db, lawyer_id)
    
    return review


async def _update_lawyer_rating(db: Session, lawyer_id: int):
    """Update lawyer's average rating"""
    from main import Lawyer, Review
    from sqlalchemy import func
    
    # Calculate new average
    result = db.query(
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('total_reviews')
    ).filter(
        Review.lawyer_id == lawyer_id,
        Review.is_visible == True
    ).first()
    
    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
    if lawyer:
        lawyer.average_rating = round(result.avg_rating, 2) if result.avg_rating else 0.0
        lawyer.total_reviews = result.total_reviews or 0
        db.commit()
