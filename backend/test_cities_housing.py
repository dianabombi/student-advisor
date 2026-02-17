#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Housing AI for different cities
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_cities():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 60)
    print("TESTING HOUSING AI FOR DIFFERENT CITIES")
    print("=" * 60)
    
    # Test Nitra
    print("\n📝 Test 1: Nitra")
    response1 = await service.chat(
        message='Hľadám byt v Nitre',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='SK',
        db=db
    )
    print(f"Response length: {len(response1)}")
    print(f"Response:\n{response1}\n")
    
    # Test Banská Bystrica
    print("\n📝 Test 2: Banská Bystrica")
    response2 = await service.chat(
        message='Hľadám byt v Banskej Bystrici',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='SK',
        db=db
    )
    print(f"Response length: {len(response2)}")
    print(f"Response:\n{response2}\n")
    
    db.close()
    print("\n✅ Tests completed!")

if __name__ == "__main__":
    asyncio.run(test_cities())
