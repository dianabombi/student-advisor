
import asyncio
import os
import sys

# Get abs path to 'backend' directory and root
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')

if backend_dir not in sys.path:
    sys.path.append(backend_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Mock slowapi to avoid import error in backend.main
from unittest.mock import MagicMock
sys.modules['slowapi'] = MagicMock()
sys.modules['slowapi.errors'] = MagicMock()
sys.modules['slowapi.util'] = MagicMock()
# Also mock services.ocr_service.OCRService if needed, but slowapi is priority

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mock database session
class MockDB:
    def query(self, model):
        return self
    
    def filter(self, *args, **kwargs):
        return self
    
    def all(self):
        # Return mock agencies for Luxembourg
        class MockAgency:
            def __init__(self, name, url, city):
                self.name = name
                self.website_url = url
                self.city = city
                self.country_code = 'LU'
                self.description = "Mock description"
                self.specialization = "Mock specialization"
                self.is_active = True
                
        return [
            MockAgency("Jobs.lu", "https://www.jobs.lu", "Luxembourg"),
            MockAgency("Moovijob.com", "https://www.moovijob.com", "Luxembourg"),
            MockAgency("Jugendinfo.lu", "https://www.jugendinfo.lu", "Luxembourg")
        ]

async def test_luxembourg_response():
    try:
        from backend.services.jobs_chat_service import JobsChatService
        
        service = JobsChatService()
        
        # Test Case 1: Ukrainian user asking for work in Luxembourg
        print("\n--- TEST CASE 1: UKRAINIAN ---")
        msg_uk = "Я шукаю роботу для студента в Люксембурзі"
        history = []
        
        print(f"User: {msg_uk.encode('ascii', 'replace').decode('ascii')}")
        response_uk = await service.chat(
            message=msg_uk,
            conversation_history=history,
            user_name="Oleh",
            language="uk",
            jurisdiction="LU",
            db=MockDB()
        )
        print(f"AI: {response_uk.encode('ascii', 'replace').decode('ascii')}")
        
        # Test Case 2: English user asking for work in Esch
        print("\n--- TEST CASE 2: ENGLISH (Esch-sur-Alzette) ---")
        msg_en = "I need a student job in Esch"
        
        print(f"User: {msg_en}")
        response_en = await service.chat(
            message=msg_en,
            conversation_history=history,
            user_name="John",
            language="en",
            jurisdiction="LU",
            db=MockDB()
        )
        print(f"AI: {response_en}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_luxembourg_response())
