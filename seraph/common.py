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