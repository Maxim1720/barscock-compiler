import re

from src.files import read_res
from src.analyzer.syntax.reader import LexemReader


class LexemTools:
    def __init__(self, reader: LexemReader):
        self._reader = reader

    def eq(self, s: str):
        return self._reader.readed_lexem() == s

    def is_identifier(self):
        for i in read_res("ti"):
            if i == self._reader.readed_lexem():
                return True
        return False

    def is_number(self):
        for i in read_res("tn"):
            if i == self._reader.readed_lexem():
                return True
        return False

    def is_bool(self):
        return self._reader.readed_lexem() == "true" or self._reader.readed_lexem() == "false"


class State:
    def __init__(self, reader: LexemReader):
        self._reader = reader
        # self._reader.read()
        self._lexem_tools = LexemTools(self._reader)

    def check(self) -> LexemReader:
        pass

    def _lexem_must_be(self, s: str):
        if not self.eq(s):
            raise SyntaxError(f'expected "{s}" but given {self._reader.readed_lexem()}')
        return True

    def eq(self, s: str):
        return LexemTools(self._reader).eq(s)

    def is_identifier(self):
        return LexemTools(self._reader).is_identifier()

    def is_number(self):
        return LexemTools(self._reader).is_number()

    def is_bool(self):
        return LexemTools(self._reader).is_bool()

class P(State):
    def check(self):
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


class I2(State):
    def check(self):
        if not self._lexem_tools.is_identifier():
            raise SyntaxError(self._reader.readed_lexem())
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
        lex = self._reader.readed_lexem()

        if self.is_identifier():
            self._reader.read()
            self._reader = A(self._reader).check()
        elif self.eq("if"):
            self._reader.read()
            self._reader = E(self._reader).check()
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
            self._lexem_must_be("to")
            self._reader.read()
            self._reader = E(self._reader).check()
            self._lexem_must_be("do")
            self._reader.read()
            self._reader = O1(self._reader).check()

        elif self.eq("while"):
            self._reader = E(self._reader).check()
            self._lexem_must_be("do")
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
        self._reader = E(self._reader).check()
        if self.eq(","):
            return E1(self._reader).check()
        return self._reader

class E(State):
    def check(self):
        self._reader = Z(self._reader).check()
        self._reader.read()
        if Z1.is_(LexemTools(self._reader)):
            self._reader = Z1(self._reader).check()
            self._reader = E(self._reader).check()
        return self._reader


class Z(State):
    def check(self):
        self._reader = J(self._reader).check()
        if J1.is_(LexemTools(self._reader)):
            self._reader = J1(self._reader).check()
            self._reader = Z(self._reader).check()
        return self._reader

class Z1(State):
    def check(self):
        if not self.is_(LexemTools(self._reader)):
            raise SyntaxError(f"unexpected {self._reader.readed_lexem()}")
        self._reader.read()
        return self._reader

    @staticmethod
    def is_(lt: LexemTools):
        #NE|EQ|LT|LE|GT|GE
        return lt.eq('NE') or lt.eq("EQ") or lt.eq("LT") or lt.eq("GE") or lt.eq("GT") or lt.eq("LE")


class J(State):
    def check(self):
        self._reader = M(self._reader).check()
        self._reader.read()
        if M1.is_(LexemTools(self._reader)):
            self._reader = M1(self._reader).check()
            self._reader = J(self._reader).check()
        return self._reader


class M(State):
    def check(self):
        if self.is_identifier():
            self._reader = I2(self._reader).check()
            # self._reader.read()
        elif self.is_bool() or self.is_number():
            self._reader.read()
        elif self.eq("~"):
            self._reader.read()
            M(self._reader).check()
        elif self.eq("("):
            E(self._reader).check()
            self._reader.read()
            self._lexem_must_be(")")
        else:
            raise SyntaxError(self._reader.readed_lexem())
        return self._reader


class M1(State):
    def check(self):
        lt = self._lexem_tools
        if not (lt.eq("mult") or lt.eq("div") or lt.eq("and")):
            raise SyntaxError("expected 'mult', 'div' or 'and'")

    @staticmethod
    def is_(lt: LexemTools):
        return lt.eq("mult") or lt.eq("div") or lt.eq("and")


class J1(State):
    def check(self):
        lt = self._lexem_tools
        if not (lt.eq("plus") or lt.eq("min") or lt.eq("or")):
            raise SyntaxError(self._reader.readed_lexem())

    @staticmethod
    def is_(lt: LexemTools):
        return lt.eq("plus") or lt.eq("min") or lt.eq("or")


class L(State):
    def check(self):
        lt = self._lexem_tools
        if not (lt.eq("true") or lt.eq("false")):
            raise SyntaxError("expected 'true' or 'false'")


class A(State):
    def check(self):
        self._lexem_must_be("as")
        self._reader.read()
        if not (self._lexem_tools.is_identifier() or self._lexem_tools.is_number() or self._lexem_tools.is_bool()):
            raise SyntaxError(f"unexpected  '{self._reader.readed_lexem()}'")
        return self._reader


class SyntaxAnalyzer:
    def __init__(self, lexem_table: list[list[int]]):
        self._reader = LexemReader(lexem_table)
        self._lexem_tools = LexemTools(self._reader)

    def analyze(self):
        self._reader.read()
        P(self._reader).check()
