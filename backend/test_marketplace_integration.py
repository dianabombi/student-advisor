"""
Test script to verify marketplace API integration
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_marketplace_endpoints():
    """Test if marketplace endpoints are accessible"""
    
    print("Testing Marketplace API Integration\n")
    print("=" * 50)
    
    # Test 1: Check if API docs are accessible
    print("\n1. Testing API Documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("   OK - Swagger UI accessible at http://localhost:8001/docs")
        else:
            print(f"   ERROR - Swagger UI returned status {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Check if lawyer search endpoint exists
    print("\n2. Testing Lawyer Search Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/marketplace/lawyers/search")
        if response.status_code in [200, 422]:  # 200 OK or 422 Validation Error is fine
            print(f"   OK - Lawyer search endpoint exists (status: {response.status_code})")
            if response.status_code == 200:
                data = response.json()
                print(f"   Found {len(data)} lawyers")
        else:
            print(f"   ERROR - Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Check OpenAPI schema
    print("\n3. Testing OpenAPI Schema...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            marketplace_paths = [p for p in schema.get('paths', {}).keys() if 'marketplace' in p]
            print(f"   OK - Found {len(marketplace_paths)} marketplace endpoints:")
            for path in marketplace_paths[:5]:  # Show first 5
                print(f"      - {path}")
            if len(marketplace_paths) > 5:
                print(f"      ... and {len(marketplace_paths) - 5} more")
        else:
            print(f"   ERROR - OpenAPI schema returned status {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Integration test complete!")
    print("\nNext steps:")
    print("   1. Visit http://localhost:8001/docs to see all endpoints")
    print("   2. Test lawyer registration endpoint")
    print("   3. Create test data")

if __name__ == "__main__":
    test_marketplace_endpoints()
