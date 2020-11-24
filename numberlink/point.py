class Point:
    def __init__(self, x, y, owner: str = '0'):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point( x = ' + str(self.x) \
               + ' y = ' + str(self.y) + ')'

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
