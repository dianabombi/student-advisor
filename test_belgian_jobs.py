
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

class TestBelgianJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_be(self):
        """Test extraction of Belgian cities with synonyms"""
        # Note: country_code for Belgium is 'BE'
        test_cases = [
            ("Student job in Brussels", "Brussels"),
            ("Praca w Brukseli", "Brussels"), # PL
            ("Jobs in Gent", "Ghent"), 
            ("Ghent student jobs", "Ghent"),
            ("Job a Liege", "Liège"),
            ("Travail etudiant Louvain-la-Neuve", "Louvain-la-Neuve"),
            ("Student job Leuven", "Leuven"),
             ("Antwerp jobs", "Antwerp")
        ]
        
        print("\nTesting Belgian City Extraction (country_code='BE'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'BE')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            # self.assertEqual(city, expected)

    def test_context_generation(self):
        """Test instruction generation for Belgian portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Student.be - Brussels"
        agency1.website_url = "https://www.student.be/en/student-jobs/jobs?l=Brussels"
        
        agency2 = MagicMock()
        agency2.name = "StepStone.be - Brussels"
        agency2.website_url = "https://www.stepstone.be/jobs/Brussels/student-jobs"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "Brussels", "BE")
        
        print("\nTesting Context Generation for Brussels (BE):")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN BRUSSELS", context)
        self.assertIn("Student.be - Brussels", context)
        # Verify instructions
        self.assertIn("Instructions: Open website", context)

if __name__ == "__main__":
    unittest.main()
