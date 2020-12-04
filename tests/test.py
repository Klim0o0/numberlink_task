import unittest
from numberlink.fields.field import Field
from numberlink.fields.hexagonal_field import HexagonalField
from numberlink.fields.rectangular_field import RectangularField
from numberlink.path import Path
from numberlink.point import Point
from numberlink.saver import Saver
from numberlink.solver import Solver


class FieldTests(unittest.TestCase):
    def setUp(self):
        self.field = Field([['1', '0', '0'], ['2', '0', '0'], ['0', '2', '1']])
        self.rectangular_correct_field = RectangularField(
            [['1', '0', '0'], ['2', '0', '0'], ['0', '2', '1']])
        self.rectangular_incorrect_field = RectangularField(
            [['1', '0'], ['2', '0', '0'], ['0', '2', '1']])
        self.hexagonal_correct_field = HexagonalField(
            [['1', '0'], ['0', '0', '0'], ['0', '1']])
        self.hexagonal_incorrect_field = HexagonalField(
            [['1', '0', '0'], ['0', '0', '0'], ['0', '1']])

    def test_point_in(self):
        for x in range(len(self.field.cells)):
            for y in range(len(self.field.cells[x])):
                self.assertTrue(self.field.point_in(Point(x, y)))

    def test_get_by_point(self):
        for x in range(len(self.field.cells)):
            for y in range(len(self.field.cells[x])):
                self.assertEqual(self.field[Point(x, y)],
                                 self.field.cells[x][y])

    def test_points(self):
        self.assertEqual(list(self.field.points.keys()), ['1', '2'])

    def test_hexagonal_correct_field(self):
        self.assertTrue(self.hexagonal_correct_field.is_correct_field())

    def test_rectangular_correct_field(self):
        self.assertTrue(self.rectangular_correct_field.is_correct_field())

    def test_hexagonal_incorrect_field(self):
        self.assertFalse(self.hexagonal_incorrect_field.is_correct_field())

    def test_rectangular_incorrect_field(self):
        self.assertFalse(self.rectangular_incorrect_field.is_correct_field())

    def test_hexagonal_correct_field_to_str(self):
        self.assertEqual(str(self.hexagonal_correct_field),
                         ' 1 0 \n0 0 0 \n 0 1 \n')

    def test_rectangular_correct_field_to_str(self):
        self.assertEqual(str(self.rectangular_correct_field),
                         '1 0 0 \n2 0 0 \n0 2 1 \n')

    def test_field_from_file(self):
        self.assertEqual(str(self.rectangular_correct_field),
                         '1 0 0 \n2 0 0 \n0 2 1 \n')


class PointTests(unittest.TestCase):

    def test_point_init(self):
        point = Point(0, 1)
        self.assertEqual(point.x, 0)
        self.assertEqual(point.y, 1)


class FakeSaver(Saver):
    def __init__(self):
        pass

    def save(self, solver):
        pass


class PathTests(unittest.TestCase):

    def test_path(self):
        path = Path(None, 1, [Point(0, 0)])
        self.assertEqual(str(path), 'way for 1: Point( x = 0 y = 0) \n')


class SolverTests(unittest.TestCase):

    def setUp(self):
        self.rectangular_field_with_solve = RectangularField(
            [['1', '0'], ['1', '0']])
        self.rectangular_field_without_solve = RectangularField(
            [['1', '0'], ['0', '1']])
        self.hexagonal_field_with_solve = HexagonalField(
            [['1', '2'], ['1', '2', '3'], ['3', '0']])
        self.hexagonal_field_without_solve = HexagonalField(
            [['1', '2'], ['0', '2', '1'], ['3', '3']])

    def test_solve_rectangular_solvable_field(self):
        solver = Solver(self.rectangular_field_with_solve, FakeSaver())
        paths = solver.solve()

        self.assertEqual(
            paths[0].path,
            [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)])

    def test_solve_rectangular_unsolvable_field(self):
        solver = Solver(self.rectangular_field_without_solve, FakeSaver())
        paths = solver.solve()

        self.assertEqual(paths, [])

    def test_solve_hexagonal_solvable_field(self):
        solver = Solver(self.hexagonal_field_with_solve, FakeSaver())
        paths = solver.solve()

        self.assertEqual(
            paths[0].path,
            [Point(1, 2), Point(2, 1), Point(2, 0)])

    def test_solve_hexagonal_unsolvable_field(self):
        solver = Solver(self.hexagonal_field_without_solve, FakeSaver())
        paths = solver.solve()

        self.assertEqual(paths, [])


class SaverTests(unittest.TestCase):

    def test_save_load(self):
        saver = Saver('./saves/save_test.json')
        solver = Solver(RectangularField([['1', '1'], ['0', '0']]), saver)
        solver.solve()
        saver.save(solver)
        loaded_saver = saver.load()
        self.assertEqual(solver.field.cells, loaded_saver.field.cells)
        self.assertEqual(len(solver.parent_paths),
                         len(loaded_saver.parent_paths))


if __name__ == '__main__':
    unittest.main()
