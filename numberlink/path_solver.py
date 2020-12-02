from typing import List

from numberlink.fields.field import Field
from numberlink.path import Path
from numberlink.point import Point
from numberlink.fields.rectangular_field import RectangularField


class PathSolver:

    def __init__(self, field: Field):
        self.field = field

    def solve(self) -> List[Path]:

        parent_paths: List[Path] = [Path(None, '', [])]

        for owner in self.field.points:
            temp_parent_paths: List[Path] = []
            for parent_path in parent_paths:
                temp_parent_paths = self.find_path(self.field.points[owner][0],
                                                   self.field.points[owner][1],
                                                   parent_path,
                                                   [])
            parent_paths = temp_parent_paths
        return parent_paths

    def find_path(self, current: Point, target: Point, parent_path: Path,
                  path: List[Point]) -> List[Path]:

        path.append(current)
        if current == target:
            return [Path(parent_path, self.field[target].owner, path)]
        paths: List[Path] = []
        for neighbor in self.field.get_neighbors(current):
            if target != neighbor \
                    and (self.field[neighbor].owner != '0'
                         or parent_path.is_point_in_path(neighbor)
                         or neighbor in path):
                continue
            for p in self.find_path(neighbor, target, parent_path, list(path)):
                paths.append(p)
        return paths


f = RectangularField.build_field_from_file('../puzzles/input.txt')
print(f)
solver = PathSolver(f)
solve = solver.solve()

for i in solve:
    p = i
    while p is not None:
        print(p.owner)
        for j in p.path:
            print(j)
        print()
        p = p.parent_path
    print("\n\n")
