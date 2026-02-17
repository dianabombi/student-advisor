#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Housing AI city detection and agency retrieval
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_housing_ai():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 60)
    print("TESTING HOUSING AI FOR SLOVAKIA")
    print("=" * 60)
    
    # Test 1: Slovak query
    print("\n📝 Test 1: Slovak query - 'Hľadám byt v Bratislave'")
    response = await service.chat(
        message='Hľadám byt v Bratislave',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='SK',
        db=db
    )
    print(f"✅ Response preview: {response[:300]}...")
    
    # Test 2: Ukrainian query
    print("\n📝 Test 2: Ukrainian query - 'Шукаю житло в Кошице'")
    response2 = await service.chat(
        message='Шукаю житло в Кошице',
        conversation_history=[],
        user_name='Test User',
        language='uk',
        jurisdiction='SK',
        db=db
    )
    print(f"✅ Response preview: {response2[:300]}...")
    
    # Test 3: Check database agencies
    print("\n📊 Database check:")
    from main import RealEstateAgency
    bratislava_agencies = db.query(RealEstateAgency).filter(
        RealEstateAgency.city == 'Bratislava',
        RealEstateAgency.country_code == 'SK'
    ).all()
    print(f"   Bratislava agencies: {len(bratislava_agencies)}")
    for agency in bratislava_agencies[:3]:
        print(f"     - {agency.name}")
    
    db.close()
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_housing_ai())
