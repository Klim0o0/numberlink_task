from numberlink.fields.field import Field
from numberlink.point import Point
from typing import *


class RectangularField(Field):

    def __init__(self, field: List[List[str]]):
        super(RectangularField, self).__init__(field)

    def __str__(self):
        field_str = ''
        for cells_line in self.cells:
            for cell in cells_line:
                field_str += cell + ' '
            field_str += '\n'
        return field_str

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

    def is_correct_field(self) -> bool:
        for point in self.points.keys():
            if len(self.points[point]) != 2:
                return False

        if len(self.cells) == 0 or len(self.cells[0]) == 0:
            return False

        standard_y = len(self.cells[0])
        for line in self.cells:
            if len(line) != standard_y:
                return False
        return True
