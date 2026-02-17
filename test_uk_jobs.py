
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

class TestUKJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_gb(self):
        """Test extraction of UK cities with synonyms (multilingual)"""
        # Note: country_code for UK is 'GB' in DB and logic
        test_cases = [
            ("I need a job in London", "London"),
            ("Praca w Londynie", "London"),
            ("Lavoro a Londra", "London"),
            ("Trabajo en Londres", "London"),
            ("Jobs in Cambridge", "Cambridge"),
            ("Work Manchester", "Manchester"),
            ("Praca Edinburgh", "Edinburgh"),
            ("Oxford jobs", "Oxford")
        ]
        
        print("\nTesting UK City Extraction (country_code='GB'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'GB')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            self.assertEqual(city, expected)

    def test_context_generation(self):
        """Test partial instruction generation for UK portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Reed.co.uk - London"
        agency1.website_url = "https://www.reed.co.uk/jobs/london?keywords=student"
        
        agency2 = MagicMock()
        agency2.name = "Totaljobs - London"
        agency2.website_url = "https://www.totaljobs.com/jobs/student/in-london"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "London", "GB")
        
        print("\nTesting Context Generation for London (GB):")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN LONDON", context)
        self.assertIn("Reed.co.uk - London", context)
        # Verify instructions
        self.assertIn("student", context.lower())

if __name__ == '__main__':
    unittest.main()
