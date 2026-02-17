#!/usr/bin/env python3
"""
Test script to trigger university scraping
"""
import requests
import time

# Test universities
universities = [
    {"id": 20, "name": "Czech Technical University in Prague"},
    {"id": 21, "name": "Masaryk University"},
    {"id": 5, "name": "Matej Bel University in Banská Bystrica"},
]

API_BASE = "http://localhost:8002"

print("🚀 Starting university scraping test...")
print(f"Will scrape {len(universities)} universities\n")

for univ in universities:
    print(f"📚 Scraping: {univ['name']} (ID: {univ['id']})")
    
    try:
        # Note: This endpoint requires authentication
        # For testing, we'll call the Celery task directly
        response = requests.post(
            f"{API_BASE}/api/admin/scrape-university/{univ['id']}",
            headers={"Authorization": "Bearer test_token"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Queued: {result}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    time.sleep(1)

print("\n✅ Scraping tasks queued!")
print("Check status with: docker logs student-celery-worker-1")
