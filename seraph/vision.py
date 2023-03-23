from seraph import point

def hsv(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

class Pixel:
    def __init__(self, x: int, y: int, strictness: int or float=.8, **colors: dict[str: int]) -> None:
        self.colors = colors
        self.location = point.ExpandedPointEntity(x, y)
        self.parent: object = None

    def __repr__(self) -> str:
        return "<seraph.vision.Pixel " + " ".join([key + "=" + str(val) for key, val in self])

    def __len__(self) -> int:
        return len(self.colors.keys())
    
    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> tuple[str, int]:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return (self.colors.keys()[self.n], self.colors[self.colors.keys()[self.n]])

    def __mod__(self, other: object) -> int:
        assert self.colors.keys() == other.colors.keys(), "Can only compare Pixels of similar color dictionaries."

        return sum([x2 - x1 for x1, x2 in zip(self.colors.keys(), other.colors.keys())])

    def __invert__(self) -> int:
        return sum([self % neighbor for neighbor in self.parent.neighbors(self)])

class Edge:
    pass

class Image:
    def __init__(self, pixels: list[list[Pixel]]) -> None:
        self.rows = pixels

        self.height = len(rows)
        self.width = len(rows[0])

        for row in self.rows:
            assert len(row) == self.width, "All rows in an Image must be the same length."

    def __repr__(self) -> str:
        return "<seraph.vision.Image " + str(self.width) + "x" + str(self.height) + ">"

    def __invert__(self) -> list[list[int]]:
        return [[~pixel for pixel in row] for row in self.rows]

    def neighbors(self, target: Pixel) -> list[Pixel]:
        return [pixel for pixel in self if pixel.location == target.location]