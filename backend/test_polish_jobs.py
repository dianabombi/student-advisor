
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

class TestPolishJobs(unittest.TestCase):
    def setUp(self):
        self.service = JobsChatService()
        self.db = MockDB()

    def test_city_extraction_pl(self):
        """Test extraction of Polish cities with fuzzy matching"""
        test_cases = [
            ("Szukam pracy w Warszawie", "Warszawa"),
            ("Chcę pracować w Krakowie", "Kraków"),
            ("Warsaw job", "Warszawa"),
            ("Szukam oferty w Poznaniu", "Poznań"),
            ("Job in Gdansk", "Gdańsk"),
            ("Praca w Wroclawiu", "Wrocław"),
            ("Praca Wrocław", "Wrocław"),
            ("Szukam pracy w Gdansku", "Gdańsk")  # No accent
        ]
        
        print("\nTesting Polish City Extraction (country_code='PL'):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'PL')
            print(f"  '{message}' -> {city} (Expected: {expected})")
            self.assertEqual(city, expected)
            
    def test_city_extraction_cross_lingual(self):
        """Test extraction of Polish cities in other languages"""
        # Testing "Warsaw" in Ukrainian, English, etc.
        test_cases = [
            ("Шукаю роботу у Варшаві", "Warszawa"),
            ("Looking for job in Warsaw", "Warszawa"),
            ("Busco trabajo en Varsovia", "Warszawa"),
            ("Ich suche Arbeit in Warschau", "Warszawa")
        ]
        
        print("\nTesting multilingual variants for Warszawa (PL):")
        for message, expected in test_cases:
            city = self.service._extract_city_from_message(message, 'PL')
            print(f"  '{message}' -> {city}")
            self.assertEqual(city, expected)


    def test_context_generation(self):
        """Test partial instruction generation for Polish portals"""
        # Mock JobAgency objects
        agency1 = MagicMock()
        agency1.name = "Pracuj.pl - Warszawa"
        agency1.website_url = "https://www.pracuj.pl/praca/warszawa;wp"
        
        agency2 = MagicMock()
        agency2.name = "OLX.pl - Warszawa"
        agency2.website_url = "https://www.olx.pl/d/praca/warszawa/"

        # Mock DB query result
        self.db.query_mock.filter.return_value.all.return_value = [agency1, agency2]
        
        context = self.service._get_agencies_context(self.db, "Warszawa", "PL")
        
        print("\nTesting Context Generation for Warszawa:")
        print(context)
        
        self.assertIn("VERIFIED JOB AGENCIES IN WARSZAWA", context)
        self.assertIn("Pracuj.pl - Warszawa", context)
        self.assertIn("OLX.pl - Warszawa", context)
        # Verify instructions
        self.assertIn("filter by 'Praca dorywcza'", context)
        self.assertIn("select 'Praca', then 'Praca dorywcza'", context)

if __name__ == '__main__':
    unittest.main()

