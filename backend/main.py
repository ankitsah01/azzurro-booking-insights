from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid
from datetime import datetime

from schemas import (
    PropertySummary, ReviewItem, AIResponseRequest, AIResponseOutput,
    OperationalTicket, ExecutiveBrief, Department, Priority
)
from data import get_properties, get_all_reviews

app = FastAPI(
    title="Azzurro Hotels - Booking.com Review Insights API",
    description="Operational Review Intelligence & AI Automation Suite for Azzurro Hotels",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demo session
REVIEWS_DB = get_all_reviews()
TICKETS_DB: List[OperationalTicket] = [
    OperationalTicket(
        id="tkt-001",
        review_id="rev-104",
        property_id="azzurro-melbourne",
        department=Department.MAINTENANCE,
        priority=Priority.CRITICAL,
        title="AC Failure in Suite 402 - Compressor Inspection",
        description="Guest Sarah O'Connor reported climate control failure during 32°C heatwave. Check-in logs indicate unit humming. Full filter and compressor replacement required.",
        status="In Progress",
        created_at="2026-11-15 19:30"
    ),
    OperationalTicket(
        id="tkt-002",
        review_id="rev-108",
        property_id="azzurro-goldcoast",
        department=Department.HOUSEKEEPING,
        priority=Priority.HIGH,
        title="Chalet 14 Deep Grout Scrub & Mould Remediation",
        description="Guest Jessica Taylor reported black mould in bathroom shower and residual hair on vanity. Immediate deep chemical steam cleaning and supervisor re-inspection required.",
        status="Open",
        created_at="2026-11-17 11:15"
    ),
    OperationalTicket(
        id="tkt-003",
        review_id="rev-106",
        property_id="azzurro-brisbane",
        department=Department.FOOD_AND_BEVERAGE,
        priority=Priority.MEDIUM,
        title="Breakfast Rush Bottleneck - Weekend Morning Shift",
        description="Repeated 40-minute ticket times for hot breakfast items between 8:00 AM - 9:30 AM. Review kitchen expediter workflow and barista allocation.",
        status="Open",
        created_at="2026-11-12 10:45"
    )
]

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "Azzurro Hotels Review Insights API",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/properties", response_model=List[PropertySummary])
def list_properties():
    """Retrieve all 4 Azzurro properties with overall ratings and sentiment breakdown."""
    return get_properties()

@app.get("/api/reviews", response_model=List[ReviewItem])
def list_reviews(
    property_id: Optional[str] = Query(None, description="Filter by property ID (e.g. azzurro-sydney)"),
    min_rating: Optional[float] = Query(None, ge=1.0, le=10.0, description="Minimum Booking.com rating"),
    max_rating: Optional[float] = Query(None, ge=1.0, le=10.0, description="Maximum Booking.com rating"),
    sentiment: Optional[str] = Query(None, description="Filter by positive, neutral, or negative"),
    traveler_type: Optional[str] = Query(None, description="Filter by traveler persona"),
    search: Optional[str] = Query(None, description="Keyword search in title or review text")
):
    results = REVIEWS_DB
    
    if property_id and property_id != "all":
        results = [r for r in results if r["property_id"] == property_id]
        
    if min_rating is not None:
        results = [r for r in results if r["rating"] >= min_rating]
        
    if max_rating is not None:
        results = [r for r in results if r["rating"] <= max_rating]
        
    if sentiment and sentiment != "all":
        results = [r for r in results if r["sentiment"] == sentiment]
        
    if traveler_type and traveler_type != "all":
        results = [r for r in results if r["traveler_type"] == traveler_type]
        
    if search:
        s = search.lower()
        results = [
            r for r in results
            if s in r["title"].lower() 
            or (r.get("positive_comments") and s in r["positive_comments"].lower())
            or (r.get("negative_comments") and s in r["negative_comments"].lower())
            or s in r["guest_name"].lower()
        ]
        
    return results

@app.get("/api/analytics/kpis")
def get_kpis(property_id: Optional[str] = "all"):
    """Calculate aggregated Booking.com operational KPIs."""
    reviews = REVIEWS_DB if property_id == "all" else [r for r in REVIEWS_DB if r["property_id"] == property_id]
    
    if not reviews:
        return {
            "average_rating": 0.0,
            "total_reviews": 0,
            "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
            "response_rate_pct": 0,
            "avg_resolution_hours": 0
        }
        
    avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 2)
    pos_count = sum(1 for r in reviews if r["sentiment"] == "positive")
    neu_count = sum(1 for r in reviews if r["sentiment"] == "neutral")
    neg_count = sum(1 for r in reviews if r["sentiment"] == "negative")
    answered_count = sum(1 for r in reviews if r["response_status"] == "answered")
    
    total = len(reviews)
    return {
        "property_id": property_id,
        "average_rating": avg_rating,
        "total_reviews": total,
        "sentiment_percentages": {
            "positive": round((pos_count / total) * 100, 1),
            "neutral": round((neu_count / total) * 100, 1),
            "negative": round((neg_count / total) * 100, 1)
        },
        "response_rate_pct": round((answered_count / total) * 100, 1),
        "open_tickets_count": len([t for t in TICKETS_DB if t.status != "Resolved" and (property_id == "all" or t.property_id == property_id)]),
        "avg_resolution_hours": 3.4
    }

