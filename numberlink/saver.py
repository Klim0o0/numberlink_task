import json
import os

from fields.field import Field
from fields.rectangular_field import RectangularField
from fields.hexagonal_field import HexagonalField
from solve_info import SolveInfo
from point import Point
from typing import *
from cell import Cell


class Saver:
    @staticmethod
    def save_solve(out_file: str, solve: str):
        if not os.path.exists(os.path.dirname(out_file)):
            os.mkdir(os.path.dirname(out_file))
        with open(out_file, 'w') as file:
            file.write(solve)

    @classmethod
    def save(cls, save_folder, save_name: str, original_field: Field,
             fields: List[Field], max_line_len: int, max_solve_cunt: int,
             solved_owners: List[str]):
        data = {}

        temp_solves: List[List[List[str]]] = []
        for field in fields:
            temp_solves.append(cls.convert_cells_to_lists(field))

        solved: List[str] = []
        for solved_owner in solved_owners:
            solved.append(solved_owner)

        data['original_field'] = cls.convert_cells_to_lists(original_field)
        data['temp_solve'] = temp_solves
        data['max_line_len'] = max_line_len
        data['max_solve_count'] = max_solve_cunt
        data['field_type'] = str(type(original_field))
        data['solved_owners'] = solved

        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        with open(save_folder + '/save_' + save_name + ".json",
                  "w") as write_file:
            json.dump(data, write_file)

    @classmethod
    def convert_cells_to_lists(cls, field: Field):
        cell_lists = []
        for cells_line in field.cells:
            cells = []
            for cell in cells_line:
                json_cell = []
                json_cell.append(cell.owner)
                if cell.previous_point is not None:
                    json_cell.append(
                        [cell.previous_point.x, cell.previous_point.y])
                else:
                    json_cell.append([-1, -1])
                if cell.next_point is not None:
                    json_cell.append([cell.next_point.x, cell.next_point.y])
                else:
                    json_cell.append([-1, -1])
                cells.append(json_cell)
            cell_lists.append(cells)
        return cell_lists

    @classmethod
    def delete_saves(cls, save_folder):
        if os.path.exists(save_folder):
            for file in cls.files(save_folder):
                os.remove(save_folder + '/' + file)

    @classmethod
    def files(cls, path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    @classmethod
    def load(cls, path: str) -> SolveInfo:
        with open(path, 'r') as file:
            field_type = None
            data = json.load(file)
            if data['field_type'] \
                    == "<class 'fields.hexagonal_field.HexagonalField'>":
                field_type = HexagonalField
            else:
                field_type = RectangularField

            temp_solve: List[Field] = []
            solved_points: List[Point] = []
            original_field = cls.build_field(field_type,
                                             data["original_field"])

            for solve in data['temp_solve']:
                temp_solve.append(cls.build_field(field_type, solve))

            max_solve_count = data['max_solve_count']
            max_line_len = data['max_line_len']

            for owner in data['solved_owners']:
                solved_points.append(owner)

            return SolveInfo(original_field, temp_solve, max_line_len,
                             max_solve_count, solved_points)

    @classmethod
    def build_field(cls, field_type, json_field) -> Field:
        cells: List[List[Cell]] = []
        for line in json_field:
            cells_line: List[Cell] = []
            for cell in line:
                previous_point = Point(cell[1][0], cell[1][1])
                next_point = Point(cell[2][0], cell[2][1])
                if previous_point.x == -1:
                    previous_point = None
                if next_point.x == -1:
                    next_point = None
                owner = cell[0]
                cells_line.append(Cell(owner, previous_point, next_point))
            cells.append(cells_line)
        return field_type(cells)
