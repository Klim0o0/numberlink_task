from point import Point


class Cell:
    def __init__(self,
                 owner: str,
                 previous_point: Point = None,
                 next_point: Point = None):
        self.owner = owner
        self.previous_point: Point = previous_point
        self.next_point: Point = next_point