@app.post("/api/ai/generate-response", response_model=AIResponseOutput)
def generate_ai_response(payload: AIResponseRequest):
    """
    AI Automation Engine: Generates humanized, empathetic, context-aware responses
    mirroring Gemini/OpenAI prompt pipelines.
    """
    review = next((r for r in REVIEWS_DB if r["id"] == payload.review_id), None)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
        
    guest = review["guest_name"]
    prop = review["property_name"]
    rating = review["rating"]
    pos = review.get("positive_comments") or ""
    neg = review.get("negative_comments") or ""
    
    addressed_points = []
    
    if rating >= 8.5:
        if payload.tone == "Warm Hospitality":
            msg = (
                f"Dear {guest},\n\n"
                f"Warm greetings from all of us at {prop}! Thank you for taking the time to share your delightful review on Booking.com.\n\n"
                f"We are overjoyed to know that you had such a wonderful stay with us. "
                f"{f'It brings a huge smile to our team knowing you loved {pos.lower()[:80]}...' if pos else 'Our team strives every day to create memorable luxury experiences.'}\n\n"
                f"It was a true privilege having you as our guest, and we eagerly look forward to welcoming you back to Azzurro soon!\n\n"
                f"Warmest regards,\n"
                f"{payload.manager_name}\n"
                f"{prop}"
            )
        elif payload.tone == "Executive & Formal":
            msg = (
                f"Dear {guest},\n\n"
                f"Thank you for reviewing your recent stay at {prop}.\n\n"
                f"On behalf of hotel management, I am pleased to learn that our services and facilities met your high expectations. "
                f"Your commendable feedback has been shared with our heads of department.\n\n"
                f"We value your patronage and look forward to hosting you on your next visit.\n\n"
                f"Sincerely,\n"
                f"{payload.manager_name}"
            )
        else:
            msg = (
                f"Dear {guest},\n\n"
                f"Thank you for sharing your experience at {prop}. We are thrilled with your high rating and appreciate your kind endorsement.\n\n"
                f"Best regards,\n{payload.manager_name}"
            )
        addressed_points.append("Acknowledged positive highlights and guest patronage")
    else:
        addressed_points.append("Direct acknowledgment of guest grievance")
        addressed_points.append("Concrete operational action and follow-up")
        
        if payload.tone == "De-escalation & Action-Oriented":
            msg = (
                f"Dear {guest},\n\n"
                f"Thank you for providing direct feedback regarding your stay at {prop}. "
                f"Please accept our sincere apologies for falling short of the high standards you rightfully expect from an Azzurro property.\n\n"
                f"I have personally reviewed your comments regarding: \"{neg[:120]}...\". "
                f"I want to assure you that this issue has already been escalated to our Head of Department, and corrective maintenance & quality protocols are underway to guarantee this does not recur.\n\n"
                f"We would welcome the opportunity to regain your trust. Please reach out to me directly at gm@azzurrohotels.com so I can personally oversee your next reservation.\n\n"
                f"Sincerely,\n"
                f"{payload.manager_name}\n"
                f"General Management, {prop}"
            )
        else:
            msg = (
                f"Dear {guest},\n\n"
                f"Thank you for your candid feedback following your recent visit to {prop}.\n\n"
                f"While we are glad you appreciated our convenient location, we deeply regret the discomfort you experienced regarding {neg[:80]}. "
                f"This does not represent the standard of hospitality Azzurro is known for. Our team is actively addressing these concerns.\n\n"
                f"We hope you will grant us another opportunity to provide the seamless experience you deserve.\n\n"
                f"Warm regards,\n"
                f"{payload.manager_name}"
            )
            
    return AIResponseOutput(
        review_id=payload.review_id,
        tone=payload.tone,
        generated_response=msg,
        confidence_score=0.96,
        key_points_addressed=addressed_points
    )

@app.get("/api/operations/tickets", response_model=List[OperationalTicket])
def list_tickets(property_id: Optional[str] = "all"):
    """Retrieve operational tickets generated from negative review triggers."""
    if property_id == "all":
        return TICKETS_DB
    return [t for t in TICKETS_DB if t.property_id == property_id]

@app.post("/api/operations/tickets", response_model=OperationalTicket)
def create_ticket(ticket: OperationalTicket):
    TICKETS_DB.append(ticket)
    return ticket

@app.get("/api/executive-brief", response_model=ExecutiveBrief)
def get_executive_brief():
    """Generates the weekly AI Executive Brief for Hotel General Managers."""
    return ExecutiveBrief(
        week_starting="November 24, 2026",
        overall_health_score=8.75,
        key_strengths=[
            "Sydney property maintains a stellar 9.1/10 rating driven by concierge excellence and harbour views.",
            "South Bank Brisbane boutique saw a 14% boost in positive breakfast mentions following new barista onboarding.",
            "High loyalty among couples and luxury leisure weekenders across all four properties."
        ],
        emerging_risks=[
            "Gold Coast: Grout cleanliness and mould complaints in chalet bathrooms require immediate deep remediation.",
            "Melbourne: Multiple HVAC/air-conditioning complaints during sudden temperature spikes; maintenance contract review recommended.",
            "Check-in waiting times exceeded 20 minutes across 3 properties during Friday afternoon 3 PM peak turnover."
        ],
        department_action_items=[
            {"department": "Housekeeping", "action": "Mandatory supervisor sign-off on chalet bathroom grout and turn-down standards."},
            {"department": "Maintenance", "action": "Emergency HVAC pre-summer servicing across all Melbourne CBD suites."},
            {"department": "Front Desk", "action": "Implement pre-arrival mobile check-in notifications to reduce lobby queue times."}
        ]
    )
