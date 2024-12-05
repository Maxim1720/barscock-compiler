from .identifier import I2
from .reader import LexemTools
from .state import State
from ..symantic.analyzer.type import TypesAnalyzer


class E(State):
    def check(self):

        self._reader = Z(self._reader).check()
        if Z1.is_(LexemTools(self._reader)):
            self._reader = Z1(self._reader).check()
            self._reader = E(self._reader).check()
        self._reader._readed = self._reader._readed[:-1]
        type = TypesAnalyzer(self._reader).analyze()
        if type is not None:
            self._reader.set_type(type)
        self._reader._readed = []
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
        if M1.is_(LexemTools(self._reader)):
            self._reader = M1(self._reader).check()
            self._reader = J(self._reader).check()
        return self._reader


class M(State):
    def check(self):
        if self.is_identifier():
            # проверить, что идентификатор существует
            self._reader = I2(self._reader).check()
            self._reader.read()
        elif self.is_bool() or self.is_number():
            self._reader.read()
        elif self.eq("~"):
            self._reader.read()
            self._reader = M(self._reader).check()
        elif self.eq("("):
            self._reader = E(self._reader).check()
            self._lexem_must_be(")")
        else:
            raise SyntaxError(self._reader.readed_lexem())
        return self._reader


class M1(State):
    def check(self):
        lt = self._lexem_tools
        if not (lt.eq("mult") or lt.eq("div") or lt.eq("and")):
            raise SyntaxError("expected 'mult', 'div' or 'and'")
        self._reader.read()
        return self._reader

    @staticmethod
    def is_(lt: LexemTools):
        return lt.eq("mult") or lt.eq("div") or lt.eq("and")


class J1(State):
    def check(self):
        lt = LexemTools(self._reader)
        if not (lt.eq("plus") or lt.eq("min") or lt.eq("or")):
            raise SyntaxError(self._reader.readed_lexem())
        self._reader.read()
        return self._reader

    @staticmethod
    def is_(lt: LexemTools):
        return lt.eq("plus") or lt.eq("min") or lt.eq("or")