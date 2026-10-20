# 🔐 GDPR Request Classifier

A Streamlit-based GDPR request classifier that maps data-subject requests to relevant GDPR articles and suggests practical compliance actions.

## Live App

[Launch the app](https://gdpr-classifier.streamlit.app/)

## Overview

This project helps triage common GDPR-related requests by identifying the request type, mapping it to a relevant GDPR article, assigning a priority level, and suggesting an appropriate next action.

It is a lightweight portfolio project demonstrating practical knowledge of GDPR, privacy-by-design principles, compliance workflows, and Python application development.

> **Important:** This tool is designed for learning, early triage, and portfolio demonstration. It is not legal advice, a replacement for a Data Protection Officer, or a complete GDPR compliance solution.

## Features

- Classifies common GDPR request types using transparent, rule-based logic
- Maps requests to relevant GDPR articles
- Suggests a recommended compliance action
- Assigns a priority level, including critical handling for potential data breaches
- Provides an interactive Streamlit interface
- Keeps a privacy-minimised history that only an admin can view, behind a password (the public app has no history tab or download)
- Includes lightweight application security and privacy controls

## GDPR Topics Covered

| GDPR Article | Topic |
|---|---|
| Article 15 | Right of Access / Subject Access Requests |
| Article 16 | Right to Rectification |
| Article 17 | Right to Erasure |
| Article 18 | Right to Restriction of Processing |
| Article 20 | Right to Data Portability |
| Article 21 | Right to Object / Withdraw Consent |
| Article 22 | Automated Individual Decision-Making and Profiling |
| Articles 13 & 14 | Right to be Informed / Privacy Notice Enquiries |
| Article 33 | Personal Data Breach Notification |
| Article 77 | Right to Lodge a Complaint |

## 🔒 Security and Privacy Controls

This project includes lightweight controls intended to demonstrate secure and privacy-aware application design.

- **Input validation and sanitisation**  
  - Enforces minimum and maximum input lengths  
  - Rejects basic malicious or unsafe patterns, such as script tags and dangerous shell commands  
  - Returns clear validation errors rather than processing invalid input  

- **Audit logging without raw request content**  
  - Classification events are written to `logs/gdpr_classification_audit.log`  
  - Logs contain the classification outcome, priority, timestamp, and a SHA-256 input hash  
  - Full user request text is not written to the audit log  

- **Data minimisation in SQLite history**  
  - The local database does not retain any of the submitted request text, not even a preview  
  - It stores a salted HMAC-SHA-256 hash, the request length, the result and a timestamp  
  - The history and its CSV download are visible only after entering an admin password (`ADMIN_PASSWORD`); if none is configured, the tab is not shown at all  

- **Rate limiting**  
  - Each browser session is limited to five classification requests per minute  
  - A second limit of 30 requests per minute is shared by all visitors of the running app, so opening a new tab does not give a fresh allowance  
  - Neither limit is per IP address or account, so this is basic protection against accidental misuse and casual flooding, not a determined attacker  

- **Error handling**  
  - Users see a generic message if classification fails; the detail goes to the server log only  

- **Secrets handling pattern**  
  - `python-dotenv` supports local environment-variable loading  
  - `.env.example` shows the optional settings: `ADMIN_PASSWORD` and `HASH_SALT`  
  - `.env`, local databases, logs, and Python cache files are excluded from Git through `.gitignore`  

These controls are intentionally lightweight and are not a substitute for production-grade access control, encryption, monitoring, retention policies, or a formal Data Protection Impact Assessment.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Data handling | Pandas |
| Local storage | SQLite |
| Classification | Rule-based keyword matching |
| Security helpers | Custom `security.py` (validation, salted hashing) and `ratelimit.py` |
| Secrets support | `python-dotenv` |

## Project Structure

```text
gdpr-classifier/
├── streamlit_app.py      # Streamlit interface, local history, rate limiting
├── classifier.py         # GDPR request classification logic and audit logging
├── security.py           # Input validation, sanitisation, salted hashing
├── ratelimit.py          # Shared (all-visitor) rate limiter
├── tests/                # Classifier, hashing and rate limit tests
├── secrets_helper.py     # Environment-variable helper for future secrets
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment-variable configuration
├── .gitignore            # Prevents secrets, databases, logs, and cache files entering Git
├── logs/                 # Runtime audit logs; ignored by Git
└── README.md
```

## How It Works

1. A user enters a GDPR-related request into the Streamlit interface.
2. The app checks that the input is present and that the request rate limit has not been exceeded.
3. The request is validated and sanitised before classification.
4. The rule-based classifier matches relevant GDPR request patterns.
5. The classifier returns:
   - Request type
   - Relevant GDPR article
   - Recommended compliance action
   - Priority level
6. The result is displayed in the app.
7. A privacy-minimised record is stored locally: a salted hash and the request length, never the request text.

## Tests

```bash
pip install pytest
pytest -q
```

## Run Locally

### Clone the repository

```bash
git clone https://github.com/ShivamKumar20-AI/gdpr-classifier.git
cd gdpr-classifier
```

### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the application

```bash
streamlit run streamlit_app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Deployment

The app is deployed on Streamlit Community Cloud:

[https://gdpr-classifier.streamlit.app/](https://gdpr-classifier.streamlit.app/)

## Limitations

- The classifier is rule-based and keyword-driven; it does not understand full legal context, intent, or complex wording.
- The tool may not classify every request correctly and should not be used as the sole basis for compliance decisions.
- It does not verify the identity of the requester before recommending action.
- Streamlit Community Cloud storage is temporary and may reset after an app restart or redeployment.
- The rate limits are per browser session and per running app, not per IP address or account.
- The admin history view uses a single shared password, not user accounts or role-based access control.
- The application does not yet include encrypted persistent storage or automated retention/deletion rules.
- Matching is by phrases and patterns, so unusual wording can still be misclassified. A person should confirm every result.

## Possible Improvements

- Replace rule-based logic with an NLP or machine-learning classifier
- Add confidence scoring and human-review escalation thresholds
- Implement user authentication and role-based access control
- Use a persistent encrypted cloud database with retention controls
- Add user identity verification before handling data-subject request workflows
- Add DPIA-style risk assessment records and decision audit workflows
- Build a secure admin dashboard for authorised compliance teams
- Expand coverage for more nuanced GDPR and UK GDPR scenarios

## Author

**Shivam Kumar**  
AI Governance Analyst and AI Engineer  

- GitHub: [ShivamKumar20-AI](https://github.com/ShivamKumar20-AI)  
- LinkedIn: [shivam-kumar-554395239](https://linkedin.com/in/shivam-kumar-554395239)
