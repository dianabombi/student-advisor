"""
STRIPE SERVICE
Integration with Stripe payment gateway (MVP version)
"""

import os
from typing import Dict, Optional
import uuid

# Stripe API key from environment
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_mock')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_mock')

# Mock mode if no real Stripe keys
MOCK_MODE = STRIPE_SECRET_KEY == 'sk_test_mock'

if not MOCK_MODE:
    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
    except ImportError:
        print("⚠️ Stripe library not installed. Using mock mode.")
        MOCK_MODE = True


async def create_payment_intent(
    amount: float,
    currency: str,
    order_id: int,
    customer_email: str,
    metadata: Optional[Dict] = None
) -> Dict:
    """
    Create Stripe payment intent
    
    Args:
        amount: Amount in EUR
        currency: Currency code (EUR)
        order_id: Order ID
        customer_email: Customer email
        metadata: Additional metadata
    
    Returns:
        Payment intent object
    """
    if MOCK_MODE:
        # Mock payment intent for testing
        payment_intent_id = f"pi_mock_{uuid.uuid4().hex[:16]}"
        return {
            "id": payment_intent_id,
            "client_secret": f"{payment_intent_id}_secret_mock",
            "status": "requires_payment_method",
            "amount": amount,
            "currency": currency.lower(),
            "metadata": {
                "order_id": str(order_id),
                **(metadata or {})
            }
        }
    
    # Real Stripe integration
    try:
        amount_cents = int(amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency.lower(),
            receipt_email=customer_email,
            metadata={
                "order_id": str(order_id),
                **(metadata or {})
            },
            automatic_payment_methods={
                "enabled": True
            }
        )
        
        return {
            "id": intent.id,
            "client_secret": intent.client_secret,
            "status": intent.status,
            "amount": amount,
            "currency": currency
        }
        
    except Exception as e:
        raise Exception(f"Stripe error: {str(e)}")


async def verify_webhook(payload: bytes, sig_header: str):
    """
    Verify Stripe webhook signature
    
    Args:
        payload: Raw request body
        sig_header: Stripe-Signature header
    
    Returns:
        Verified event object
    """
    if MOCK_MODE:
        # Mock webhook event
        import json
        return json.loads(payload)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


async def create_refund(
    payment_intent_id: str,
    amount: Optional[float] = None,
    reason: str = "requested_by_customer"
) -> Dict:
    """
    Create a refund
    
    Args:
        payment_intent_id: Payment Intent ID to refund
        amount: Amount to refund (None = full refund)
        reason: Refund reason
    
    Returns:
        Refund object
    """
    if MOCK_MODE:
        # Mock refund
        return {
            "id": f"re_mock_{uuid.uuid4().hex[:16]}",
            "amount": amount or 0,
            "status": "succeeded",
            "reason": reason
        }
    
    try:
        refund_params = {
            "payment_intent": payment_intent_id,
            "reason": reason
        }
        
        if amount:
            refund_params["amount"] = int(amount * 100)
        
        refund = stripe.Refund.create(**refund_params)
        
        return {
            "id": refund.id,
            "amount": refund.amount / 100,
            "status": refund.status,
            "reason": refund.reason
        }
        
    except Exception as e:
        raise Exception(f"Refund error: {str(e)}")


async def create_payout(
    amount: float,
    destination_account: str,
    description: str
) -> Dict:
    """
    Create payout to connected account
    
    Args:
        amount: Amount in EUR
        destination_account: Stripe connected account ID
        description: Payout description
    
    Returns:
        Payout object
    """
    if MOCK_MODE:
        # Mock payout
        return {
            "id": f"po_mock_{uuid.uuid4().hex[:16]}",
            "amount": amount,
            "status": "paid",
            "arrival_date": None
        }
    
    try:
        payout = stripe.Payout.create(
            amount=int(amount * 100),
            currency="eur",
            destination=destination_account,
            description=description
        )
        
        return {
            "id": payout.id,
            "amount": amount,
            "status": payout.status,
            "arrival_date": payout.arrival_date
        }
        
    except Exception as e:
        raise Exception(f"Payout error: {str(e)}")
