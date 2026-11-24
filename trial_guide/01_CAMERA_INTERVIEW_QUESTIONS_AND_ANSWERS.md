# 🎙️ Azzurro Hotels Trial: On-Camera Operations Questions & Model Answers

**Role:** Full-Stack Developer — AI Automation & Business Operations  
**Format:** 5 short questions on camera & microphone before starting the build.

---

### Question 1: How do you systematically identify operational bottlenecks from guest reviews across multiple hotel properties?

> **Key Theme:** Data aggregation, root-cause tagging, and noise filtering.

**Model Answer (Speak naturally, ~45-60 seconds):**
> *"In hospitality operations, guest reviews fall into two categories: random anomalies and systemic failures. To identify real bottlenecks across multiple properties, I look at cluster frequency, category sentiment, and velocity. 
> 
> Technically, we aggregate reviews into normalized categories—Housekeeping, Front Desk, F&B, Facilities, and WiFi. Then, we calculate the negative sentiment velocity per category over rolling 14-day and 30-day windows. If a single property has three reviews in a week mentioning 'slow check-in at 3 PM', that's not a one-off; it points to shift handover or room readiness issues. By visualizing these clusters alongside Department Impact Scores, general managers can address the root cause immediately rather than reacting blindly."*

---

### Question 2: How would you automate review responses without losing the warm, personalized hospitality touch?

> **Key Theme:** Human-in-the-loop, dynamic prompt context, and brand voice guardrails.

**Model Answer (~45-60 seconds):**
> *"Pure automated generic boilerplate like 'Thank you for your feedback, we hope to see you again' actually damages a luxury brand like Azzurro Hotels. My approach is 'AI-assisted, human-in-the-loop automation.'
>
> We use LLMs with structured context injection: the guest's name, room type, specific compliments (like the rooftop pool), and specific complaints (like noisy street traffic). The system drafts a tailored response in Azzurro's brand voice—empathetic and action-oriented—and automatically flags whether it can be auto-approved (for 9-10/10 reviews) or requires general manager sign-off (anything below 7/10 or mentioning safety/cleanliness). This cuts response time from days to minutes while keeping genuine human warmth."*

---

### Question 3: If a guest posts a critical 1-star review regarding room cleanliness, what automated operational pipeline should trigger?

> **Key Theme:** Real-time event triggers, PMS/ticketing webhooks, and closed-loop escalation.

**Model Answer (~45-60 seconds):**
> *"A 1-star cleanliness review is an operational emergency that affects reputation and future bookings. The automated pipeline triggers in three immediate stages:
>
> 1. **Instant Ingestion & Tagging:** The webhook receives the review, classifies sentiment as critical, and extracts the room number or stay dates.
> 2. **Automated Ticket Creation:** It instantly pushes a high-priority ticket via webhook or API to the property's PMS or operations channel (like Slack, WhatsApp, or hotel maintenance software), assigning it directly to the Head of Housekeeping and the General Manager on duty.
> 3. **Closed-Loop Resolution:** It drafts an empathetic response acknowledging the exact issue, logs the room history to inspect past turnover logs, and alerts the guest relations manager to reach out directly with guest recovery steps."*

---

### Question 4: How do you handle integrating data from OTAs like Booking.com with internal hotel databases?

> **Key Theme:** Webhooks, scraping/API limits, schema normalization, and idempotency.

**Model Answer (~45-60 seconds):**
> *"OTAs like Booking.com provide structured partner APIs or automated email/webhook ingestion. When building a unified dashboard, the biggest challenge is data disparity across OTAs (Booking.com uses a 10-point scale, Google uses 5-star, TripAdvisor uses bubble ratings).
>
> I build a normalization ingestion pipeline (using FastAPI/Python or Node.js) that maps incoming reviews into a single canonical schema: `property_id`, `guest_type`, `review_date`, `normalized_score (0-100)`, `category_ratings`, and `sentiment_tokens`. We ensure idempotency using the OTA review UUID so duplicates are never inserted, and store raw payloads in PostgreSQL/Supabase for auditability."*

---

### Question 5: How do you measure the ROI and operational impact of an AI automation dashboard for hotel leadership?

> **Key Theme:** Business outcomes, response velocity, review score lift, and operational labor saved.

**Model Answer (~45-60 seconds):**
> *"For hotel leadership, ROI boils down to two things: labor efficiency and direct revenue lift.
>
> 1. **Time Saved:** We measure the reduction in staff hours spent manually reading, categorizing, and drafting replies across 4 properties. Typically, automated classification and drafting saves 15-20 hours per week per property.
> 2. **Review Score Lift:** Fast, proactive resolution of guest issues directly raises average Booking.com review scores over 3-6 months. In hospitality, an increase of just 0.5 points on Booking.com historically correlates with a 5% to 9% increase in Average Daily Rate (ADR) and higher booking conversion. We measure this through a rolling correlation between issue resolution time and score trends."*
