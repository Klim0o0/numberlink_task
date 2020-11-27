from fields.field import Field
from typing import *


class SolveInfo:
    def __init__(self, original_field: Field, temp_solve: List[Field], max_line_len: int, max_solve_count: int,
                 solved_points: List[str]):
        self.original_field = original_field
        self.temp_solve = temp_solve
        self.max_line_len = max_line_len
        self.max_solve_count = max_solve_count
        self.solved_points = solved_points
