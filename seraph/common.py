import random

UNKNOWN = 0

def plusOrMinus(x: int, n: int) -> int:
    return x + random.randint(-n, n)