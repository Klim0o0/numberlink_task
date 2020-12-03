from typing import List

from numberlink.fields.field import Field
from numberlink.path import Path
from numberlink.point import Point


class Solver:

    def __init__(self, field: Field, saver):
        self.field: Field = field
        self.max_solve_count = -1
        self.max_line_len = -1
        self.saver = saver
        self.parent_paths: List[Path] = [None]
        self.solved_owners = set()

    def solve(self) -> List[Path]:
        for owner in self.field.points:
            if owner in self.solved_owners:
                continue

            temp_parent_paths: List[Path] = []
            for parent_path in self.parent_paths:
                temp_parent_paths += self.find_path(
                    self.field.points[owner][0],
                    self.field.points[owner][1],
                    parent_path,
                    [])
            self.parent_paths = temp_parent_paths
            self.saver.save(self)
            self.solved_owners.add(owner)
        return self.find_correct_paths(self.parent_paths)

    def find_path(self, current: Point, target: Point, parent_path: Path,
                  path: List[Point]) -> List[Path]:
        path.append(current)

        if len(path) == self.max_line_len:
            return []

        if current == target:
            children_paths = Path(parent_path, self.field[target], path)
            if parent_path is not None:
                parent_path.add_children_path(children_paths)
            return [children_paths]

        paths: List[Path] = []
        for neighbor in self.field.get_neighbors(current):
            if target != neighbor \
                    and (self.field[neighbor] != '0'
                         or (parent_path is not None
                             and parent_path.is_point_in_path(neighbor))
                         or neighbor in path):
                continue
            for current_path in self.find_path(neighbor,
                                               target,
                                               parent_path,
                                               list(path)):
                paths.append(current_path)
        return paths

    def find_correct_paths(self, paths: List[Path]) -> List[Path]:
        correct_paths: List[Path] = []
        for path in paths:
            if len(correct_paths) == self.max_solve_count:
                return correct_paths
            if self.is_correct_path(path):
                correct_paths.append(path)
        return correct_paths

    def is_correct_path(self, path: Path) -> bool:
        count = 0
        while path is not None:
            count += len(path.path)
            path = path.parent_path
        return count == self.field.cells_count
