from cell import Cell
from point import Point
from typing import *


class Field:

    def __init__(self, field: List[List[Cell]]):
        self.points: Dict[str, List[Point]] = {}
        self.cells: List[List[Cell]] = []

        for x in range(len(field)):
            new_line = []
            for y in range(len(field[x])):
                new_line.append(Cell(field[x][y].owner,
                                     field[x][y].previous_point,
                                     field[x][y].next_point))

                if field[x][y].owner != '0':
                    if self.points.get(field[x][y].owner) is None:
                        self.points[field[x][y].owner] = [Point(x, y)]
                    else:
                        self.points[field[x][y].owner].append(
                            Point(x, y))

            self.cells.append(new_line)

    def get_paths(self):
        solve: Dict[str:List[Point]] = {}
        for owner in self.points.keys():
            current_point = self[self.points[owner][0]]
            path: List[Point] = [self.points[owner][0]]
            while current_point.next_point is not None:
                path.append(current_point.next_point)
                current_point = self[current_point.next_point]
            solve[owner] = path
        return solve

    def __getitem__(self, point: Point) -> Cell:
        return self.cells[point.x][point.y]

    def __setitem__(self, point, value):
        self.cells[point.x][point.y] = value

    def __str__(self):
        s = ''
        for x in self.cells:
            for y in x:
                s += y.owner+ ' '
            s+='\n'
        return s


    def copy(self):
        field = self.__class__(self.cells)
        field.points = self.points
        return field

    @classmethod
    def build_field_from_file(cls, file_path):
        cells: List[List[Cell]] = []
        with open(file_path) as file:
            text: List[str] = file.read().split('\n')

            for x in range(len(text)):
                field_line = []
                t = text[x].split()

                for y in range(len(t)):
                    field_line.append(Cell(t[y]))
                cells.append(field_line)
        field = cls(cells)
        if field.is_correct_field():
            return field
        return None

    @classmethod
    def build_field_from_array(cls, field: List[List[str]]):
        cells = cls.get_cells(field)
        return cls(cells)

    def is_correct_field(self) -> bool:
        return True

    @classmethod
    def get_cells(cls, field: List[List[str]]) -> List[List[Cell]]:
        cells: List[List[Cell]] = []
        for x in range(len(field)):
            cells_line: List[Cell] = []
            for y in range(len(field[x])):
                cells_line.append(Cell(str(field[x][y])))
            cells.append(cells_line)
        return cells

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
