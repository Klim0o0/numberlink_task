from cell import Cell
from fields.field import Field
from point import Point
from typing import *


class HexagonalField(Field):
    def __init__(self, field: List[List[Cell]]):
        Field.__init__(self, field)
        max_len: int = 0
        for x in range(len(self.cells)):
            if len(self.cells[x]) > max_len:
                max_len = len(self.cells[x])
                self.center_index = x

    def __str__(self):
        s = ''
        for x in range(len(self.cells)):
            s += ' ' * (len(self.cells[self.center_index]) - len(
                self.cells[x]))
            for y in range(len(self.cells[x])):
                s += self.cells[x][y].owner + ' '
            s += '\n'

        return s

    def is_correct_field(self) -> bool:
        for point in self.points.keys():
            if len(self.points[point]) != 2:
                return False

        if len(self.cells) == 0 or len(self.cells[0]) == 0:
            return False

        if len(self.cells) % 2 == 0:
            return False

        start_len = (len(self.cells) + 1) / 2
        if len(self.cells[0]) != start_len:
            return False

        for x in range(1, int(len(self.cells) / 2)):
            if len(self.cells[x]) - 1 != len(self.cells[x - 1]):
                return False

        for x in range(int(len(self.cells) / 2 )+ 1, len(self.cells)):
            if len(self.cells[x]) + 1 != len(self.cells[x - 1]):
                return False

        return True

    def get_neighbors(self, point: Point) -> List[Point]:
        neighbors = Field.get_neighbors(self, point)
        if point.x < self.center_index:
            n: List[Point] = []
            for i in neighbors:
                if i not in [Point(point.x - 1, point.y + 1),
                             Point(point.x + 1, point.y - 1)]:
                    n.append(i)
            return n

        if point.x > self.center_index:
            n: List[Point] = []
            for i in neighbors:
                if i not in [Point(point.x - 1, point.y - 1),
                             Point(point.x + 1, point.y + 1)]:
                    n.append(i)
            return n

        n: List[Point] = []
        for i in neighbors:
            if i not in [Point(point.x + 1, point.y + 1),
                         Point(point.x - 1, point.y + 1)]:
                n.append(i)
        return n