#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Slovakia housing to see how it works
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_slovakia():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING SLOVAKIA (WORKING)")
    print("=" * 70)
    
    response = await service.chat(
        message='Hľadám byt v Bratislave',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='SK',
        db=db
    )
    
    print(f"\nResponse length: {len(response)}")
    print(f"Has Nehnuteľnosti: {'nehnuteľnosti' in response.lower() or 'nehnutelnosti' in response.lower()}")
    print(f"\nResponse preview:\n{response[:500]}")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_slovakia())
