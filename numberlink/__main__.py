import argparse
import os
import shutil

from solver import Solver
from fields.hexagonal_field import HexagonalField
from fields.field import Field
from fields.rectangular_field import RectangularField
from saver import Saver
from solve_info import SolveInfo
from typing import *


def parser_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_append_compile = subparsers.add_parser('solve',
                                                  help='select .txt file'
                                                       ' with puzzle'
                                                       ' and puzzle type')

    parser_append_compile.set_defaults(function=solve)

    parser_append_compile.add_argument('-t', '--type',
                                       default="rect",
                                       type=str,
                                       help='rect or hex')

    parser_append_compile.add_argument('-o', '--out_file',
                                       default='./solved_puzzles/output.txt',
                                       type=str,
                                       help='select output file')

    parser_append_compile.add_argument('-p', '--puzzle',
                                       default="./puzzles/input.txt",
                                       type=str,
                                       help='select .txt file')

    parser_append_compile.add_argument('-c', '--solve_count',
                                       default=-1,
                                       type=int,
                                       help='max solve count')

    parser_append_compile.add_argument('-l', '--line_len',
                                       default=-1,
                                       type=int,
                                       help='max line len')
    parser_append_compile.add_argument('-f', '--saves_folder',
                                       default='./saves',
                                       type=str,
                                       help='select folder for saves')

    parser_append_compile = subparsers.add_parser('solve_saved',
                                                  help='select .json '
                                                       'save file')

    parser_append_compile.set_defaults(function=solve_load)

    parser_append_compile.add_argument('-s', '--save',
                                       type=str,
                                       help='select save .json file')

    parser_append_compile.add_argument('-o', '--out_file',
                                       default='./solved_puzzles/output.txt',
                                       type=str,
                                       help='select output file')

    parser_append_compile.add_argument('-f', '--saves_folder',
                                       default='./saves',
                                       type=str,
                                       help='select folder for saves')
    args = parser.parse_args()
    args.function(args)


def solve(args):
    field = None
    if args.type == 'rect':
        field = RectangularField.build_field_from_file(args.puzzle)
    if args.type == 'hex':
        field = HexagonalField.build_field_from_file(args.puzzle)

    if field is None:
        print("Not correct input")
        return

    print(field)
    fields = Solver.solve(args.saves_folder, field, args.solve_count,
                          args.line_len)
    solve_str = get_solve_str(fields)
    print(solve_str)
    Saver.save_solve(args.out_file, solve_str)


def solve_load(args):
    solve_info: SolveInfo = Saver.load(args.save)
    fields = Solver.solve(args.saves_folder, solve_info.original_field,
                          solve_info.max_solve_count, solve_info.max_line_len,
                          solve_info.temp_solve, solve_info.solved_points)
    solve_str = get_solve_str(fields)
    print(solve_str)
    Saver.save_solve(args.out_file, solve_str)


def get_solve_str(fields: List[Field]) -> str:
    solve_str = ''
    if len(fields) == 0:
        return 'No solves'
    for i in range(len(fields)):
        paths = fields[i].get_paths()
        solve_str += 'Solve # ' + str(i + 1) + '\n'
        for path in paths.keys():
            solve_str += 'way for ' + str(path) + ' : '
            for point in paths[path]:
                solve_str += str(point) + ' '
            solve_str += '\n'
        solve_str += '\n\n'
    return solve_str


if __name__ == '__main__':
    parser_arguments()
