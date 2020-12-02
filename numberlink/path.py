from typing import List

from numberlink.point import Point


class Path:
    def __init__(self, parent_path, owner: str, path: List[Point]):
        self.parent_path = parent_path
        self.owner = owner
        self.path = path

    def is_point_in_path(self, point: Point):
        if point in self.path:
            return True
        if self.parent_path is not None \
                and self.parent_path.is_point_in_path(point):
            return True
        return False

    def __str__(self):
        path_str = ''
        path = self
        while path is not None:
            path_str += 'way for ' + str(path.owner) + ": "
            for point in path.path:
                path_str += str(point) + ' '
            path_str += '\n'
            path = path.parent_path
        return path_str
