"""Small, offline password checks for learning Python; not a security audit."""

import string
from pathlib import Path


# These are examples, not a complete list of predictable passwords.
PREDICTABLE_PATTERNS = [
    "1234", "4321", "abcd", "dcba", "qwer", "asdf", "zxcv", "abc123",
    "password", "passw0rd", "p@ssword", "p@ssw0rd", "letmein", "welcome",
    "admin", "iloveyou", "changeme",
]


def load_common_passwords():
    # Resolve the file beside this module, not in the terminal's current folder.
    file_path = Path(__file__).resolve().with_name("common_passwords.txt")
    common_passwords = set()
    with file_path.open("r", encoding="utf-8") as password_file:
        for line in password_file:
            word = line.rstrip("\r\n")
            if word:
                common_passwords.add(word.lower())
    if not common_passwords:
        raise ValueError("The common-password list is empty.")
    return common_passwords


def is_common_password(password, common_passwords):
    return password.lower() in common_passwords


def has_repeated_characters(password):
    lowered = password.lower()
    # Compare each character with the next two: "aaa" fails, but "aba" does not.
    for index in range(len(lowered) - 2):
        if lowered[index] == lowered[index + 1] == lowered[index + 2]:
            return True
    return False


def has_predictable_pattern(password):
    lowered = password.lower()
    for pattern in PREDICTABLE_PATTERNS:
        if pattern in lowered:
            return True
    return False


def get_strength_label(score):
    if score < 20:
        return "Very Weak"
    elif score < 40:
        return "Weak"
    elif score < 60:
        return "Medium"
    elif score < 90:
        return "Strong"
    else:
        return "Very Strong"


def analyze_password(password, common_passwords):
    length = len(password)
    has_uppercase = False
    has_lowercase = False
    has_number = False
    has_special = False
    for character in password:
        if character.isupper():
            has_uppercase = True
        if character.islower():
            has_lowercase = True
        if character.isdigit():
            has_number = True
        if character in string.punctuation:
            has_special = True

    repeated = has_repeated_characters(password)
    predictable = has_predictable_pattern(password)
    common = is_common_password(password, common_passwords)

    # Start with length points, then add points for the other checks.
    if length >= 16:
        score = 40
    elif length >= 12:
        score = 25
    elif length >= 8:
        score = 10
    else:
        score = 0
    for requirement_met in (has_uppercase, has_lowercase, has_number, has_special):
        if requirement_met:
            score += 10
    if not repeated:
        score += 10
    if not predictable:
        score += 10

    # min(score, limit) stops obvious weaknesses from receiving a high score.
    if length == 0:
        score = 0
    elif length < 8:
        score = min(score, 19)
    elif length < 12:
        score = min(score, 59)
    if repeated:
        score = min(score, 59)
    if predictable:
        score = min(score, 39)
    if common:
        score = min(score, 19)

    checks = {
        "At least 12 characters": length >= 12,
        "16 or more characters (recommended)": length >= 16,
        "Contains uppercase letters": has_uppercase,
        "Contains lowercase letters": has_lowercase,
        "Contains numbers": has_number,
        "Contains special characters (ASCII punctuation)": has_special,
        "No three identical characters in a row (case-insensitive)": not repeated,
        "No patterns from the example list": not predictable,
        "Not in the bundled common-password sample": not common,
    }

    suggestions = []
    if length < 12:
        suggestions.append("Use at least 12 characters; 16 or more is recommended.")
    elif length < 16:
        suggestions.append("Increase the length to 16 or more characters.")
    if not has_uppercase:
        suggestions.append("Include uppercase letters, without relying on an initial capital alone.")
    if not has_lowercase:
        suggestions.append("Include lowercase letters.")
    if not has_number:
        suggestions.append("Include numbers, but avoid obvious sequences or dates.")
    if not has_special:
        suggestions.append("Include punctuation such as !, @, or #.")
    if repeated:
        suggestions.append("Avoid runs of three or more identical characters.")
    if predictable:
        suggestions.append("Avoid obvious words and patterns such as password, qwerty, or 1234.")
    if common:
        suggestions.append("Replace this common password entirely, rather than making a small change.")
    if not suggestions:
        suggestions.append("No obvious issues were found by these limited checks.")
    suggestions.append("Use a unique password for every account and a reputable password manager.")
    suggestions.append("Enable multi-factor authentication where available.")

    # Return findings only: callers do not need the password in the result.
    return {
        "length": length,
        "score": score,
        "rating": get_strength_label(score),
        "checks": checks,
        "suggestions": suggestions,
    }
