# GDPR Request Classifier

A live AI-powered API that classifies data subject requests and maps them to the relevant GDPR article — built with FastAPI and deployed on Railway.

🌐 **Live URL:** https://gdpr-classifier-production.up.railway.app

---

## What It Does

DPOs and compliance teams receive hundreds of data subject requests. This tool automates triage — paste any incoming message and the classifier instantly identifies the request type, maps it to the correct GDPR article, recommends a compliance action, and assigns a priority level.

- Identifies the **request type** (e.g. Right to Erasure, Subject Access Request)
- Maps it to the **GDPR article**
- Recommends a **compliance action** to take
- Assigns a **priority** (Critical / High / Medium / Low)

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

## Real Test Results

| Input message | Classification | GDPR Article | Priority |
|---|---|---|---|
| "Please delete all my data and forget me" | Right to Erasure | Article 17 | High |
| "I want to export my data in a portable format" | Data Portability Request | Article 20 | Medium |
| "I would like to know what personal data your company holds about me" | Data Portability Request | Article 20 | Medium |
| "I received an email saying my password was changed but I did not do this" | General Enquiry | No article triggered | Low |
| "I think someone has accessed my account without my permission" | General Enquiry | No article triggered | Low |
| "What are your opening hours and how do I contact customer support" | General Enquiry | No article triggered | Low |
| "How do I update the email address on my account" | Data Breach Report | Article 33 | Critical |
| "I want to know how much data you have on me" | General Enquiry | No article triggered | Low |

> Note: Some misclassifications (e.g. account update queries triggering Article 33) reflect the limitations of keyword-based classification on ambiguous inputs. This is a known trade-off in rule-based NLP triage tools.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Language | Python 3.11+ |
| Classification | Keyword-based rule engine mapping to GDPR articles |
| Logging | SQLite |
| UI | Browser-based HTML interface |
| Deployment | Railway |

---

## Project Structure

```
gdpr-classifier/
├── main.py            # FastAPI app and /classify endpoint
├── classifier.py      # GDPR classification rules and logic
├── static/            # Browser UI files
├── requirements.txt   # Python dependencies
├── Procfile           # Railway deployment config
└── README.md
```

---

## API Usage

### Endpoint

```
POST /classify
```

### Request

```bash
curl -X POST "https://gdpr-classifier-production.up.railway.app/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "I want to delete all my personal data immediately."}'
```

### Example Response

```json
{
  "request_type": "Right to Erasure",
  "gdpr_article": "Article 17 — Right to be Forgotten",
  "action": "Erase all personal data unless a lawful retention basis applies.",
  "priority": "High"
}
```

---

## Getting Started Locally

```bash
git clone https://github.com/ShivamKumar20-AI/gdpr-classifier.git
cd gdpr-classifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

---

## Limitations

- Rule-based and keyword-driven — does not understand full legal context or nuanced language.
- Not a substitute for legal advice or formal GDPR impact assessment.
- Intended for learning, portfolio demonstration, and early-stage triage, not production compliance decisions.

---

## Author

**Shivam Kumar** — AI Governance Analyst & ML Engineer

[GitHub Profile](https://github.com/ShivamKumar20-AI) | [LinkedIn](https://linkedin.com/in/shivam-kumar-554395239)
