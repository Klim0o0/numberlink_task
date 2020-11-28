from point import Point
from fields.field import Field
from saver import Saver
from typing import *


class Solver:

    @classmethod
    def solve(cls, saves_folder,
              original_field: Field,
              max_solves_count: int,
              max_line_len: int,
              fields: List[Field] = [],
              solved_owners: List[str] = []):

        save_number = 1
        if len(fields) == 0:
            fields: List[Field] = [original_field]

        for owner in original_field.points:
            if owner in solved_owners:
                continue

            solved_owners.append(owner)
            temp_fields: List[Field] = []
            for field in fields:
                cls.find_paths(original_field.points[owner][0],
                               original_field.points[owner][1], None,
                               field.copy(), max_line_len, 0, temp_fields)

                Saver.save(saves_folder, str(save_number), original_field,
                           temp_fields, max_line_len, max_solves_count,
                           solved_owners)
            save_number += 1
            fields = temp_fields

        return cls.find_correct_solves(fields, max_solves_count)

    @classmethod
    def find_paths(cls, current: Point,
                   target: Point,
                   previous: Point,
                   field: Field,
                   max_len: int,
                   current_len: int,
                   fields: List[Field]):
        if max_len == current_len:
            return

        field[current].owner = field[target].owner
        if previous is not None:
            field[current].previous_point = previous
            field[previous].next_point = current

        if current == target:
            fields.append(field)
            return

        for neighbor in field.get_neighbors(current):
            if field[neighbor].owner == '0' or target == neighbor:
                Solver.find_paths(neighbor, target, current,
                                  field.copy(), max_len, current_len + 1,
                                  fields)

    @classmethod
    def find_correct_solves(cls, fields: [Field],
                            max_solves_count: int) -> List[Field]:
        correct_solves: List[Field] = []
        for field in fields:
            if cls.is_correct_solve(field):
                correct_solves.append(field)
                if len(correct_solves) == max_solves_count:
                    return correct_solves
        return correct_solves

    @classmethod
    def is_correct_solve(cls, field: Field):
        for line in field.cells:
            for cell in line:
                if cell.owner == '0':
                    return False
        return True
