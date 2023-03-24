from seraph import point
from seraph import utils

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
    def __init__(self, pixel: Pixel, strictness: int=0.8) -> None:
        pixel.edge = self
        self.pixels = [pixel]

        self.strictness = strictness

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

    def __eq__(self, edge: object) -> int or float:
        return self % edge <= self.strictness

    def __lshift__(self, pixel: Pixel) -> bool:
        if pixel not in self:
            pixel.edge = self
            self.pixels.append(pixel)
            return True
        return False

    def __mod__(self, edge: object) -> int or float:
        sim = 0
        for point1 in self:
            for point2 in edge:
                sim += point1.location % point2.location
        
        return sim

    def __invert__(self) -> ExpandedPointEntity:
        return point.midpoint(self.points())

    def points(self) -> list[point.ExpandedPointEntity]:
        return [pixel.location for pixel in self]

class Object:
    # look, at least i'm not name-colliding the base "object" class.

    def __init__(self, edges: list[Edge]) -> None:
        self.edges = edges

    def __repr__(self) -> str:
        return "<seraph.vision.Object>"

    def __len__(self) -> int:
        return len(self.edges)

    def __mod__(self, other: object) -> float:
        if len(self) >= len(other):
            return other % self
        
        matches = 0
        for edge in self:
            if edge in other:
                matches += 1

        return matches / len(self)

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

    def mapEdges(self, threshold: int=256, strictness: int=1) -> list[Edge]:
        poi = [pixel for pixel in self if ~pixel >= threshold]
        
        edges = []

        def mapped(x):
            for edge in edges:
                if x in edge:
                    return True
            return False

        for point in poi:
            if not mapped(poi):
                edge = Edge(point)
                for otherPoint in poi:
                    edge << otherPoint
                self.edges.append(edge)

        return edges

    def mapObjects(self, threshold)
