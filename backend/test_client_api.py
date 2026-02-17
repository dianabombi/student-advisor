"""
Test Client API Endpoints
Tests the 3 main scenarios from Krok 3
"""

import requests
import json

BASE_URL = "http://localhost:8001"

# You need a valid JWT token - get it from login
# For testing, we'll use a mock token or skip auth
TOKEN = None  # Will be set after login

def login():
    """Login to get JWT token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={
            "username": "test@example.com",  # Replace with real user
            "password": "password123"
        }
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    return None

def test_create_case():
    """TEST 1: Create a legal case"""
    print("\n" + "="*60)
    print("TEST 1: Creating legal case...")
    print("="*60)
    
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    case_data = {
        "title": "Nezákonná pokuta v MHD",
        "description": "Dostal som pokutu 50€ za cestovanie bez lístka, ale lístok som mal. Kontrolór ho neuznал a vystavil pokutu. Mám fotku lístka a chcem sa odvolať.",
        "category": "transport_law",
        "case_type": "transport_fine",
        "urgency": "medium"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/client/cases",
            json=case_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            print("✅ TEST 1 PASSED: Case created successfully!")
            return response.json().get("id")
        else:
            print(f"⚠️ TEST 1 FAILED: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ TEST 1 ERROR: {str(e)}")
        return None


def test_analyze_case(case_id):
    """TEST 2: AI analysis of case"""
    print("\n" + "="*60)
    print(f"TEST 2: Analyzing case {case_id}...")
    print("="*60)
    
    if not case_id:
        print("⚠️ Skipping - no case_id")
        return False
    
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/client/cases/{case_id}/analyze",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 AI Analysis Results:")
            print(f"   Complexity: {data.get('complexity_score')}/10")
            print(f"   Success Probability: {data.get('success_probability')}%")
            print(f"   Recommended Action: {data.get('recommended_action')}")
            print("✅ TEST 2 PASSED: AI analysis completed!")
            return True
        else:
            print(f"⚠️ TEST 2 FAILED: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ TEST 2 ERROR: {str(e)}")
        return False


def test_match_lawyer(case_id):
    """TEST 3: Auto-match lawyer (SCENARIO 1)"""
    print("\n" + "="*60)
    print(f"TEST 3: Auto-matching lawyer for case {case_id}...")
    print("="*60)
    
    if not case_id:
        print("⚠️ Skipping - no case_id")
        return False
    
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/client/cases/{case_id}/match-lawyer",
            params={"service_type": "document_review"},
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n👨‍⚖️ Best Matched Lawyer:")
            print(f"   Name: {data.get('full_name')}")
            print(f"   Rating: {data.get('rating')}/5")
            print(f"   Match: {data.get('match_percentage')}%")
            print(f"   Price: €{data.get('price')}")
            print(f"   Delivery: {data.get('estimated_delivery')}")
            print("✅ TEST 3 PASSED: Lawyer matched successfully!")
            return True
        else:
            print(f"⚠️ TEST 3 FAILED: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ TEST 3 ERROR: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CLIENT API ENDPOINT TESTING")
    print("="*60)
    
    # Try to login (optional)
    global TOKEN
    print("\nAttempting login...")
    TOKEN = login()
    if TOKEN:
        print("✅ Logged in successfully")
    else:
        print("⚠️ Login failed - testing without auth (may fail)")
    
    # Test 1: Create case
    case_id = test_create_case()
    
    # Test 2: AI analysis
    if case_id:
        test_analyze_case(case_id)
    
    # Test 3: Match lawyer
    if case_id:
        test_match_lawyer(case_id)
    
    print("\n" + "="*60)
    print("TESTING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
