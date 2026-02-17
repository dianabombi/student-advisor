"""Test login API with provided password"""
import requests
import json

password = '1111111111'

print("\n" + "="*60)
print("TESTING LOGIN API")
print("="*60)

response = requests.post(
    'http://localhost:8002/api/auth/login',
    data={
        'username': 'Eduard.pavlyshche@gmail.com',
        'password': password
    },
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print("\n" + "="*60)
    print("FULL RESPONSE:")
    print("="*60)
    print(json.dumps(data, indent=2))
    
    print("\n" + "="*60)
    print("USER OBJECT:")
    print("="*60)
    if 'user' in data:
        for key, value in data['user'].items():
            print(f"  {key}: {value}")
        
        if 'role' in data['user']:
            print(f"\n✅ SUCCESS! Role found: {data['user']['role']}")
        else:
            print("\n❌ FAIL! Role NOT found in user object!")
            print("\nAvailable fields:", list(data['user'].keys()))
    else:
        print("❌ No 'user' field in response!")
else:
    print(f"\n❌ Login failed!")
    print(response.text)
