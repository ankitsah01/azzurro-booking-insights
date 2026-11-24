# 🏨 Azzurro Hotels — Booking.com Review Insights & AI Operations Dashboard

An enterprise-grade operational intelligence dashboard and AI automation suite built for **Azzurro Hotels Pty Ltd**. This platform ingests Booking.com guest reviews across four premier Azzurro properties, computes normalized multi-property KPIs, tracks category-level sentiment bottlenecks, and empowers hotel general managers with AI-assisted review replies and automated operational department ticketing.

---

## 🌟 Key Features

### 1. Executive Multi-Property Overview & Benchmarking
- **4 Azzurro Properties Supported:**
  - 🏙️ **Azzurro Harbour Grand Resort & Spa** (Sydney, NSW) — *9.1/10*
  - 🏢 **Azzurro City Centre Suites** (Melbourne, VIC) — *8.6/10*
  - 🌊 **Azzurro Riverfront Boutique Hotel** (Brisbane, QLD) — *8.9/10*
  - 🌴 **Azzurro Oceanfront Palms & Chalets** (Gold Coast, QLD) — *8.4/10*
- **Real-Time KPIs:** Overall Booking.com rating, total reviews analyzed, Net Sentiment Score (Positive / Neutral / Negative), and active operational tickets queue.
- **Category Comparison Matrix:** Interactive benchmark charts comparing Cleanliness, Staff Service, Location, Comfort, Facilities, and Value for Money across all properties.

### 2. Granular Review Explorer & Advanced Filtering
- Search reviews by guest name, room type, or keywords (e.g. "air conditioning", "concierge", "breakfast").
- Multi-dimensional filters: Booking.com score thresholds (9+, 7-9, 5-7, <5), sentiment tags, and traveler personas (*Couples, Business travelers, Families with children, Solo travelers, Friends*).
- Visual status badges for verified Booking.com reviews and management response tracking.

### 3. AI-Powered Hospitality Automation Suite
- **Contextual AI Review Responder:**
  - Ingests guest name, room type, specific compliments, and specific grievances.
  - Three distinct hospitality tone presets:
    - ✨ **Warm Hospitality:** For positive/neutral reviews, reinforcing brand warmth and loyalty.
    - 👔 **Executive & Formal:** High-level corporate luxury tone for corporate accounts and VIP guests.
    - 🛡️ **De-escalation & Action-Oriented:** For critical complaints, acknowledging issues with zero boilerplate and guaranteeing operational remediation.
- **Automated Root-Cause Ticket Escalator:**
  - Automatically parses negative review text and generates prioritized operational tickets (*Critical, High, Medium*) assigned to **Housekeeping**, **Front Desk**, **Maintenance**, or **Food & Beverage**.
  - General Managers can track ticket lifecycle from *Open* to *In Progress* to *Resolved*.

### 4. AI Executive Weekly Brief
- Auto-generated weekly digest for Azzurro hotel leadership.
- Summarizes high-performing department highlights, emerging systemic risks (e.g., HVAC failure patterns during heatwaves, bathroom mould flags), and concrete next actions.

---

## 🛠️ Tech Stack & Tooling Ecosystem

| Category | Tools & Technologies |
| :--- | :--- |
| **Frontend** | React, Tailwind CSS, Lucide Icons, Chart.js, HTML5 / CSS3 |
| **Backend & API** | Python 3, FastAPI, Pydantic v2, Uvicorn, CORS Middleware |
| **AI & Automation** | Contextual Prompt Engineering (Gemini / OpenAI pipelines), Automated Sentiment Extraction, Department Routing Rules |
| **DevOps & Hosting** | Vercel (Frontend / Demo), Render / Railway (Backend), Docker Containerization |
| **Testing & Quality** | Pytest (Backend API tests), Vitest & Playwright (E2E browser automation) |

---

## 🚀 Quick Start Guide

### Option 1: Run Frontend (Zero-Config / Standalone)
The dashboard is completely standalone and can be launched immediately:

```bash
# Using Python's built-in HTTP server:
python3 -m http.server 3000

# Open your browser at:
# http://localhost:3000
```
Or simply double-click `index.html` or `frontend/index.html` in any web browser.

---

### Option 2: Run Full-Stack (FastAPI Backend + Frontend)

#### 1. Start the FastAPI Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
- API Docs (Swagger UI): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

#### 2. Run with Docker:
```bash
cd backend
docker build -t azzurro-api .
docker run -p 8000:8000 azzurro-api
```

---

## 📁 Repository Structure

```
├── index.html                   # Production-ready standalone dashboard (Vercel root)
├── vercel.json                  # Vercel deployment configuration
├── frontend/
│   └── index.html               # Frontend dashboard source
├── backend/
│   ├── main.py                  # FastAPI application & API endpoints
│   ├── schemas.py               # Pydantic data schemas & validation
│   ├── data.py                  # Realistic Booking.com multi-property dataset
│   ├── requirements.txt         # Backend Python dependencies
│   └── Dockerfile               # Backend Docker container specification
├── trial_guide/
│   ├── 01_CAMERA_INTERVIEW_QUESTIONS_AND_ANSWERS.md  # 5 on-camera operations questions & model answers
│   ├── 02_EVERY_25_MINS_PROGRESS_UPDATES.md          # Natural, human dev updates for 25-min check-ins
│   └── 03_FINAL_VOICE_NOTE_SCRIPT.md                 # 90-second voice note walkthrough script
└── README.md                    # Project documentation & architecture overview
```

---

## 🌐 Live Demo & Deployment

- **Vercel Deployment:** Push this repository to GitHub and connect to [Vercel](https://vercel.com). Because `index.html` is in the root directory, Vercel will deploy it instantly with zero configuration and provide an SSL-secured live URL.
- **GitHub Repository:** Initialize git and push:
  ```bash
  git init
  git add .
  git commit -m "feat: complete Booking.com review insights dashboard for Azzurro Hotels"
  git branch -M main
  git remote add origin https://github.com/<your-username>/azzurro-review-insights.git
  git push -u origin main
  ```

---

## 📄 License & Credits
Built for Azzurro Hotels Pty Ltd by **Ankit** for the *Full-Stack Developer — AI Automation & Business Operations* practical trial.
