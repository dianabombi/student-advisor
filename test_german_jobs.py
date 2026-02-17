
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

class TestGermanJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_de(self):
        """Test extraction of German cities with synonyms"""
        test_cases = [
            ("Ich suche Arbeit in München", "München"),
            ("Job in Munich", "München"),
            ("Praca w Monachium", "München"),
            ("Lavoro a Monaco", "München"),
            ("Jobs in Cologne", "Köln"),
            ("Job Köln", "Köln"),
            ("Arbeit in Berlin", "Berlin"),
            ("Job in Nuremberg", "Nürnberg"),
            ("Praca w Norymberdze", "Nürnberg"),
            ("Aix-la-Chapelle jobs", "Aachen")
        ]
        
        print("\nTesting German City Extraction (country_code='DE'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'DE')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            self.assertEqual(city, expected)

    def test_context_generation(self):
        """Test partial instruction generation for German portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Zenjob - München"
        agency1.website_url = "https://www.zenjob.com/de/jobs/muenchen/"
        
        agency2 = MagicMock()
        agency2.name = "StepStone - München"
        agency2.website_url = "https://www.stepstone.de/jobs/München?q=Werkstudent"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "München", "DE")
        
        print("\nTesting Context Generation for München:")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN MÜNCHEN", context)
        self.assertIn("Zenjob - München", context)
        # Verify instructions
        self.assertIn("BEST FOR STUDENTS", context)
        self.assertIn("search for 'Werkstudent'", context)

if __name__ == '__main__':
    unittest.main()
