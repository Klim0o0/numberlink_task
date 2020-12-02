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
