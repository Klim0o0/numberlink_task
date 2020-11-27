import argparse
import os
import shutil

from solver import Solver
from fields.hexagonal_field import HexagonalField
from fields.rectangular_field import RectangularField
from saver import Saver
from solve_info import SolveInfo


def parser_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_append_compile = subparsers.add_parser('solve',
                                                  help='select .txt file with puzzle and puzzle type')

    parser_append_compile.set_defaults(function=solve)

    parser_append_compile.add_argument('-t', '--type',
                                       default="rect",
                                       type=str,
                                       help='rect or hex')

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

    parser_append_compile = subparsers.add_parser('solve_saved',
                                                  help='select .txt file with puzzle and puzzle type')

    parser_append_compile.set_defaults(function=solve_load)

    parser_append_compile.add_argument('-s', '--save',
                                       type=str,
                                       help='select save .json file')

    args = parser.parse_args()
    args.function(args)


def solve_load(args):
    solve_indo: SolveInfo = Saver.load(args.save)
    fields = Solver.solve(solve_indo.original_field, solve_indo.max_solve_count, solve_indo.max_line_len,
                          solve_indo.temp_solve, solve_indo.solved_points)

    if len(fields) == 0:
        print('No solves')
    for i in fields:
        paths = i.get_paths()
        for path in paths.keys():
            s = "way for " + str(path) + " : "
            for point in paths[path]:
                s += str(point) + ' '
            print(s)
        print('\n\n')
    pass


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
    fields = Solver.solve(field, args.solve_count, args.line_len)
    if len(fields) == 0:
        print('No solves')
    for i in fields:
        paths = i.get_paths()
        for path in paths.keys():
            s = "way for " + str(path) + " : "
            for point in paths[path]:
                s += str(point) + ' '
            print(s)
        print('\n\n')

    # Saver.delete_saves()


if __name__ == '__main__':
    parser_arguments()
