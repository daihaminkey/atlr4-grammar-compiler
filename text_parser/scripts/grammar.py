from pathlib import Path

from text_parser.utils import calculate_hash


class Grammar:
    def __init__(self, path: Path, root_rule: str):
        if str(path.absolute())[-3:] != '.g4':
            raise NameError(path.absolute())

        self.path = path
        self.name = path.name
        self.hash = calculate_hash(self.path)

        self.root_rule = root_rule
