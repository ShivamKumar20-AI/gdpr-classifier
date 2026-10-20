# security.py
import hashlib
import hmac
import re
import secrets

from secrets_helper import get_secret

MAX_INPUT_LEN = 2000
MIN_INPUT_LEN = 10

# Very basic pattern checks; adjust as needed
DANGEROUS_PATTERNS = [
    r"<script",
    r"javascript:",
    r"on\w+\s*=",
    r"```\s*\w+",
    r"curl\s+http",
    r"wget\s+http",
    r"rm\s+-rf",
    r"eval\s*\(",
    r"exec\s*\(",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in DANGEROUS_PATTERNS]


def sanitize_input(text: str) -> str:
    """
    Basic sanitisation and length checks for user-provided text.
    Raises ValueError if input is invalid.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    text = text.strip()

    if len(text) < MIN_INPUT_LEN:
        raise ValueError(f"Input too short (min {MIN_INPUT_LEN} characters)")

    if len(text) > MAX_INPUT_LEN:
        raise ValueError(f"Input too long (max {MAX_INPUT_LEN} characters)")

    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            raise ValueError("Input contains disallowed patterns")

    # Optionally strip control characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    return text


# Salt for hashing. Set HASH_SALT in the environment (or Streamlit secrets) for hashes that
# stay comparable between restarts. Without it a random salt is made each time the app starts,
# so short, guessable requests cannot be matched to their hash by an outsider.
_SALT = (get_secret("HASH_SALT") or secrets.token_hex(16)).encode("utf-8")


def hash_input(text: str) -> str:
    """
    Create a salted, non-reversible hash of the input for logging/auditing.
    """
    return hmac.new(_SALT, (text or "").encode("utf-8"), hashlib.sha256).hexdigest()
