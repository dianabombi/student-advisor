"""
MARKETPLACE PAYMENTS ROUTES
API endpoints for marketplace payment processing

Base path: /api/marketplace/payments
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from sqlalchemy.orm import Session

from models.marketplace_payment import (
    CreatePaymentRequest,
    WithdrawRequest,
    CreateDisputeRequest,
    ResolveDisputeRequest,
    PaymentIntentResponse,
    TransactionResponse,
    WalletResponse,
    DisputeResponse
)
from main import get_current_user, get_current_lawyer, get_db, logger
from auth.rbac import require_admin
from services import marketplace_payment_service, escrow_service, stripe_service

router = APIRouter(prefix="/api/marketplace/payments", tags=["Marketplace Payments"])

# ============================================
# CLIENT PAYMENT ENDPOINTS
# ============================================

@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
    payment_data: CreatePaymentRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create payment intent for marketplace order
    
    **Vytvoriť platobný intent pre objednávku**
    """
    try:
        # Get order
        order = await marketplace_payment_service.get_order(db, payment_data.order_id)
        
        # Verify order belongs to user
        if order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Check if already paid
        if order.status not in ['pending_payment', 'payment_failed']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Objednávka už je zaplatená / Order already paid"
            )
        
        # Create payment intent
        payment_intent = await stripe_service.create_payment_intent(
            amount=float(order.service_price),
            currency="EUR",
            order_id=payment_data.order_id,
            customer_email=current_user.email,
            metadata={
                "order_number": order.order_number,
                "client_id": current_user.id
            }
        )
        
        # Create transaction record
        await marketplace_payment_service.create_transaction(
            db=db,
            order_id=payment_data.order_id,
            transaction_type="payment",
            amount=float(order.service_price),
            payment_method="stripe",
            payment_id=payment_intent['id'],
            status="pending"
        )
        
        logger.info("payment_intent_created", order_id=payment_data.order_id, amount=order.service_price)
        
        return PaymentIntentResponse(
            payment_intent_id=payment_intent['id'],
            client_secret=payment_intent['client_secret'],
            amount=float(order.service_price),
            currency="EUR",
            status=payment_intent['status'],
            checkout_url=f"/checkout/{payment_intent['id']}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("payment_intent_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/webhook/stripe", include_in_schema=False)
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Stripe webhook handler
    
    Handles: payment_intent.succeeded, payment_intent.payment_failed
    """
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature', '')
        
        # Verify webhook signature
        event = await stripe_service.verify_webhook(payload, sig_header)
        
        # Handle different event types
        if event.get('type') == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_id = int(payment_intent['metadata']['order_id'])
            
            # Update transaction status
            await marketplace_payment_service.update_transaction_status(
                db=db,
                payment_id=payment_intent['id'],
                status="completed"
            )
            
            # Move money to escrow
            await escrow_service.hold_funds(
                db=db,
                order_id=order_id,
                amount=payment_intent['amount'] / 100
            )
            
            # Update order status
            await marketplace_payment_service.update_order_status(
                db=db,
                order_id=order_id,
                status="payment_confirmed"
            )
            
            logger.info("payment_succeeded", order_id=order_id)
        
        elif event.get('type') == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            
            await marketplace_payment_service.update_transaction_status(
                db=db,
                payment_id=payment_intent['id'],
                status="failed"
            )
            
            logger.warning("payment_failed", payment_id=payment_intent['id'])
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error("webhook_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook error: {str(e)}"
        )


@router.get("/transactions", response_model=List[TransactionResponse])
async def get_my_transactions(
    limit: int = 20,
    offset: int = 0,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's transaction history
    
    **Získať históriu transakcií**
    """
    try:
        transactions = await marketplace_payment_service.get_user_transactions(
            db=db,
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# LAWYER PAYOUT ENDPOINTS
# ============================================

@router.get("/wallet", response_model=WalletResponse)
async def get_wallet(
    current_lawyer = Depends(get_current_lawyer),
    db: Session = Depends(get_db)
):
    """
    Get lawyer's wallet/balance
    
    **Získať peňaženku advokáta**
    """
    try:
        wallet = await marketplace_payment_service.get_lawyer_wallet(db, current_lawyer['id'])
        return wallet
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/withdraw")
async def request_withdrawal(
    withdraw_data: WithdrawRequest,
    current_lawyer = Depends(get_current_lawyer),
    db: Session = Depends(get_db)
):
    """
    Request withdrawal of available balance
    
    **Požiadať o výber zostatku**
    """
    try:
        # Check available balance
        wallet = await marketplace_payment_service.get_lawyer_wallet(db, current_lawyer['id'])
        
        if withdraw_data.amount > wallet['available_balance']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nedostatok prostriedkov. Dostupné: €{wallet['available_balance']}"
            )
        
        # Minimum withdrawal
        if withdraw_data.amount < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimálna suma na výber je €10"
            )
        
        # Create withdrawal request
        withdrawal = await marketplace_payment_service.create_withdrawal_request(
            db=db,
            lawyer_id=current_lawyer['id'],
            amount=withdraw_data.amount,
            bank_account=withdraw_data.bank_account,
            note=withdraw_data.note
        )
        
        logger.info("withdrawal_requested", lawyer_id=current_lawyer['id'], amount=withdraw_data.amount)
        
        return {
            "success": True,
            "message": "Žiadosť o výber vytvorená. Prostriedky budú odoslané do 2-3 pracovných dní.",
            "data": {
                "withdrawal_number": withdrawal.withdrawal_number,
                "amount": float(withdrawal.amount),
                "status": withdrawal.status
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/withdrawals")
async def get_withdrawal_history(
    limit: int = 20,
    offset: int = 0,
    current_lawyer = Depends(get_current_lawyer),
    db: Session = Depends(get_db)
):
    """
    Get withdrawal history
    
    **Získať históriu výberov**
    """
    try:
        withdrawals = await marketplace_payment_service.get_withdrawal_history(
            db=db,
            lawyer_id=current_lawyer['id'],
            limit=limit,
            offset=offset
        )
        return {"success": True, "data": withdrawals}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# DISPUTE ENDPOINTS
# ============================================

@router.post("/disputes", status_code=status.HTTP_201_CREATED)
async def create_dispute(
    dispute_data: CreateDisputeRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a dispute for an order
    
    **Vytvoriť spor**
    """
    try:
        # Get order
        order = await marketplace_payment_service.get_order(db, dispute_data.order_id)
        
        # Verify order belongs to user
        if order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nemáte oprávnenie / Not authorized"
            )
        
        # Check if order can be disputed
        if order.status not in ['delivered', 'completed']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Objednávka nemôže byť sporná v tomto stave"
            )
        
        # Create dispute
        dispute = await marketplace_payment_service.create_dispute(
            db=db,
            order_id=dispute_data.order_id,
            raised_by='client',
            client_id=current_user.id,
            lawyer_id=order.lawyer_id,
            reason=dispute_data.reason.value,
            description=dispute_data.description,
            requested_refund_amount=dispute_data.requested_refund_amount
        )
        
        # Freeze escrow
        await escrow_service.freeze_funds(db, dispute_data.order_id)
        
        # Update order status
        await marketplace_payment_service.update_order_status(db, dispute_data.order_id, "disputed")
        
        logger.info("dispute_created", order_id=dispute_data.order_id, reason=dispute_data.reason)
        
        return {
            "success": True,
            "message": "Spor vytvorený. Náš tím ho preskúma do 48 hodín.",
            "data": {"dispute_id": dispute.id}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/disputes", response_model=List[DisputeResponse])
async def get_my_disputes(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's disputes
    
    **Získať spory**
    """
    try:
        disputes = await marketplace_payment_service.get_user_disputes(db, current_user.id)
        return disputes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# ADMIN ENDPOINTS
# ============================================

@router.get("/admin/pending-withdrawals")
async def get_pending_withdrawals(
    current_admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get pending withdrawal requests (Admin only)
    """
    try:
        from main import Withdrawal
        withdrawals = db.query(Withdrawal).filter(Withdrawal.status == 'pending').all()
        return {"success": True, "data": withdrawals}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/admin/withdrawals/{withdrawal_id}/approve")
async def approve_withdrawal(
    withdrawal_id: int,
    current_admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Approve withdrawal request (Admin only)
    """
    try:
        await marketplace_payment_service.approve_withdrawal(
            db=db,
            withdrawal_id=withdrawal_id,
            admin_id=current_admin.id
        )
        
        logger.info("withdrawal_approved", withdrawal_id=withdrawal_id, admin_id=current_admin.id)
        
        return {
            "success": True,
            "message": "Výber schválený"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/admin/disputes/{dispute_id}/resolve")
async def resolve_dispute(
    resolve_data: ResolveDisputeRequest,
    current_admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Resolve a dispute (Admin only)
    """
    try:
        dispute = await marketplace_payment_service.get_dispute(db, resolve_data.dispute_id)
        
        # Resolve dispute
        await marketplace_payment_service.resolve_dispute(
            db=db,
            dispute_id=resolve_data.dispute_id,
            resolution=resolve_data.resolution,
            refund_amount=resolve_data.refund_amount,
            admin_id=current_admin.id
        )
        
        # Handle refund if needed
        if resolve_data.refund_to_client and resolve_data.refund_amount > 0:
            await escrow_service.refund_to_client(
                db=db,
                order_id=dispute.order_id,
                amount=resolve_data.refund_amount
            )
        else:
            # Release to lawyer
            await escrow_service.release_to_lawyer(
                db=db,
                order_id=dispute.order_id
            )
        
        # Update order status
        await marketplace_payment_service.update_order_status(db, dispute.order_id, "completed")
        
        logger.info("dispute_resolved", dispute_id=resolve_data.dispute_id, admin_id=current_admin.id)
        
        return {
            "success": True,
            "message": "Spor vyriešený"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )
