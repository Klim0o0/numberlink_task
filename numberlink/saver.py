import json
import os
from typing import List
from numberlink.fields.field import Field
from numberlink.fields.rectangular_field import RectangularField
from numberlink.fields.hexagonal_field import HexagonalField
from numberlink.path import Path
from numberlink.solver import Solver
from numberlink.utils import Utils


class Saver:
    def __init__(self, file: str):
        self.file = file
        self.i = 1

    def save(self, solver):
        paths: List[Path] = solver.parent_paths
        field: Field = solver.field
        max_line_len = solver.max_line_len
        max_solve_count = solver.max_solve_count

        data = {}
        paths_data = []
        roots = Utils.get_roots(paths)
        for root in roots:
            paths_data.append(Utils.get_children_paths(root))
        data['field'] = field.cells
        data['field_type'] = type(field).__name__
        data['max_solve_count'] = max_solve_count
        data['max_line_len'] = max_line_len
        data['paths'] = paths_data

        if not os.path.exists(self.file):
            os.mkdir(os.path.dirname(self.file))

        with open(self.file, 'w') as file:
            json.dump(data, file)

    def load(self):
        with open(self.file, 'r') as file:
            data = json.load(file)
        max_line_len: int = data['max_line_len']
        max_solve_count: int = data['max_solve_count']
        field_type = data['field_type']
        if field_type == 'RectangularField':
            field = RectangularField(data['field'])
        else:
            field = HexagonalField(data['field'])
        paths = Utils.get_lover_paths(Utils.complete_pats(data['paths'], None))
        solver = Solver(field, self)
        solver.max_solve_count = max_solve_count
        solver.max_line_len = max_line_len
        solver.parent_paths = paths
        solver.solved_owners = Utils.get_solved_owners(paths)
        return solver

    @staticmethod
    def save_solve(solve: str, file_path: str):
        if not os.path.exists(file_path):
            os.mkdir(os.path.dirname(file_path))
        with open(file_path, 'w') as file:
            file.write(solve)
