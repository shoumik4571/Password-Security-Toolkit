"""Generate passwords with operating-system-backed randomness."""

import secrets
import string

from password_checker import analyze_password


MIN_LENGTH = 12
MAX_LENGTH = 128
DEFAULT_LENGTH = 16
ALL_CHARACTERS = string.ascii_letters + string.digits + string.punctuation


def generate_password(length, common_passwords):
    if isinstance(length, bool) or not isinstance(length, int):
        raise ValueError("Password length must be a whole number.")
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH}.")

    secure_random = secrets.SystemRandom()

    # Limit retries in case the checker rules are changed later.
    for attempt in range(100):
        # Start with one character of each type so none are missing.
        characters = []
        characters.append(secrets.choice(string.ascii_uppercase))
        characters.append(secrets.choice(string.ascii_lowercase))
        characters.append(secrets.choice(string.digits))
        characters.append(secrets.choice(string.punctuation))

        for position in range(length - 4):
            characters.append(secrets.choice(ALL_CHARACTERS))

        # Mix the order securely; the four required types must not have fixed positions.
        secure_random.shuffle(characters)
        password = "".join(characters)

        result = analyze_password(password, common_passwords)
        if result["score"] >= 60:
            return password

    raise RuntimeError("Could not generate a password that passes the local strength checks.")
