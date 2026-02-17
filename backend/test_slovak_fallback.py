
import sys
import asyncio
from unittest.mock import MagicMock, AsyncMock

# Add the project root to the python path
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService

async def test_fallback():
    service = JobsChatService()
    
    # Mock DB
    mock_db = MagicMock()
    # Mock query to return some agency
    mock_agency = MagicMock()
    mock_agency.name = "Test Agency"
    mock_agency.description = "Test Description"
    mock_agency.website_url = "http://test.com"
    mock_agency.specialization = "student"
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_agency]
    
    # Mock OpenAI client
    service.client = AsyncMock()
    service.client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Found: Test Agency"))
    ]
    
    print("--- Test 1: Message has NO city, but Context HAS city ---")
    response = await service.chat(
        message="Hladam brigadu",
        conversation_history=[],
        user_name="Student",
        language="sk",
        jurisdiction="SK",
        db=mock_db,
        city="Bratislava" # Context fallback
    )
    
    # Check if _get_agencies_context was called with "Bratislava"
    # We can't easily check internal calls without spying, but we can check if DB was queried
    # DB query filter calls: .filter(JobAgency.city == city, ...)
    # Let's verify DB interaction args if possible, or just rely on output mock?
    # Actually, in integration environment, we check logging or logical flow.
    
    print("Response logic executed.")
    # If city was used, DB should be queried.
    # If not used, DB might not be queried or queried with None?
    
    # Verify DB query was made
    print(f"DB Query called: {mock_db.query.called}")
    
    # Check if system prompt creation used "Bratislava" context
    # Hard to check without more mocking.
    
    # But if I run this in Docker with REAL DB, it is better.
    
if __name__ == "__main__":
    asyncio.run(test_fallback())
