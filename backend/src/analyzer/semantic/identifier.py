import re

from src import debug
from src.analyzer.syntax.exceptions import UnknownIdentifierError
from src.analyzer.syntax.identifiers import founded


class IdentifierChecker:
    def __init__(self, name):
        self.name = name

    def exists(self):
        if debug:
            print(f"founded to check: {founded}")
        if self.name in [i.name for i in founded]:
            return True
        return False


class IdChecker:
    def __init__(self, i1):
        self.i1 = i1

    def check(self):
        ids = re.split(",", self.i1)
        if debug:
            print(f"ids in read: {ids}")
        for i in ids:
            if not IdentifierChecker(i).exists():
                raise UnknownIdentifierError(f"Identifier '{i}' not defined")

class AssignmentChecker:
    def check(self, i, e):
        need_type = e
        IdChecker(i).check()

        id = None
        for ii in founded:
            if ii.name == i:
                id = ii
                break

        if id.type != need_type:
            raise TypeError(f"Type error: {id.type} != {need_type} at identifier '{id.name}'")

