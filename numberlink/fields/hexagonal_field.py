from typing import List

from numberlink.fields.field import Field
from numberlink.point import Point


class HexagonalField(Field):
    def __init__(self, field: List[List[str]]):
        super(HexagonalField, self).__init__(field)
        max_len: int = 0
        for x in range(len(self.cells)):
            if len(self.cells[x]) > max_len:
                max_len = len(self.cells[x])
                self.center_index = x

    def __str__(self):
        field: List[str] = []
        for x in range(len(self.cells)):
            field.append(' ' * (len(self.cells[self.center_index]) - len(
                self.cells[x])))
            for y in range(len(self.cells[x])):
                field.append(self.cells[x][y]+' ')
            field.append('\n')

        return ''.join(field)

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

        for x in range(int(len(self.cells) / 2) + 1, len(self.cells)):
            if len(self.cells[x]) + 1 != len(self.cells[x - 1]):
                return False

        return True

    def get_neighbors(self, point: Point) -> List[Point]:
        neighbors = Field.get_neighbors(self, point)
        if point.x < self.center_index:
            hex_neighbors: List[Point] = []
            for neighbor in neighbors:
                if neighbor not in [Point(point.x - 1, point.y + 1),
                                    Point(point.x + 1, point.y - 1)]:
                    hex_neighbors.append(neighbor)
            return hex_neighbors

        if point.x > self.center_index:
            hex_neighbors: List[Point] = []
            for neighbor in neighbors:
                if neighbor not in [Point(point.x - 1, point.y - 1),
                                    Point(point.x + 1, point.y + 1)]:
                    hex_neighbors.append(neighbor)
            return hex_neighbors

        hex_neighbors: List[Point] = []
        for neighbor in neighbors:
            if neighbor not in [Point(point.x + 1, point.y + 1),
                                Point(point.x - 1, point.y + 1)]:
                hex_neighbors.append(neighbor)
        return hex_neighbors
