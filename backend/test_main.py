import unittest
from data import get_properties, get_all_reviews

class TestAzzurroData(unittest.TestCase):
    def test_properties_count(self):
        props = get_properties()
        self.assertEqual(len(props), 4, "Should have exactly 4 Azzurro properties")
        
    def test_property_scores(self):
        props = get_properties()
        for p in props:
            self.assertTrue(1.0 <= p["average_rating"] <= 10.0)
            self.assertIn("Cleanliness", p["category_scores"])
            self.assertIn("Staff", p["category_scores"])
            
    def test_reviews_data(self):
        reviews = get_all_reviews()
        self.assertGreaterEqual(len(reviews), 10)
        for r in reviews:
            self.assertIn(r["property_id"], ["azzurro-sydney", "azzurro-melbourne", "azzurro-brisbane", "azzurro-goldcoast"])
            self.assertIn(r["sentiment"], ["positive", "neutral", "negative"])

if __name__ == "__main__":
    unittest.main()
