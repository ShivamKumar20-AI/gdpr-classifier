# GDPR Request Classifier

A Streamlit-based GDPR request classifier that maps data subject requests to relevant GDPR articles and suggests a compliance action.

## What it does

This tool helps triage common GDPR-related requests by:

- Identifying the request type
- Mapping it to the relevant GDPR article
- Recommending an action
- Assigning a priority level

## GDPR articles covered

- Article 15 — Right of Access
- Article 16 — Right to Rectification
- Article 17 — Right to Erasure
- Article 18 — Right to Restriction of Processing
- Article 20 — Right to Data Portability
- Article 21 — Right to Object
- Article 22 — Automated Decision-Making
- Article 13 & 14 — Right to be Informed
- Article 33 — Personal Data Breach Notification
- Article 77 — Right to Lodge a Complaint

## Tech stack

- Python
- Streamlit
- Pandas
- SQLite

## Project structure

```text
gdpr-classifier/
├── streamlit_app.py
├── classifier.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally

```bash
git clone https://github.com/ShivamKumar20-AI/gdpr-classifier.git
cd gdpr-classifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Notes

- The classifier is rule-based and keyword-driven.
- SQLite history on Streamlit Community Cloud is temporary and may reset after app restarts.
- This project is intended for learning, prototyping, and portfolio demonstration.

## Author

Shivam Kumar

- GitHub: https://github.com/ShivamKumar20-AI
- LinkedIn: https://linkedin.com/in/shivam-kumar-554395239