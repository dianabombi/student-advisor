
import sys
import unittest
from unittest.mock import MagicMock

# Add the project root to the python path
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService

class MockDB:
    def __init__(self):
        self.query_mock = MagicMock()
        self.query_mock.filter.return_value.all.return_value = []
    
    def query(self, model):
        return self.query_mock

class TestAustrianJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_at(self):
        """Test extraction of Austrian cities with synonyms"""
        test_cases = [
            ("Ich suche Arbeit in Wien", "Wien"),
            ("Job in Vienna", "Wien"),
            ("Praca we Wiedniu", "Wien"),
            ("Lavoro a Vienna", "Wien"),
            ("Jobs in Salzburg", "Salzburg"),
            ("Job Graz", "Graz"),
            ("Arbeit in Linz", "Linz"),
            ("Innsbruck jobs", "Innsbruck")
        ]
        
        print("\nTesting Austrian City Extraction (country_code='AT'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'AT')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            self.assertEqual(city, expected)

    def test_context_generation(self):
        """Test partial instruction generation for Austrian portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Karriere.at - Wien"
        agency1.website_url = "https://www.karriere.at/jobs/wien?keywords=student"
        
        agency2 = MagicMock()
        agency2.name = "Hogastjob - Wien"
        agency2.website_url = "https://www.hogastjob.com/jobs?location=Wien"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "Wien", "AT")
        
        print("\nTesting Context Generation for Wien:")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN WIEN", context)
        self.assertIn("Karriere.at - Wien", context)
        # Verify instructions
        self.assertIn("keyword 'Student'", context)
        self.assertIn("tourism/seasonal", context)

if __name__ == '__main__':
    unittest.main()
