from typing import List

from numberlink.fields.field import Field
from numberlink.path import Path
from numberlink.point import Point
from numberlink.fields.rectangular_field import RectangularField


class Solver:

    def __init__(self, field: Field):
        self.field = field
        self.max_solve_count = -1

    def solve(self) -> List[Path]:

        parent_paths: List[Path] = [None]

        for owner in self.field.points:
            temp_parent_paths: List[Path] = []
            for parent_path in parent_paths:
                temp_parent_paths += self.find_path(
                    self.field.points[owner][0],
                    self.field.points[owner][1],
                    parent_path,
                    [])
            parent_paths = temp_parent_paths
        return self.find_correct_paths(parent_paths)

    def find_path(self, current: Point, target: Point, parent_path: Path,
                  path: List[Point]) -> List[Path]:

        path.append(current)
        if current == target:
            return [Path(parent_path, self.field[target], path)]
        paths: List[Path] = []
        for neighbor in self.field.get_neighbors(current):
            if target != neighbor \
                    and (self.field[neighbor] != '0'
                         or (parent_path is not None
                             and parent_path.is_point_in_path(neighbor))
                         or neighbor in path):
                continue
            for p in self.find_path(neighbor, target, parent_path, list(path)):
                paths.append(p)
        return paths

    def find_correct_paths(self, paths: List[Path]):
        correct_paths: List[Path] = []
        for path in paths:
            if len(correct_paths) == self.max_solve_count:
                return correct_paths
            if self.is_correct_path(path):
                correct_paths.append(path)
        return correct_paths

    def is_correct_path(self, path: Path):
        count = 0
        while path is not None:
            count += len(path.path)
            path = path.parent_path
        return count == self.field.cells_count
