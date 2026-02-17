#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Slovak city detection fix
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_slovak_fix():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING SLOVAK CITY DETECTION FIX")
    print("=" * 70)
    
    # Test that caused the bug
    print("\n📝 Test 1: Slovak query for Warsaw (previously matched Amsterdam)")
    response = await service.chat(
        message='Hľadám byt vo Varšave',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='PL',
        db=db
    )
    
    has_warsaw_portals = 'otodom' in response.lower() or 'olx' in response.lower()
    has_amsterdam = 'amsterdam' in response.lower()
    
    print(f"✅ Has Warsaw portals: {has_warsaw_portals}")
    print(f"❌ Has Amsterdam: {has_amsterdam}")
    print(f"\nResponse preview:\n{response[:300]}")
    
    # Test that Amsterdam still works when explicitly mentioned
    print("\n\n📝 Test 2: Explicit Amsterdam query (should still work)")
    response2 = await service.chat(
        message='Hľadám byt v Amsterdame',
        conversation_history=[],
        user_name='Test User',
        language='sk',
        jurisdiction='NL',
        db=db
    )
    
    has_amsterdam2 = 'amsterdam' in response2.lower()
    print(f"✅ Has Amsterdam: {has_amsterdam2}")
    print(f"\nResponse preview:\n{response2[:300]}")
    
    db.close()
    
    print("\n" + "=" * 70)
    if has_warsaw_portals and not has_amsterdam and has_amsterdam2:
        print("✅ FIX SUCCESSFUL!")
    else:
        print("⚠️ FIX INCOMPLETE")

if __name__ == "__main__":
    asyncio.run(test_slovak_fix())
