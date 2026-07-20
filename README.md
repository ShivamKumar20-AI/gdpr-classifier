# GDPR Request Classifier

A Streamlit-based GDPR request classifier that maps data subject requests to relevant GDPR articles and recommended compliance actions.

## Live App

[Launch the app](https://gdpr-classifier.streamlit.app/)

## Overview

This project helps triage common GDPR-related requests by classifying the request, linking it to the relevant GDPR article, and suggesting an appropriate compliance action.

It is designed as a lightweight portfolio project to demonstrate practical knowledge of GDPR, compliance workflows, and Python-based application development.

## Features

- Classifies common GDPR request types using rule-based logic
- Maps requests to relevant GDPR articles
- Suggests a recommended compliance action
- Assigns a priority level
- Stores recent classifications in SQLite
- Allows users to download recent history as CSV
- Includes a simple Streamlit interface for testing and demonstration

## GDPR topics covered

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

## How it works

1. A user enters a GDPR-related request into the Streamlit interface.
2. The app passes the text to a rule-based classifier in `classifier.py`.
3. The classifier returns:
   - request type,
   - GDPR article,
   - recommended action,
   - priority level.
4. The result is displayed in the app and optionally logged to a local SQLite database.

## Run locally

```bash
git clone https://github.com/ShivamKumar20-AI/gdpr-classifier.git
cd gdpr-classifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deployment

This app is deployed on Streamlit Community Cloud:

[https://gdpr-classifier.streamlit.app/](https://gdpr-classifier.streamlit.app/)

## Notes

- The classifier is rule-based and keyword-driven.
- SQLite storage on Streamlit Community Cloud is temporary and may reset after app restarts.
- This project is intended for learning, prototyping, and portfolio demonstration rather than production use.

## Possible improvements

- Replace rule-based logic with an NLP or ML-based classifier
- Add confidence scoring
- Store history in a persistent cloud database
- Add audit logging and role-based access controls
- Expand coverage for more nuanced GDPR scenarios

## Author

Shivam Kumar

- GitHub: [https://github.com/ShivamKumar20-AI](https://github.com/ShivamKumar20-AI)
- LinkedIn: [https://linkedin.com/in/shivam-kumar-554395239](https://linkedin.com/in/shivam-kumar-554395239)
