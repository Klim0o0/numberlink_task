from numberlink.point import Point


class Cell:
    def __init__(self, owner: str, previous: Point = None, next: Point = None):
        self.owner = owner
        self.previous: Point = previous
        self.next: Point = next
