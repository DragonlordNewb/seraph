import random
import warnings

UNKNOWN = 0
DELTA = "DELTA"
ABSOLUTE = "ABSOLUTE"

def plusOrMinus(x: int, n: int) -> int:
    return x + random.randint(-n, n)

class UnsafeValueWarning(warnings.Warning):
    pass