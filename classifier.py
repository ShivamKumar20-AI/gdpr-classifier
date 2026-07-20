from typing import Dict


def classify(text: str) -> Dict:
    t = text.lower()

    # Article 15 — Subject Access Request
    if any(k in t for k in ["subject access request", "sar", "access to my data",
                              "what data do you hold", "copy of my data",
                              "what information do you have on me"]):
        return {
            "request_type": "Subject Access Request (SAR)",
            "gdpr_article": "Article 15 — Right of Access",
            "action": "Respond within 30 days with a copy of all personal data held.",
            "priority": "High"
        }

    # Article 17 — Right to Erasure
    if any(k in t for k in ["delete my data", "delete all my data", "i want to delete",
                              "right to erasure", "remove my information",
                              "forget me", "erase my data", "right to be forgotten",
                              "wipe my data", "remove all my details"]):
        return {
            "request_type": "Right to Erasure",
            "gdpr_article": "Article 17 — Right to be Forgotten",
            "action": "Erase all personal data unless a lawful retention basis applies.",
            "priority": "High"
        }

    # Article 33 — Data Breach
    if any(k in t for k in ["data breach", "unauthorised access", "leaked", "hacked",
                              "personal data exposed", "security incident",
                              "compromised", "cyber attack", "data leak"]):
        return {
            "request_type": "Data Breach Report",
            "gdpr_article": "Article 33 — Notification of Personal Data Breach",
            "action": "Notify the ICO within 72 hours if risk to individuals is likely.",
            "priority": "Critical"
        }

    # Article 21 — Right to Object
    if any(k in t for k in ["stop processing", "opt out", "object to processing",
                              "withdraw consent", "no longer consent",
                              "revoke consent", "unsubscribe from processing"]):
        return {
            "request_type": "Right to Object / Withdraw Consent",
            "gdpr_article": "Article 21 — Right to Object",
            "action": "Stop processing personal data unless compelling legitimate grounds exist.",
            "priority": "High"
        }

    # Article 16 — Right to Rectification
    if any(k in t for k in ["update my data", "correct my information", "wrong details",
                              "inaccurate data", "change my address", "update my name",
                              "fix my details", "incorrect information", "is incorrect",
                              "my address is", "my name is wrong", "wrong address",
                              "wrong name", "update my address", "please correct",
                              "needs to be updated", "out of date"]):
        return {
            "request_type": "Right to Rectification",
            "gdpr_article": "Article 16 — Right to Rectification",
            "action": "Correct or complete inaccurate personal data without undue delay.",
            "priority": "Medium"
        }

    # Article 20 — Data Portability
    if any(k in t for k in ["data portability", "export my data", "download my data",
                              "transfer my data", "portable format", "machine readable",
                              "move my data", "send my data to another"]):
        return {
            "request_type": "Data Portability Request",
            "gdpr_article": "Article 20 — Right to Data Portability",
            "action": "Provide personal data in a structured, machine-readable format (e.g. CSV/JSON) within 30 days.",
            "priority": "Medium"
        }

    # Article 18 — Right to Restriction
    if any(k in t for k in ["restrict processing", "pause processing", "limit processing",
                              "put a hold on", "suspend processing", "freeze my data"]):
        return {
            "request_type": "Restriction of Processing",
            "gdpr_article": "Article 18 — Right to Restriction of Processing",
            "action": "Restrict processing of personal data — store it but take no further action until resolved.",
            "priority": "High"
        }

    # Article 13/14 — Privacy Notice
    if any(k in t for k in ["privacy notice", "privacy policy", "how do you use my data",
                              "what do you do with my data", "why do you collect",
                              "lawful basis", "legal basis", "data retention policy",
                              "who do you share my data with"]):
        return {
            "request_type": "Privacy Notice / Transparency Enquiry",
            "gdpr_article": "Article 13 & 14 — Right to be Informed",
            "action": "Provide clear information on data purpose, lawful basis, retention period, and third-party sharing.",
            "priority": "Low"
        }

    # Article 22 — Automated Decision Making
    if any(k in t for k in ["automated decision", "profiling", "algorithm decided",
                              "ai decision", "automated processing", "no human reviewed",
                              "automated rejection", "machine made the decision"]):
        return {
            "request_type": "Automated Decision Making / Profiling",
            "gdpr_article": "Article 22 — Automated Individual Decision-Making",
            "action": "Provide human review of the decision, explain the logic, and allow the individual to contest it.",
            "priority": "High"
        }

    # Article 77 — Right to Lodge a Complaint
    if any(k in t for k in ["complaint", "report to ico", "supervisory authority",
                              "raise a concern", "file a complaint", "report a breach",
                              "report to regulator"]):
        return {
            "request_type": "Complaint / Supervisory Authority Referral",
            "gdpr_article": "Article 77 — Right to Lodge a Complaint",
            "action": "Acknowledge the complaint, investigate, and advise the individual of their right to contact the ICO.",
            "priority": "High"
        }

    # Fallback
    return {
        "request_type": "General Enquiry",
        "gdpr_article": "No specific GDPR article triggered",
        "action": "Review manually and respond within a reasonable timeframe.",
        "priority": "Low"
    }
