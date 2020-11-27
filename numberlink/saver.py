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
    def save(save_name: str, original_field: Field, fields: List[Field], max_line_len: int, max_solve_cunt: int,
             solved_owners: List[str]):
        data = {}
        data['original_field'] = Saver.convert_cells_to_lists(original_field)
        temp_solves: List[List[List[str]]] = []
        for field in fields:
            temp_solves.append(Saver.convert_cells_to_lists(field))
        data['temp_solve'] = temp_solves
        data['max_line_len'] = max_line_len
        data['max_solve_count'] = max_solve_cunt
        data['field_type'] = str(type(original_field))

        solved: List[str] = []
        for solved_owner in solved_owners:
            solved.append(solved_owner)

        data['solved_owners'] = solved

        with open("saves/save_" + save_name + ".json", "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def convert_cells_to_lists(field: Field) -> List[List[str]]:
        cells = []
        for cells_line in field.cells:
            v = []
            for cell in cells_line:
                json_cell = []
                json_cell.append(cell.owner)
                if cell.previous is not None:
                    json_cell.append([cell.previous.x, cell.previous.y])
                else:
                    json_cell.append([-1, -1])
                if cell.next is not None:
                    json_cell.append([cell.next.x, cell.next.y])
                else:
                    json_cell.append([-1, -1])
                v.append(json_cell)
            cells.append(v)
        return cells

    @staticmethod
    def delete_saves():
        for file in Saver.files('./saves'):
            os.remove('./saves/' + file)

    @staticmethod
    def files(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    @staticmethod
    def load(path: str) -> SolveInfo:
        with open(path, 'r') as file:
            field_type = None
            data = json.load(file)
            if data['field_type'] == "<class 'fields.hexagonal_field.HexagonalField'>":
                field_type = HexagonalField
            else:
                field_type = RectangularField

            original_field = Saver.build_field(field_type, data["original_field"])

            temp_solve: List[Field] = []
            for solve in data['temp_solve']:
                temp_solve.append(Saver.build_field(field_type, solve))
            max_solve_count = data['max_solve_count']
            max_line_len = data['max_line_len']

            solved_points: List[Point] = []
            for owner in data['solved_owners']:
                solved_points.append(owner)

            return SolveInfo(original_field, temp_solve, max_line_len, max_solve_count, solved_points)

    @staticmethod
    def build_field(field_type, json_field) -> Field:
        cells: List[List[Cell]] = []
        for line in json_field:
            cells_line: List[Cell] = []
            for cell in line:
                previous = Point(cell[1][0], cell[1][1])
                next = Point(cell[2][0], cell[2][1])
                if previous.x == -1:
                    previous = None
                if next.x == -1:
                    next = None
                owner = cell[0]
                cells_line.append(Cell(owner, previous, next))
            cells.append(cells_line)
        return field_type(cells)
