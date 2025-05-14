import random
import re


def is_valid_password(password: str):
    pattern = re.compile(
        "^(?=.*[a-z])"
        "(?=.*[A-Z])"
        "(?=.*\d)"
        "(?=.*[@$!%*#?&])"
        "[A-Za-z\d@$!#%*?&]{6,20}$"
    )
    return re.search(pattern, password)


def is_valid_verification_code(code):
    pattern = re.compile("^[0-9]{4}$")
    return re.search(pattern, code)


def generate_4_digits():
    return "".join(random.choices("0123456789", k=4))
