import unittest
from data import get_properties, get_all_reviews, get_portfolio_weekly, get_topic_analysis, get_reliability_metrics

class TestAzzurroTrialSuite(unittest.TestCase):
    def test_exact_four_properties(self):
        props = get_properties()
        self.assertEqual(len(props), 4)
        prop_ids = [p["id"] for p in props]
        self.assertIn("olympic-paddington", prop_ids)
        self.assertIn("venus-potts-point", prop_ids)
        self.assertIn("central-sydney", prop_ids)
        self.assertIn("darling-harbour", prop_ids)
        
    def test_weekly_comparison_present(self):
        weekly = get_portfolio_weekly()
        self.assertIn("current_week", weekly)
        self.assertIn("previous_week", weekly)
        self.assertIn("score_delta", weekly)
        self.assertGreater(weekly["current_week"]["average_rating"], 0)
        
    def test_topic_analysis_accurate(self):
        topics = get_topic_analysis()
        topic_names = [t["topic"] for t in topics]
        self.assertIn("Cleanliness", topic_names)
        self.assertIn("Noise", topic_names)
        self.assertIn("Check-in Experience", topic_names)
        self.assertIn("Staff Behaviour", topic_names)
        for t in topics:
            self.assertIn("negative_percentage", t)
            self.assertTrue(0 <= t["negative_percentage"] <= 100)
            
    def test_data_reliability_metrics(self):
        rel = get_reliability_metrics()
        self.assertEqual(rel["total_reviews_collected"], 148)
        self.assertEqual(rel["duplicates_detected_and_prevented"], 14)
        self.assertEqual(rel["collection_errors_count"], 0)

if __name__ == "__main__":
    unittest.main()
