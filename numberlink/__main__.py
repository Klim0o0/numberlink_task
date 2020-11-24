from numberlink.solver import Solver
from numberlink.field_builder import FieldBuilder
from numberlink.field_saver import FieldSaver
from numberlink.field import HexagonalField
from numberlink.field import RectangularField

if __name__ == '__main__':
    # field = Solver.solve(HexagonalField([[1, 0], [0, 0, 0], [0, 1]]))
    fields = Solver.solve(RectangularField.build_field_from_file(
        "../puzzles/input.txt"))

    print(len(fields))

    for i in fields:
        print(str(i))

    FieldSaver.save(fields, '../solved_puzzles/output.txt')
    # FieldSaver.save(field, "./solved_puzzles/output.txt")
