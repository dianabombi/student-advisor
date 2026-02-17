#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Slovak language detection
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_slovak():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING SLOVAK LANGUAGE DETECTION")
    print("=" * 70)
    
    # Test 1: Direct Slovak request
    print("\n📝 Test 1: Slovak request for Ostrava")
    print("Message: Hľadám byt v Ostrave")
    
    response1 = await service.chat(
        message='Hľadám byt v Ostrave',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='CZ',
        db=db
    )
    
    print(f"Response length: {len(response1)} chars")
    print(f"Has Sreality: {'Sreality' in response1}")
    print(f"Response preview: {response1[:300]}...\n")
    
    # Test 2: Language switch request
    print("\n📝 Test 2: Language switch to Slovak")
    print("Message: A po slovensky?")
    
    # Simulate conversation history
    history = [
        {"role": "user", "content": "Шукаю гуртожиток в Остраві"},
        {"role": "assistant", "content": "Response in Ukrainian..."}
    ]
    
    response2 = await service.chat(
        message='A po slovensky?',
        conversation_history=history,
        user_name='Test User',
        language='uk',  # Frontend still thinks Ukrainian
        jurisdiction='CZ',
        db=db
    )
    
    print(f"Response length: {len(response2)} chars")
    print(f"Has Sreality: {'Sreality' in response2}")
    print(f"Response: {response2}\n")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_slovak())
