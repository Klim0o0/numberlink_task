from collections import deque
from numberlink.point import Point


class Solver:

    @staticmethod
    def solve(field_type, field):
        p = [field]
        for i in field.points:
            h = []
            for fi in p:
                Solver.find_path(field_type, field.points[i][0], field.points[i][1], fi,
                                 h)
            p = h
        return Solver.find_correct_solution(field_type, p)

    @staticmethod
    def find_correct_solution(field_type, solution_list):
        for solution in solution_list:
            if Solver.is_correct_solution(solution):
                return solution
        return field_type([])

    @staticmethod
    def is_correct_solution(solution):
        for i in solution.cells:
            for j in i:
                if j == 0:
                    return False
        return True

    @staticmethod
    def find_path(field_type, point_from, point_to, field, p):
        field[point_from] = field[point_to]
        if point_from.x == point_to.x and point_from.y == point_to.y:
            p.append(field)
            return True
        else:
            for point in field.get_neighbors(point_from):
                if field[point] == 0 or point == point_to:
                    Solver.find_path(field_type, point, point_to, field_type(field.cells), p)
