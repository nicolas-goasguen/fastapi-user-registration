import random
import re


def is_valid_password(password: str) -> bool:
    pattern = re.compile(
        "^(?=.*[a-z])"
        "(?=.*[A-Z])"
        "(?=.*\d)"
        "(?=.*[@$!%*#?&])"
        "[A-Za-z\d@$!#%*?&]{6,20}$"
    )
    return bool(re.search(pattern, password))


def is_valid_verification_code(code: str) -> bool:
    pattern = re.compile("^[0-9]{4}$")
    return bool(re.match(pattern, code))


def generate_random_4_digits() -> str:
    return "".join(random.choices("0123456789", k=4))
