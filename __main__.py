from numberlink.solver import Solver
from numberlink.field_builder import FieldBuilder
from numberlink.field_saver import FieldSaver

if __name__ == '__main__':
    field = Solver.solve(FieldBuilder.build_field_from_file("puzzles/input.txt"))
    FieldSaver.save(field,"solved_puzzles/output.txt")
    print(field.field)
