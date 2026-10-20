import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from classifier import classify  # noqa: E402
from ratelimit import SlidingWindowLimiter  # noqa: E402
from security import hash_input  # noqa: E402


def request_type(text):
    return classify(text)["request_type"]


def test_deletion_request_found_in_the_security_review_is_now_erasure():
    text = ("Jane Testperson of 1 Fake Street, test.person@example.com: "
            "please delete all the personal data you hold about me.")
    assert request_type(text) == "Right to Erasure"


def test_other_erasure_wordings():
    assert request_type("Please erase the information you have on me") == "Right to Erasure"
    assert request_type("I want you to wipe my account and all details") == "Right to Erasure"
    assert request_type("Please remove my details from your records") == "Right to Erasure"


def test_plain_access_request_is_still_access():
    assert request_type("I want a copy of all the personal data you hold about me.") == "Subject Access Request (SAR)"


def test_sar_keyword_only_matches_as_a_whole_word():
    assert request_type("It is necessary to disarm the old process, thanks") == "General Enquiry"
    assert request_type("This is a SAR from a customer") == "Subject Access Request (SAR)"


def test_breach_still_outranks_other_rules():
    assert request_type("Your company leaked my data in a breach, please delete my data") == "Data Breach Report"


def test_example_requests_in_the_app():
    assert request_type("My address is wrong and needs to be updated.") == "Right to Rectification"
    assert request_type("I want to transfer my data to another provider.") == "Data Portability Request"


def test_hash_is_stable_within_a_run_and_not_a_plain_sha256():
    import hashlib
    assert hash_input("delete my data") == hash_input("delete my data")
    assert hash_input("delete my data") != hashlib.sha256(b"delete my data").hexdigest()


def test_global_rate_limit_ignores_new_sessions():
    limiter = SlidingWindowLimiter(max_requests=3, window_seconds=60)
    assert [limiter.allow(now=t) for t in (0, 1, 2, 3)] == [True, True, True, False]
    assert limiter.allow(now=61) is True  # old requests age out
