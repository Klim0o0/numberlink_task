from typing import List

from numberlink.point import Point


class SolvePath:
    def __init__(self, parent_path, owner: str, path: List[Point]):
        self.parent_path = parent_path
        self.owner = owner
        self.path = path
        self.children_paths = []

    def add_children_path(self, path):
        self.children_paths.append(path)

    def is_point_in_path(self, point: Point) -> bool:
        if point in self.path:
            return True
        if self.parent_path is not None \
                and self.parent_path.is_point_in_path(point):
            return True
        return False

    def __str__(self):
        path_str: List[str] = []
        path = self
        while path is not None:
            path_str.append('way for ' + str(path.owner) + ': ')
            for point in path.path:
                path_str.append(str(point) + ' ')
            path_str.append('\n')
            path = path.parent_path
        return ''.join(path_str)
