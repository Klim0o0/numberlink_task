from numberlink.point import Point
from typing import *


class Field:
    def __init__(self, field: List[List[str]]):
        self.points = {}
        self.cells: List[List[str]] = []
        for x in range(len(field)):
            new_line = []
            for y in range(len(field[x])):
                new_line.append(field[x][y])
                if field[x][y] != 0:
                    if self.points.get(field[x][y]) == None:
                        t = [Point(x, y)]
                        self.points[field[x][y]] = t
                    else:
                        self.points[field[x][y]].append(Point(x, y))

            self.cells.append(new_line)

    def __getitem__(self, point: Point):
        return self.cells[point.x][point.y]

    def point_in(self, point):
        return 0 <= point.x < len(self.cells) \
               and 0 <= point.y < len(self.cells[point.x])

    def __setitem__(self, point, value):
        self.cells[point.x][point.y] = value

    def get_neighbors(self, point: Point):
        neighbors: List[Point] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                current_point = Point(point.x + x, point.y + y)
                if x == 0 and y == 0:
                    continue
                if self.point_in(current_point):
                    neighbors.append(current_point)
        return neighbors


class RectangularField(Field):
    def __init__(self, field: List[List[str]]):
        Field.__init__(self, field)

    def get_neighbors(self, point: Point):
        neighbors: List[Point] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) == abs(y):
                    continue
                corrent_point: Point = Point(point.x + x, point.y + y)
                if self.point_in(corrent_point):
                    neighbors.append(corrent_point)
        return neighbors


class HexagonalField(Field):
    def __init__(self, field: List[List[str]]):
        Field.__init__(self, field)
        max_len: int = 0
        for x in range(len(self.cells)):
            if len(self.cells[x]) > max_len:
                max_len = len(self.cells[x])
                self.center_index = x

    def get_neighbors(self, point: Point):
        neighbors = Field.get_neighbors(self, point)
        if point.x < self.center_index:
            n: List[Point] = []
            for i in neighbors:
                if i not in [Point(point.x - 1, point.y + 1), Point(point.x + 1, point.y - 1)]:
                    n.append(i)
            return n

        if point.x > self.center_index:
            n: List[Point] = []
            for i in neighbors:
                if i not in [Point(point.x - 1, point.y - 1), Point(point.x + 1, point.y + 1)]:
                    n.append(i)
            return n

        n: List[Point] = []
        for i in neighbors:
            if i not in [Point(point.x + 1, point.y + 1), Point(point.x - 1, point.y + 1)]:
                n.append(i)
        return n
