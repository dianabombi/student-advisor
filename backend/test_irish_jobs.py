
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

class TestIrishJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_ie(self):
        """Test extraction of Irish cities with synonyms"""
        # Note: country_code for Ireland is 'IE'
        test_cases = [
            ("I need a job in Dublin", "Dublin"),
            ("Praca w Dublinie", "Dublin"), # PL
            ("Lavoro a Dublino", "Dublin"), # IT
            ("Trabajo en Dublin", "Dublin"), # ES
            ("Jobs in Cork", "Cork"),
            ("Corcaigh jobs", "Cork"), # Irish
            ("Gaillimh work", "Galway"), # Irish
            ("Praca Limerick", "Limerick"),
            ("Maynooth student job", "Maynooth") # No synonyms needed for Maynooth usually
        ]
        
        print("\nTesting Irish City Extraction (country_code='IE'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'IE')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            self.assertEqual(city, expected)

    def test_context_generation(self):
        """Test partial instruction generation for Irish portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Jobs.ie - Dublin"
        agency1.website_url = "https://www.jobs.ie/jobs/dublin?keyword=student"
        
        agency2 = MagicMock()
        agency2.name = "IrishJobs.ie - Dublin"
        agency2.website_url = "https://www.irishjobs.ie/jobs/student/in-dublin"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "Dublin", "IE")
        
        print("\nTesting Context Generation for Dublin (IE):")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN DUBLIN", context)
        self.assertIn("Jobs.ie - Dublin", context)
        # Verify instructions
        self.assertIn("student", context.lower())

if __name__ == '__main__':
    unittest.main()
