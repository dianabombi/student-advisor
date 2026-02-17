
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

class TestSwissJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_ch(self):
        """Test extraction of Swiss cities with synonyms (multilingual)"""
        test_cases = [
            ("Ich suche Arbeit in Zürich", "Zurich"),
            ("Lavoro a Zurigo", "Zurich"),
            ("Poste à Genève", "Geneva"),
            ("Arbeit in Genf", "Geneva"),
            ("Job in Bern", "Bern"),
            ("Travail à Bâle", "Basel"),
            ("Job in Basel", "Basel"),
            ("Jobs in St. Gallen", "St. Gallen"),
            ("Sankt Gallen work", "St. Gallen"),
            ("Lozanna praca", "Lausanne")
        ]
        
        print("\nTesting Swiss City Extraction (country_code='CH'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'CH')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            self.assertEqual(city, expected)

    def test_context_generation(self):
        """Test partial instruction generation for Swiss portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Jobs.ch - Zurich"
        agency1.website_url = "https://www.jobs.ch/en/vacancies/?location=Zurich"
        
        agency2 = MagicMock()
        agency2.name = "Indeed.ch - Zurich"
        agency2.website_url = "https://ch.indeed.com/jobs?q=Student&l=Zurich"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "Zurich", "CH")
        
        print("\nTesting Context Generation for Zurich:")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN ZURICH", context)
        self.assertIn("Jobs.ch - Zurich", context)
        # Verify instructions
        self.assertIn("keyword 'Student'", context)

if __name__ == '__main__':
    unittest.main()
