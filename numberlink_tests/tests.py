import unittest
from numberlink.field import Field
from numberlink.point import Point
from numberlink.solver import Solver


class FieldTests(unittest.TestCase):
    def setUp(self):
        self.field = Field([[1, 0, 0], [2, 0, 0], [0, 2, 1]])
        self.w = 3
        self.h = 3

    def test_point_in(self):
        for x in range(self.w):
            for y in range(self.h):
                self.assertTrue(self.field.point_in(Point(x, y)))

    def test_get_by_point(self):
        for x in range(self.w):
            for y in range(self.h):
                self.assertEqual(self.field.get_by_point(Point(x, y)),
                                 self.field.field[x][y])

    def test_set_on_point(self):
        for x in range(self.w):
            for y in range(self.h):
                self.field.set_on_point(Point(x, y), 3)
                self.assertEqual(self.field.field[x][y], 3)

    def test_points(self):
        self.assertEqual(list(self.field.points.keys()), [1, 2])


class PointTests(unittest.TestCase):

    def test_point_init(self):
        point = Point(0, 1)
        self.assertEqual(point.x, 0)
        self.assertEqual(point.y, 1)

    def test_get_neighbors(self):
        point = Point(0, 1)
        for i in point.get_neighbors():
            self.assertTrue(
                i in [Point(0, 0), Point(-1, 1), Point(1, 1), Point(0, 2)])


class SolverTests(unittest.TestCase):

    def test_solve_unsolvable(self):
        self.assertEqual(
            Solver.solve(Field([[1, 0, 0], [2, 0, 0], [0, 2, 1]])),
            [])

    def test_solve_solvable(self):
        self.assertEqual(
            Solver.solve(Field([[1, 2, 0], [0, 0, 0], [1, 0, 2]])).field,
            [[1, 2, 2], [1, 1, 2], [1, 1, 2]])


if __name__ == '__main__':
    unittest.main()
