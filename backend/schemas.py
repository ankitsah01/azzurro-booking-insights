from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date, datetime
from enum import Enum

class TravelerType(str, Enum):
    COUPLE = "Couple"
    FAMILY = "Family with children"
    BUSINESS = "Business traveler"
    SOLO = "Solo traveler"
    GROUP = "Group of friends"

class SentimentCategory(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class Department(str, Enum):
    HOUSEKEEPING = "Housekeeping"
    FRONT_DESK = "Front Desk"
    MAINTENANCE = "Maintenance"
    FOOD_AND_BEVERAGE = "Food & Beverage"
    MANAGEMENT = "General Management"

class Priority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class PropertySummary(BaseModel):
    id: str
    name: str
    location: str
    total_reviews: int
    average_rating: float
    sentiment_breakdown: Dict[str, float]
    category_scores: Dict[str, float]
    image_url: str

class ReviewItem(BaseModel):
    id: str
    property_id: str
    property_name: str
    guest_name: str
    guest_country: str
    traveler_type: TravelerType
    room_type: str
    stay_date: str
    review_date: str
    rating: float = Field(..., ge=1.0, le=10.0, description="Booking.com score from 1.0 to 10.0")
    title: str
    positive_comments: Optional[str] = None
    negative_comments: Optional[str] = None
    sentiment: SentimentCategory
    flagged_departments: List[Department] = []
    response_status: str = "pending" # pending | answered
    manager_response: Optional[str] = None

class AIResponseRequest(BaseModel):
    review_id: str
    tone: str = "Warm Hospitality" # "Warm Hospitality", "Executive & Formal", "De-escalation & Action-Oriented"
    manager_name: str = "Azzurro Guest Relations Team"

class AIResponseOutput(BaseModel):
    review_id: str
    tone: str
    generated_response: str
    confidence_score: float
    key_points_addressed: List[str]

class OperationalTicket(BaseModel):
    id: str
    review_id: str
    property_id: str
    department: Department
    priority: Priority
    title: str
    description: str
    status: str = "Open" # Open, In Progress, Resolved
    created_at: str

class ExecutiveBrief(BaseModel):
    week_starting: str
    overall_health_score: float
    key_strengths: List[str]
    emerging_risks: List[str]
    department_action_items: List[Dict[str, str]]
