# security.py
import hashlib
import re
from typing import Tuple

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


def hash_input(text: str) -> str:
    """
    Create a non-reversible hash of the input for logging/auditing.
    """
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def mask_sensitive_text(text: str, keep_chars: int = 10) -> str:
    """
    For display/logging: show only first/last few chars.
    """
    if len(text) <= keep_chars * 2:
        return "*" * len(text)
    return text[:keep_chars] + "..." + text[-keep_chars:]