from typing import List, Tuple, Set, Dict

from numberlink.solve_path import SolvePath
from numberlink.point import Point


class Utils:

    @classmethod
    def get_solved_owners(cls, paths: List[SolvePath]) -> Set[str]:
        if len(paths) == 0:
            return set()
        solved_owners: Set[str] = set()
        path = paths[0]
        while path is not None:
            solved_owners.add(path.owner)
            path = path.parent_path
        return solved_owners

    @classmethod
    def complete_pats(cls, paths_data, parent_pats) -> List[SolvePath]:
        paths: List[SolvePath] = []
        for path_data in paths_data:
            path: SolvePath = SolvePath(parent_pats, path_data['owner'],
                                        cls.ints_list_to_points_list(
                                            path_data['path']))
            for sub_path in cls.complete_pats(path_data['sub_paths'],
                                              path):
                path.add_children_path(sub_path)
            paths.append(path)
        return paths

    @classmethod
    def get_lover_paths(cls, roots: List[SolvePath]) -> List[SolvePath]:
        lover_paths: List[SolvePath] = []
        while len(roots) != 0:
            lover_paths: List[SolvePath] = []
            temp_roots: List[SolvePath] = []
            for root in roots:
                for children in root.children_paths:
                    temp_roots.append(children)
                lover_paths.append(root)
            roots = temp_roots
        return lover_paths

    @classmethod
    def ints_list_to_points_list(cls, points_data: List[Tuple[int, int]]) -> \
            List[Point]:
        points_list: List[Point] = []
        for point_data in points_data:
            points_list.append(Point(point_data[0], point_data[1]))
        return points_list

    @classmethod
    def get_children_paths(cls, root: SolvePath) -> Dict:
        paths_data = {'owner': root.owner,
                      'path': cls.point_list_to_list_int(root.path)}
        paths = []
        for children_paths in root.children_paths:
            paths.append(cls.get_children_paths(children_paths))
        paths_data['sub_paths'] = paths
        return paths_data

    @classmethod
    def get_roots(cls, paths: List[SolvePath]) -> List[SolvePath]:
        roots: List[SolvePath] = []

        while None not in paths:
            parents_paths: List[SolvePath] = []
            roots: List[SolvePath] = []
            for path in paths:
                if path.parent_path not in parents_paths:
                    parents_paths.append(path.parent_path)
                roots.append(path)
            paths = parents_paths
        return roots

    @classmethod
    def point_list_to_list_int(cls, path: List[Point]) \
            -> List[Tuple[int, int]]:
        points: List[Tuple[int, int]] = []
        for point in path:
            points.append((point.x, point.y))
        return points
