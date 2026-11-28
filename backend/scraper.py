"""
Azzurro Hotels — Booking.com Review Collection & Ingestion Engine
Target Properties:
1. Olympic Hotel Paddington: https://www.booking.com/hotel/au/olympic-paddington.html
2. Potts Point: https://www.booking.com/hotel/au/venus-potts-point-sydney.html
3. Central Sydney: https://www.booking.com/hotel/au/venus-surry-hills.html
4. Darling Harbour: https://www.booking.com/hotel/au/chateau-de-venus.html
"""

import hashlib
import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AzzurroScraper")

PROPERTIES_TARGETS = [
    {
        "id": "olympic-paddington",
        "name": "Olympic Hotel Paddington",
        "url": "https://www.booking.com/hotel/au/olympic-paddington.html",
        "suburb": "Paddington, Sydney",
        "rating_target": 7.8,
    },
    {
        "id": "venus-potts-point",
        "name": "Potts Point",
        "url": "https://www.booking.com/hotel/au/venus-potts-point-sydney.html",
        "suburb": "Potts Point, Sydney",
        "rating_target": 7.2,
    },
    {
        "id": "central-sydney",
        "name": "Central Sydney",
        "url": "https://www.booking.com/hotel/au/venus-surry-hills.html",
        "suburb": "Surry Hills, Sydney",
        "rating_target": 7.5,
    },
    {
        "id": "darling-harbour",
        "name": "Darling Harbour",
        "url": "https://www.booking.com/hotel/au/chateau-de-venus.html",
        "suburb": "Darling Harbour, Sydney",
        "rating_target": 7.9,
    },
]

TOPIC_KEYWORDS = {
    "Cleanliness": ["clean", "dirty", "dust", "mould", "mold", "hair", "smell", "stain", "towel", "linen", "cockroach", "bedbug", "messy"],
    "Noise": ["noise", "noisy", "loud", "traffic", "street", "siren", "bar", "pub", "music", "thin walls", "banging", "earplugs"],
    "Staff Behaviour": ["staff", "receptionist", "rude", "friendly", "helpful", "unfriendly", "host", "greeting", "attitude", "service"],
    "Check-in Experience": ["check-in", "queue", "wait", "waiting", "early check-in", "late check-in", "key", "code", "lockbox", "front desk"],
    "Facilities": ["wifi", "wi-fi", "internet", "elevator", "lift", "shower", "hot water", "parking", "kitchen", "bathroom", "toilet"],
    "Room Condition": ["bed", "mattress", "ac", "aircon", "air conditioning", "heater", "window", "small", "cramped", "dated", "broken", "light"],
    "Location": ["location", "station", "train", "bus", "walk", "central", "convenient", "suburb", "restaurant", "shops", "safe"],
    "Value for Money": ["price", "expensive", "cheap", "overpriced", "worth", "value", "cost", "affordable"],
}


class ReviewCollector:
    def __init__(self, storage_path: str = "collected_reviews.json"):
        self.storage_path = storage_path
        self.seen_hashes = set()
        self.stats = {
            "total_collected": 0,
            "duplicates_detected": 0,
            "errors_count": 0,
            "last_run": None,
            "status": "Healthy",
        }
        self.load_existing()

    def generate_hash(self, property_id: str, author: str, date_str: str, text: str) -> str:
        """Deduplication key: SHA256 of property + author + date + normalized text."""
        norm_text = re.sub(r"\s+", " ", text.lower().strip())
        raw = f"{property_id}|{author.strip().lower()}|{date_str}|{norm_text}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def load_existing(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data.get("reviews", []):
                        h = item.get("hash") or self.generate_hash(
                            item["property_id"], item["guest_name"], item["review_date"], item["title"] + (item.get("positive_comments") or "")
                        )
                        self.seen_hashes.add(h)
                logger.info(f"Loaded {len(self.seen_hashes)} existing unique review hashes.")
            except Exception as e:
                logger.error(f"Error loading existing storage: {e}")

    def classify_topics(self, text: str) -> List[str]:
        """Classify review text into operational topics based on keyword matching."""
        t_lower = text.lower()
        matched = []
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(k in t_lower for k in keywords):
                matched.append(topic)
        return matched

    def determine_sentiment(self, score: float, neg_text: Optional[str]) -> str:
        if score >= 8.0:
            return "positive"
        elif score >= 6.0:
            return "neutral"
        return "negative"


# Singleton instance for backend ingestion
collector = ReviewCollector(storage_path=os.path.join(os.path.dirname(__file__), "collected_reviews.json"))
