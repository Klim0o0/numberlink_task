from collections import deque
from numberlink.point import Point
from numberlink.field import Field, RectangularField
from typing import *


class Solver:

    @staticmethod
    def solve(original_field: Field):
        fields: List[Field] = [original_field]
        for owner in original_field.points:
            temp_fields: List[Field] = []
            for field in fields:
                temp_fields = []
                Solver.find_paths(original_field.points[owner][0],
                                  original_field.points[owner][1], None,
                                  field.copy(), temp_fields)
            fields = temp_fields

        return Solver.find_correct_solves(fields)

    @staticmethod
    def find_paths(current: Point,
                   target: Point,
                   previous: Point,
                   field: Field,
                   fields: List[Field]):

        field[current].owner = field[target].owner

        if previous is not None:
            field[current].previous = previous
            field[previous].next = current

        if current == target:
            fields.append(field)
            return

        for neighbor in field.get_neighbors(current):
            if field[neighbor].owner == '0' or target == neighbor:
                Solver.find_paths(neighbor, target, current,
                                  field.copy(), fields)

    @staticmethod
    def find_correct_solves(fields: [Field]) -> List[Field]:
        correct_solves: List[Field] = []
        for field in fields:
            if Solver.is_correct_solve(field):
                correct_solves.append(field)
        return correct_solves

    @staticmethod
    def is_correct_solve(field: Field):
        for line in field.cells:
            for cell in line:
                if cell.owner == '0':
                    return False
        return True
