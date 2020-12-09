from typing import Dict, List
from numberlink.point import Point


class Field:

    def __init__(self, field: List[List[str]]):
        self.points: Dict[str, List[Point]] = {}
        self.cells: List[List[str]] = field
        self.cells_count = 0

        for x in range(len(field)):
            for y in range(len(field[x])):
                self.cells_count += 1
                if field[x][y] != '0':
                    if self.points.get(field[x][y]) is None:
                        self.points[field[x][y]] = [Point(x, y)]
                    else:
                        self.points[field[x][y]].append(
                            Point(x, y))

    def __getitem__(self, point: Point) -> str:
        return self.cells[point.x][point.y]

    def __str__(self):
        field: List[str] = []
        for cells_line in self.cells:
            for cell in cells_line:
                field.append(cell+' ')
            field.append('\n')
        return ''.join(field)

    @classmethod
    def build_field_from_file(cls, file_path):
        cells: List[List[str]] = []
        with open(file_path) as file:
            lines: List[str] = file.read().split('\n')

            for x in range(len(lines)):
                field_line = []
                items = lines[x].split()

                for y in range(len(items)):
                    field_line.append(items[y])
                cells.append(field_line)

        field = cls(cells)
        if field.is_correct_field():
            return field
        return None

    def is_correct_field(self) -> bool:
        return True

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
                    neighbors.append(current_point)
        return neighbors
