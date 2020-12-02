from typing import List


from numberlink.path import Path


class Saver:
    def __init__(self, file: str):
        self.file = file

    def save(self, paths: List[Path]):
