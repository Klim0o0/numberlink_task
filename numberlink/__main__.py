from numberlink.solver import Solver
from numberlink.field_builder import FieldBuilder
from numberlink.field_saver import FieldSaver
from numberlink.field import HexagonalField
from numberlink.field import RectangularField

if __name__ == '__main__':
    field = Solver.solve(HexagonalField, HexagonalField([[1, 0], [0, 0, 0], [0, 1]]))
    #field = Solver.solve(RectangularField,FieldBuilder.build_field_from_file(RectangularField,"puzzles/input.txt"))
    FieldSaver.save(field, "./solved_puzzles/output.txt")
    print(field.cells)
