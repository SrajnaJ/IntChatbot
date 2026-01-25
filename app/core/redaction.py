import re


EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\b\d{10}\b"
# Updated regex to target monetary amounts specifically
AMOUNT_REGEX = r"(₹|\$)\s?\d{1,3}(,\d{3})*(\.\d+)?"

BLOCK_KEYWORDS = [
    r"\bbank account\b",
    r"\bifsc\b",
    r"\bpan\b",
    r"\baadhaar\b",
    r"\bssn\b"
]


def contains_blocked_info(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(keyword, text_lower) for keyword in BLOCK_KEYWORDS)


def redact_text(text: str) -> str:
    text = re.sub(EMAIL_REGEX, "[REDACTED_EMAIL]", text)
    text = re.sub(PHONE_REGEX, "[REDACTED_PHONE]", text)
    # Only redact monetary amounts, not general numbers
    text = re.sub(AMOUNT_REGEX, "[REDACTED_AMOUNT]", text)
    return text
