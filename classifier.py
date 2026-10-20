import logging
import re
from dataclasses import dataclass
from pathlib import Path

from security import sanitize_input, hash_input


# Configure audit logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "gdpr_classification_audit.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Lower number = more urgent. A request that trips several rules is reported
# under the most urgent one: a message that both asks for a copy of personal
# data and discloses a breach is a breach first, because Article 33 carries a
# 72-hour notification deadline that Article 15's 30 days does not.
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


@dataclass(frozen=True)
class Rule:
    request_type: str
    gdpr_article: str
    action: str
    priority: str
    triggers: tuple[str, ...]
    # Regular expressions for wording that fixed phrases miss, such as "delete all the
    # personal data you hold" (a fixed phrase only catches "delete all my personal data").
    patterns: tuple[str, ...] = ()

    def matches(self, text: str) -> bool:
        if any(trigger in text for trigger in self.triggers):
            return True
        return any(re.search(pattern, text) for pattern in self.patterns)


# Order matters for ties: Erasure is listed before Access, so a request that asks to delete the data
# a company holds is treated as erasure, not just access.
RULES: tuple[Rule, ...] = (
    Rule(
        request_type="Right to Erasure",
        gdpr_article="Article 17 — Right to be Forgotten",
        action="Erase all personal data unless a lawful retention basis applies.",
        priority="High",
        triggers=(
            "delete my data", "delete all my data", "i want to delete", "right to erasure",
            "remove my information", "forget me", "erase my data", "right to be forgotten",
            "wipe my data", "remove all my details", "delete all my personal data",
        ),
        patterns=(
            r"\b(delete|erase|wipe)\b.{0,40}\b(data|information|details|records|account)\b",
            r"\bremove\b.{0,20}\bmy\b.{0,20}\b(data|information|details|records)\b",
        ),
    ),
    Rule(
        request_type="Subject Access Request (SAR)",
        gdpr_article="Article 15 — Right of Access",
        action="Respond within 30 days with a copy of all personal data held.",
        priority="High",
        triggers=(
            "subject access request", "access to my data", "what data do you hold",
            "copy of my data", "what information do you have on me",
            "personal data you hold about me", "data you hold about me",
        ),
        # "sar" on its own, not inside words such as "necessary" or "disarray"
        patterns=(r"\bsar\b",),
    ),
    Rule(
        request_type="Data Breach Report",
        gdpr_article="Article 33 — Notification of Personal Data Breach",
        action="Notify the ICO within 72 hours if risk to individuals is likely.",
        priority="Critical",
        triggers=(
            "data breach", "unauthorised access", "leaked", "hacked",
            "personal data exposed", "security incident", "compromised", "cyber attack",
            "data leak",
        ),
    ),
    Rule(
        request_type="Right to Object / Withdraw Consent",
        gdpr_article="Article 21 — Right to Object",
        action="Stop processing personal data unless compelling legitimate grounds exist.",
        priority="High",
        triggers=(
            "stop processing", "opt out", "object to processing", "withdraw consent",
            "no longer consent", "revoke consent", "unsubscribe from processing",
        ),
    ),
    Rule(
        request_type="Right to Rectification",
        gdpr_article="Article 16 — Right to Rectification",
        action="Correct or complete inaccurate personal data without undue delay.",
        priority="Medium",
        triggers=(
            "update my data", "correct my information", "wrong details", "inaccurate data",
            "change my address", "update my name", "fix my details",
            "incorrect information", "is incorrect", "my address is", "my name is wrong",
            "wrong address", "wrong name", "update my address", "please correct",
            "needs to be updated", "out of date", "my address is wrong",
        ),
    ),
    Rule(
        request_type="Data Portability Request",
        gdpr_article="Article 20 — Right to Data Portability",
        action="Provide personal data in a structured, machine-readable format (e.g. CSV/JSON) within 30 days.",
        priority="Medium",
        triggers=(
            "data portability", "export my data", "download my data", "transfer my data",
            "portable format", "machine readable", "move my data",
            "send my data to another",
        ),
    ),
    Rule(
        request_type="Restriction of Processing",
        gdpr_article="Article 18 — Right to Restriction of Processing",
        action="Restrict processing of personal data — store it but take no further action until resolved.",
        priority="High",
        triggers=(
            "restrict processing", "pause processing", "limit processing", "put a hold on",
            "suspend processing", "freeze my data",
        ),
    ),
    Rule(
        request_type="Privacy Notice / Transparency Enquiry",
        gdpr_article="Article 13 & 14 — Right to be Informed",
        action="Provide clear information on data purpose, lawful basis, retention period, and third-party sharing.",
        priority="Low",
        triggers=(
            "privacy notice", "privacy policy", "how do you use my data",
            "what do you do with my data", "why do you collect", "lawful basis",
            "legal basis", "data retention policy", "who do you share my data with",
        ),
    ),
    Rule(
        request_type="Automated Decision Making / Profiling",
        gdpr_article="Article 22 — Automated Individual Decision-Making",
        action="Provide human review of the decision, explain the logic, and allow the individual to contest it.",
        priority="High",
        triggers=(
            "automated decision", "profiling", "algorithm decided", "ai decision",
            "automated processing", "no human reviewed", "automated rejection",
            "machine made the decision",
        ),
    ),
    Rule(
        request_type="Complaint / Supervisory Authority Referral",
        gdpr_article="Article 77 — Right to Lodge a Complaint",
        action="Acknowledge the complaint, investigate, and advise the individual of their right to contact the ICO.",
        priority="High",
        triggers=(
            "complaint", "report to ico", "supervisory authority", "raise a concern",
            "file a complaint", "report a breach", "report to regulator",
        ),
    ),
)


def classify(text: str) -> dict[str, str]:
    try:
        clean_text = sanitize_input(text)
    except ValueError as e:
        input_hash = hash_input(text)
        logger.warning("Invalid input: input_hash=%s reason=%s", input_hash, str(e))
        return {
            "request_type": "Invalid Input",
            "gdpr_article": "Input Validation Error",
            "action": f"Fix input: {str(e)}",
            "priority": "Error"
        }

    t = clean_text.lower()
    input_hash = hash_input(clean_text)

    matched = [rule for rule in RULES if rule.matches(t)]

    if not matched:
        logger.info(
            "Classification: input_hash=%s request_type=%s priority=%s",
            input_hash,
            "General Enquiry",
            "Low",
        )
        return {
            "request_type": "General Enquiry",
            "gdpr_article": "No specific GDPR article triggered",
            "action": "Review manually and respond within a reasonable timeframe.",
            "priority": "Low"
        }

    # Most urgent wins; ties fall back to the order the rules are declared in.
    primary = min(
        matched,
        key=lambda rule: (SEVERITY_ORDER[rule.priority], RULES.index(rule)),
    )
    secondary = [rule.request_type for rule in matched if rule is not primary]

    logger.info(
        "Classification: input_hash=%s request_type=%s priority=%s also_detected=%s",
        input_hash,
        primary.request_type,
        primary.priority,
        secondary or "none",
    )

    result = {
        "request_type": primary.request_type,
        "gdpr_article": primary.gdpr_article,
        "action": primary.action,
        "priority": primary.priority,
    }
    if secondary:
        result["also_detected"] = ", ".join(secondary)
    return result
