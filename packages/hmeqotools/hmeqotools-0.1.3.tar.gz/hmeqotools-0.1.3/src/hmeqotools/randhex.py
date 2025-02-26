import random

HEXDIGITS = "0123456789abcdefABCDEF"
HEXDIGITS_LOWERCASE = "0123456789abcdef"
HEXDIGITS_UPPERCASE = "0123456789ABCDEF"


def randhex(k: int):
    return "".join(random.choices(HEXDIGITS, k=k))


def randlowerhex(k: int):
    return "".join(random.choices(HEXDIGITS_LOWERCASE, k=k))


def randupperhex(k: int):
    return "".join(random.choices(HEXDIGITS_UPPERCASE, k=k))
