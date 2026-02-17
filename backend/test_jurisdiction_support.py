"""
Test script for multi-jurisdiction support
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_jurisdiction_support():
    """Test jurisdiction filtering in marketplace"""
    
    print("Testing Multi-Jurisdiction Support\n")
    print("=" * 60)
    
    # Test 1: Search without jurisdiction (should return all lawyers)
    print("\n1. Search ALL lawyers (no jurisdiction filter)...")
    try:
        response = requests.get(f"{BASE_URL}/api/marketplace/lawyers/search")
        if response.status_code == 200:
            lawyers = response.json()
            print(f"   OK - Found {len(lawyers)} lawyers total")
            for lawyer in lawyers:
                print(f"      - {lawyer['full_name']}: {lawyer.get('jurisdictions', ['N/A'])}")
        else:
            print(f"   ERROR - Status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Search SK jurisdiction
    print("\n2. Search lawyers in SK jurisdiction...")
    try:
        response = requests.get(f"{BASE_URL}/api/marketplace/lawyers/search?jurisdiction=SK")
        if response.status_code == 200:
            lawyers = response.json()
            print(f"   OK - Found {len(lawyers)} Slovak lawyers")
            for lawyer in lawyers:
                jurisdictions = lawyer.get('jurisdictions', [])
                has_sk = 'SK' in jurisdictions
                print(f"      - {lawyer['full_name']}: {jurisdictions} {'✓' if has_sk else '✗'}")
        else:
            print(f"   ERROR - Status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Search CZ jurisdiction (should return empty or CZ lawyers)
    print("\n3. Search lawyers in CZ jurisdiction...")
    try:
        response = requests.get(f"{BASE_URL}/api/marketplace/lawyers/search?jurisdiction=CZ")
        if response.status_code == 200:
            lawyers = response.json()
            print(f"   OK - Found {len(lawyers)} Czech lawyers")
            if len(lawyers) == 0:
                print("      (No Czech lawyers registered yet - expected)")
        else:
            print(f"   ERROR - Status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 4: Search invalid jurisdiction
    print("\n4. Search with invalid jurisdiction (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/api/marketplace/lawyers/search?jurisdiction=INVALID")
        if response.status_code == 400:
            print("   OK - Correctly rejected invalid jurisdiction")
        else:
            print(f"   UNEXPECTED - Status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 5: Search inactive jurisdiction (DE - not yet active)
    print("\n5. Search with inactive jurisdiction DE (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/api/marketplace/lawyers/search?jurisdiction=DE")
        if response.status_code == 400:
            print("   OK - Correctly rejected inactive jurisdiction")
        else:
            print(f"   UNEXPECTED - Status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("Multi-jurisdiction test complete!")
    print("\nActive jurisdictions: SK, CZ, PL")
    print("Planned jurisdictions: DE, AT, FR, HU, RO, UA, EN")

if __name__ == "__main__":
    test_jurisdiction_support()
