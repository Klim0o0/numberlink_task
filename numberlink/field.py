from numberlink.cell import Cell
from numberlink.point import Point
from typing import *


class Field:
    def __init__(self, field: List[List[Cell]]):
        self.points: Dict[str, List[Point]] = {}
        self.cells: List[List[Cell]] = []

        for x in range(len(field)):
            new_line = []
            for y in range(len(field[x])):
                new_line.append(Cell(field[x][y].owner,
                                     field[x][y].previous,
                                     field[x][y].next))

                if field[x][y].owner != '0':
                    if self.points.get(field[x][y].owner) is None:
                        self.points[field[x][y].owner] = [Point(x, y)]
                    else:
                        self.points[field[x][y].owner].append(
                            Point(x, y))

            self.cells.append(new_line)

    def __str__(self):
        s = ''
        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                s+=self.cells[x][y].owner
            s+='\n'
        return s

    def __getitem__(self, point: Point) -> Cell:
        return self.cells[point.x][point.y]

    def __setitem__(self, point, value):
        self.cells[point.x][point.y] = value

    def copy(self):
        field = self.__class__(self.cells)
        field.points = self.points
        return field

    @classmethod
    def build_field_from_file(cls, file_path):
        field: List[List[Cell]] = []
        with open(file_path) as file:
            text: List[str] = file.read().split('\n')

            for x in range(len(text)):
                field_line = []
                t = text[x].split()

                for y in range(len(t)):
                    field_line.append(Cell(t[y]))
                field.append(field_line)

        return cls(field)

    def point_in(self, point) -> bool:
        return 0 <= point.x < len(self.cells) \
               and 0 <= point.y < len(self.cells[point.x])

    def get_neighbors(self, point: Point) -> List[Point]:
        neighbors: List[Point] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                current_point = Point(point.x + x, point.y + y)

                if self.point_in(current_point):
                    neighbors.append(
                        current_point)
        return neighbors


class RectangularField(Field):

    def __init__(self, field: List[List[Point]]):
        Field.__init__(self, field)

    def get_neighbors(self, point: Point) -> List[Point]:
        neighbors: List[Point] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) == abs(y):
                    continue
                current_point: Point = Point(point.x + x, point.y + y)
                if self.point_in(current_point):
                    neighbors.append(
                        current_point)
        return neighbors


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
                if self.cells[x][y].next is None \
                        or self.cells[x][y].previous is None:
                    s += self.cells[x][y].owner + ' '
                else:
                    s += str(Field._select_pipe(self.cells[x][y],
                                            Point(x, y)) )+ ' '
            s += '\n'

        return s

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
