from numberlink.point import Point


class Field:
    def __init__(self, field):
        self.points = {}
        self.field = []
        for x in range(len(field)):
            new_line = []
            for y in range(len(field[0])):
                new_line.append(field[x][y])
                if field[x][y] != 0:
                    if self.points.get(field[x][y]) == None:
                        t = [Point(x, y)]
                        self.points[field[x][y]] = t
                    else:
                        self.points[field[x][y]].append(Point(x, y))

            self.field.append(new_line)

    def get_by_point(self, point):
        return self.field[point.x][point.y]

    def point_in(self, point):
        return 0 <= point.x < len(self.field) \
               and 0 <= point.y < len(self.field[0])

    def set_on_point(self, point, value):
        self.field[point.x][point.y] = value
