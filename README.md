# GDPR Request Classifier

A live AI-powered API that classifies data subject requests and maps them to the relevant GDPR article — built with FastAPI and deployed on Railway.

🌐 **Live URL:** https://gdpr-classifier-production.up.railway.app

---

## What It Does

Paste any request from a customer or data subject and the classifier will:
- Identify the **request type** (e.g. Right to Erasure, Subject Access Request)
- Map it to the **GDPR article**
- Recommend an **action** to take
- Assign a **priority** (Critical / High / Medium / Low)

---

## GDPR Articles Covered (10/10 ✅)

| Article | Right | Priority |
|---|---|---|
| Article 15 | Right of Access (SAR) | High |
| Article 16 | Right to Rectification | Medium |
| Article 17 | Right to Erasure (Right to be Forgotten) | High |
| Article 18 | Right to Restriction of Processing | High |
| Article 20 | Right to Data Portability | Medium |
| Article 21 | Right to Object / Withdraw Consent | High |
| Article 22 | Automated Decision Making / Profiling | High |
| Article 13 & 14 | Right to be Informed (Privacy Notice) | Low |
| Article 33 | Data Breach Notification | Critical |
| Article 77 | Right to Lodge a Complaint | High |

---

## API Endpoints

### `POST /classify`
Classify a data subject request.

**Request:**
```json
{
  "text": "I want to delete all my data"
}
```

**Response:**
```json
{
  "request_type": "Right to Erasure",
  "gdpr_article": "Article 17 — Right to be Forgotten",
  "action": "Erase all personal data unless a lawful retention basis applies.",
  "priority": "High"
}
```

### `GET /health`
Returns `{"status": "healthy"}` — use for uptime monitoring.

### `GET /history`
Returns the last 20 classifications logged to the database.

### `GET /docs`
Interactive Swagger UI — try the API in your browser.

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/ShivamKumar20-AI/gdpr-classifier.git
cd gdpr-classifier

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Then open: http://localhost:8000

---

## Run Tests

```bash
python test.py
```

---

## Project Structure

```
gdpr-classifier/
├── main.py           # FastAPI app, routes, SQLite logging
├── classifier.py     # GDPR classification logic (10 articles)
├── test.py           # Automated tests
├── requirements.txt  # Python dependencies
├── Procfile          # Railway start command
├── nixpacks.toml     # Railway build config
└── static/
    └── index.html    # Browser UI
```

---

## Tech Stack

- **FastAPI** — API framework
- **Uvicorn** — ASGI server
- **SQLite** — request logging
- **Railway** — cloud deployment (auto-deploys on push to `main`)
