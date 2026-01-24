import re


EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\b\d{10}\b"
AMOUNT_REGEX = r"(₹|\$)?\s?\d{1,3}(,\d{3})*(\.\d+)?"

BLOCK_KEYWORDS = [
    "bank account",
    "ifsc",
    "pan",
    "aadhaar",
    "ssn"
]


def contains_blocked_info(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in BLOCK_KEYWORDS)


def redact_text(text: str) -> str:
    text = re.sub(EMAIL_REGEX, "[REDACTED_EMAIL]", text)
    text = re.sub(PHONE_REGEX, "[REDACTED_PHONE]", text)
    text = re.sub(AMOUNT_REGEX, "[REDACTED_AMOUNT]", text)
    return text
