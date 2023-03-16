import random
import warnings

UNKNOWN = 0
DELTA = "DELTA"
ABSOLUTE = "ABSOLUTE"
ACTION = "ACTION"
REACTION = "REACTION"
SEQBREAK = "SEQBREAK"

def plusOrMinus(x: int, n: int) -> int:
    return x + random.randint(-n, n)

class UnsafeValueWarning(Warning):
    pass

def levenshtein(a, b):
    if len(b) == 0:
        return len(a)
    if len(a) == 0:
        return len(b)

    if len(a) == len(b):
        return levenshtein(a[1:], b[1:])

    return 1 + min([
        levenshtein(a, b[1:]),
        levenshtein(a[1:], b),
        levenshtein(a[1:], b[1:])
    ])