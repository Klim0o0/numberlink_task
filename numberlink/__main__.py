import argparse
import sys
from typing import List

from numberlink.saver import Saver
from numberlink.solver import Solver
from numberlink.fields.hexagonal_field import HexagonalField
from numberlink.fields.rectangular_field import RectangularField

from numberlink.solve_path import SolvePath


def parser_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_append_compile = subparsers.add_parser('solve',
                                                  help='select .txt file'
                                                       ' with puzzle'
                                                       ' and puzzle type')

    parser_append_compile.set_defaults(function=solve)

    parser_append_compile.add_argument('puzzle',
                                       default="./puzzles/input.txt",
                                       type=str,
                                       help='select .txt file')

    parser_append_compile.add_argument('type',
                                       default="rect",
                                       type=str,
                                       help='rect or hex')

    parser_append_compile.add_argument('-o', '--out_file',
                                       default='./solved_puzzles/output.txt',
                                       type=str,
                                       help='select output file')

    parser_append_compile.add_argument('-c', '--solve_count',
                                       default=-1,
                                       type=int,
                                       help='max solve count')

    parser_append_compile.add_argument('-l', '--line_len',
                                       default=-1,
                                       type=int,
                                       help='max line len')
    parser_append_compile.add_argument('-f', '--save_file',
                                       default='./saves/save.json',
                                       type=str,
                                       help='select folder for saves')

    parser_append_compile = subparsers.add_parser('solve_saved',
                                                  help='select .json '
                                                       'save file')

    parser_append_compile.set_defaults(function=solve_load)

    parser_append_compile.add_argument('save',
                                       type=str,
                                       help='select save .json file')

    parser_append_compile.add_argument('-o', '--out_file',
                                       default='./solved_puzzles/output.txt',
                                       type=str,
                                       help='select output file')

    parser_append_compile.add_argument('-f', '--save_file',
                                       default='./saves/save.json',
                                       type=str,
                                       help='select folder for saves')
    args = parser.parse_args()
    if not hasattr(args, 'function'):
        print('Error: Select solve/solve_saved')
        sys.exit(1)

    try:
        args.function(args)
    except KeyboardInterrupt:
        print('Interrupt solve')
    except Exception:
        print('Not valid parameters')


def solve(args):
    if args.type == 'rect':
        field = RectangularField.build_field_from_file(args.puzzle)
    elif args.type == 'hex':
        field = HexagonalField.build_field_from_file(args.puzzle)
    else:
        print("Not correct field type")
        return

    if field is None:
        print("Not correct input")
        return

    solver = Solver(field, Saver(args.save_file))
    paths: List[SolvePath] = solver.solve()
    solve_str: str = get_solve_str(field, paths)
    print(solve_str)
    Saver.save_solve(solve_str, args.out_file)


def solve_load(args):
    saver = Saver(args.saves_folder)
    solver = saver.load()
    paths: List[SolvePath] = solver.solve()
    solve_str: str = get_solve_str(solver.field, paths)
    print(solve_str)
    Saver.save_solve(solve_str, args.out_file)


def get_solve_str(original_field, fields: List[SolvePath]) -> str:
    solve_str = [str(original_field) + '\n\n']
    if len(fields) == 0:
        return 'No solves'

    for i in range(len(fields)):
        path = fields[i]
        solve_str.append('Solve # ' + str(i + 1) + '\n' + str(path) + '\n')
    return ''.join(solve_str)


if __name__ == '__main__':
    parser_arguments()
