"""Check what backend returns for login"""
import requests

# Login
response = requests.post(
    'http://localhost:8002/api/auth/login',
    data={
        'username': 'Eduard.pavlyshche@gmail.com',
        'password': input('Enter password: ')
    },
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

print("Status Code:", response.status_code)
print("\nResponse JSON:")
import json
print(json.dumps(response.json(), indent=2))

# Check if role is in response
data = response.json()
if 'user' in data:
    print("\n" + "="*60)
    print("USER OBJECT:")
    print("="*60)
    for key, value in data['user'].items():
        print(f"  {key}: {value}")
    
    if 'role' in data['user']:
        print(f"\n✅ Role found: {data['user']['role']}")
    else:
        print("\n❌ Role NOT found in user object!")
