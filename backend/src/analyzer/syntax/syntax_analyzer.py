from src.analyzer.symantic.analyzer.identifier import IdentifiersAnalyzer
from src.analyzer.syntax.expression import E
from src.analyzer.syntax.identifier import I2, A
from src.analyzer.syntax.reader import LexemReader, LexemTools
from src.analyzer.syntax.state import State


class P(State):
    def check(self):
        IdentifiersAnalyzer().analyze()
        self._lexem_must_be('program')
        self._reader.read()
        self._reader = D(self._reader).check()
        self._reader = B(self._reader).check()
        self._reader.read()
        self._lexem_must_be('.')
        return self._reader


class D(State):
    def check(self):
        self._lexem_must_be('var')
        self._reader.read()
        if self._lexem_tools.is_identifier():
            return D1(self._reader).check()
        return self._reader


class D1(State):
    def check(self):
        self._reader = I(self._reader).check()
        if self.eq(";"):
            self._reader.read()
            if self.is_identifier():
                return D1(self._reader).check()
            return self._reader


class B(State):
    def check(self):
        self._lexem_must_be('begin')
        self._reader.read()
        self._reader = O(self._reader).check()
        self._lexem_must_be('end')
        return self._reader


class I(State):
    def check(self):
        self._reader = I1(self._reader).check()
        self._lexem_must_be(':')
        self._reader.read()
        self._reader = T(self._reader).check()
        self._reader.read()
        self._lexem_must_be(";")
        return self._reader


class I1(State):
    def check(self):
        self._reader = I2(self._reader).check()
        self._reader.read()
        if self.eq(','):
            self._reader.read()
            self._reader = I1(self._reader).check()
            # self._reader = I2(self._reader).check()
        return self._reader


class T(State):
    def check(self):
        if not (self.eq("int") or self.eq("float") or self.eq("bool")):
            raise SyntaxError(f"expected int|float|bool, given '{self._reader.readed_lexem()}'")
        return self._reader





class O(State):
    def check(self):
        self._reader = O1(self._reader).check()
        if self.eq(';'):
            self._reader.read()
            self._reader = O(self._reader).check()
        return self._reader


class O1(State):
    def check(self):
        if self.is_identifier():
            self._reader = I2(self._reader).check()
            self._reader.read()
            self._reader = A(self._reader).check()
        elif self.eq("if"):
            self._reader._readed = []
            self._reader.read()
            self._reader = E(self._reader).check()
            if self._reader.get_type() != 'bool':
                raise TypeError(f"expected bool, got {self._reader.get_type()}")
            self._lexem_must_be("then")
            self._reader.read()
            self._reader = O1(self._reader).check()
            if self.eq("else"):
                self._reader.read()
                self._reader = O1(self._reader).check()

        elif self.eq("for"):
            self._reader.read()
            self._reader = I2(self._reader).check()
            self._reader.read()
            self._reader = A(self._reader).check()
            type = self._reader.get_type()
            self._lexem_must_be("to")
            self._reader._readed = []
            self._reader.read()
            self._reader = E(self._reader).check()
            if type != self._reader.get_type():
                raise TypeError(f"expected {type}, got {self._reader.get_type()}")
            self._lexem_must_be("do")
            self._reader.read()
            self._reader = O1(self._reader).check()

        elif self.eq("while"):
            self._reader._readed = []
            self._reader.read()
            self._reader = E(self._reader).check()
            if self._reader.get_type() != 'bool':
                raise TypeError(f"expected bool, got {self._reader.get_type()}")
            self._lexem_must_be("do")
            self._reader._readed = []
            self._reader.read()
            self._reader = O1(self._reader).check()
        elif self.eq("read"):
            self._reader.read()
            self._lexem_must_be("(")
            self._reader.read()
            self._reader = I1(self._reader).check()
            self._lexem_must_be(")")
            self._reader.read()

        elif self.eq("write"):
            self._reader.read()
            self._lexem_must_be("(")
            self._reader._readed = []
            self._reader.read()
            self._reader = E1(self._reader).check()
            self._lexem_must_be(")")
            self._reader.read()
        else:
            raise SyntaxError(f"unexpected {self._reader.readed_lexem()}")

        if self.eq(":") or self.eq("\n"):
            self._reader.read()
            self._reader = O1(self._reader).check()

        return self._reader


class E1(State):
    def check(self):

        # начать запоминать типчики
        # self._reader._readed = []
        self._reader = E(self._reader).check()
        if self.eq(","):
            return E1(self._reader).check()
        return self._reader






class L(State):
    def check(self):
        lt = self._lexem_tools
        if not (lt.eq("true") or lt.eq("false")):
            raise SyntaxError("expected 'true' or 'false'")




class SyntaxAnalyzer:
    def __init__(self, lexem_table: list[list[int]]):
        self._reader = LexemReader(lexem_table)
        self._lexem_tools = LexemTools(self._reader)

    def analyze(self):
        self._reader.read()
        P(self._reader).check()
