from collections import deque
from numberlink.point import Point
from numberlink.field import Field


class Solver:

    @staticmethod
    def solve(field):
        p = [field]
        for i in field.points:
            h = []
            for fi in p:
                Solver.find_path(field.points[i][0], field.points[i][1], fi,
                                 h)
            p = h
        return Solver.find_correct_solution(p)

    @staticmethod
    def find_correct_solution(solution_list):
        for solution in solution_list:
            if Solver.is_correct_solution(solution):
                return solution
        return []

    @staticmethod
    def is_correct_solution(solution):
        for i in solution.field:
            for j in i:
                if j == 0:
                    return False
        return True

    @staticmethod
    def find_path(point_from, point_to, field, p):
        field.set_on_point(point_from, field.get_by_point(point_to))
        if point_from.x == point_to.x and point_from.y == point_to.y:
            p.append(field)
            return True
        else:
            for point in point_from.get_neighbors():
                if field.point_in(point) and (
                        field.get_by_point(point) == 0 or point==point_to):
                    Solver.find_path(point, point_to, Field(field.field), p)
