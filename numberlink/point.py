class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_neighbors(self):
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) != abs(y):
                    neighbors.append(Point(self.x + x, self.y + y))
        return neighbors

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
