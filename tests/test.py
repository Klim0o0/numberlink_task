import unittest
from numberlink.fields.field import Field
from numberlink.fields.hexagonal_field import HexagonalField
from numberlink.fields.rectangular_field import RectangularField
from numberlink.point import Point
from numberlink.saver import Saver
from numberlink.solver import Solver


class FieldTests(unittest.TestCase):
    def setUp(self):
        self.field = Field([['1', '0', '0'], ['2', '0', '0'], ['0', '2', '1']])

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


class SolverTests(unittest.TestCase):

    def setUp(self):
        self.field_with_solve = RectangularField([['1', '0'], ['1', '0']])
        self.field_without_solve = RectangularField([['1', '0'], ['0', '1']])

    def test_solve_solvable(self):
        solver = Solver(self.field_with_solve, FakeSaver())
        paths = solver.solve()

        self.assertEqual(
            paths[0].path,
            [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)])

    def test_solve_unsolvable(self):
        solver = Solver(self.field_without_solve, FakeSaver())
        paths = solver.solve()

        self.assertEqual(paths, [])


if __name__ == '__main__':
    unittest.main()
