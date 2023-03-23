from seraph import point
from seraph import utils

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
        self.edge: object = None

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

        return sum([abs(x2 - x1) for x1, x2 in zip(self.colors.keys(), other.colors.keys())])

    def __invert__(self) -> int:
        return sum([self % neighbor for neighbor in self.parent.neighbors(self)])

class Edge:
    def __init__(self, pixel: Pixel) -> None:
        pixel.edge = self
        self.pixels = [pixel]

    def __repr__(self) -> str:
        return "<seraph.vision.Edge of length " + str(len(self)) + ">"

    def __len__(self) -> int:
        return len(self.pixels)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Pixel:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self[self.n]

    def __getitem__(self, index: int) -> Pixel:
        return self.pixels[index]

    def __contains__(self, target: Pixel) -> bool:
        for pixel in self:
            if pixel.location == target.location:
                return True
        return False

    def __lshift__(self, pixel: Pixel) -> bool:
        if pixel not in self:
            pixel.edge = self
            self.pixels.append(pixel)
            return True
        return False

class Image:
    def __init__(self, pixels: list[list[Pixel]]) -> None:
        self.rows = pixels

        self.height = len(rows)
        self.width = len(rows[0])

        for row in self.rows:
            assert len(row) == self.width, "All rows in an Image must be the same length."

    def __repr__(self) -> str:
        return "<seraph.vision.Image " + str(self.width) + "x" + str(self.height) + ">"

    def __iter__(self) -> object:
        self.r = 0
        self.c = -1
        return self
    
    def __next__(self) -> Pixel:
        self.c += 1
        try:
            return self.rows[self.r][self.c]
        except IndexError:
            try:
                self.c = -1
                self.r += 1
                return next(self)
            except IndexError:
                raise StopIteration

    def __invert__(self) -> list[list[int]]:
        return [[~pixel for pixel in row] for row in self.rows]

    def neighbors(self, target: Pixel) -> list[Pixel]:
        return [pixel for pixel in self if pixel.location == target.location]

    def mapEdges(self, threshold: int=256):
        poi = [pixel for pixel in self if ~pixel >= threshold]
        