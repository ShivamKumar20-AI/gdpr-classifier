import requests

BASE_URL = "http://localhost:8000"

tests = [
    # (description, input text, expected article)
    ("SAR",              "I want to know what data you hold about me",                "Article 15"),
    ("Erasure",          "Please delete all my personal data and forget me",          "Article 17"),
    ("Data Breach",      "We have had a data breach, customer data was exposed",      "Article 33"),
    ("Right to Object",  "I want to stop you processing my data, withdraw consent",   "Article 21"),
    ("Rectification",    "My address in your system is wrong, please correct it",     "Article 16"),
    ("Portability",      "I want to export my data in a portable format",             "Article 20"),
    ("Restriction",      "Please restrict processing of my data immediately",         "Article 18"),
    ("Privacy Notice",   "What is your lawful basis for collecting my data?",         "Article 13"),
    ("Automated AI",     "An algorithm made a decision about me with no human review","Article 22"),
    ("Complaint",        "I want to raise a complaint and report to the ICO",         "Article 77"),
    ("Fallback",         "Hi, I have a general question about your service",          "No specific"),
]

passed = 0
failed = 0

print("\n🧪 Running GDPR Classifier Tests\n" + "="*45)

for name, text, expected in tests:
    try:
        r = requests.post(f"{BASE_URL}/classify", json={"text": text})
        data = r.json()
        article = data.get("gdpr_article", "")
        ok = expected in article
        status = "✅ PASS" if ok else "❌ FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"{status}  [{name}]")
        if not ok:
            print(f"       Expected: {expected}")
            print(f"       Got:      {article}")
    except Exception as e:
        print(f"💥 ERROR [{name}]: {e}")
        failed += 1

print("="*45)
print(f"\n✅ Passed: {passed}  ❌ Failed: {failed}  Total: {len(tests)}\n")