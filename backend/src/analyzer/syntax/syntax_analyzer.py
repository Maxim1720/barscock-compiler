import re

from src.analyzer.lexical.const import TableLexem
from src.conf import get_global_config as config
from src.files import read_out, read_res

class LexemReader:
    def __init__(self):
        self._file = open(f"{config().OUT_DIR}/lex/lex.txt")
        self._lexem = None

    def __del__(self):
        self._file.close()

    def read(self):
        line = self._file.readline()

        line = re.split(" ", line)
        line = map(str.strip, line)
        line = list(map(int, line))

        type = line[0]

        lines = []

        if type == TableLexem.TW.value:
            lines = read_res("tw")
        elif type == TableLexem.TL.value:
            lines = read_res("tl")
        elif type == TableLexem.TI.value:
            lines = read_out("ti")
        elif type == TableLexem.TN.value:
            lines = read_out("tn")

        for index, l in enumerate(lines):
            if index == line[1]:
                self._lexem = l
                break


    def readed_lexem(self):
        return self._lexem



class LexemTools:
    def __init__(self, reader: LexemReader):
        self._reader = reader

    def eq(self, s: str):
        return self._reader.readed_lexem() == s

    def is_identifier(self):
        pass

    def is_number(self):
        pass

    def is_bool(self):
        pass

class State:
    def __init__(self, reader: LexemReader):
        self._reader = reader
        self._reader.read()
        self._lexem_tools = LexemTools(self._reader)

    def check(self):
        pass

    def _check_lexem(self, s: str):
        if not self._lexem_tools.eq(s):
            raise SyntaxError(f'expected "{s}" but given {self._reader.readed_lexem()}')

class P(State):
    def check(self):
        self._check_lexem('program')
        D(self._reader).check()
        B(self._reader).check()
        self._check_lexem('.')


class D(State):
    def check(self):
        self._check_lexem('var')
        if self._lexem_tools.is_identifier():
            D1(self._reader).check()

class D1(State):
    def check(self):
        I(self._reader).check()

class B(State):
    def check(self):
        self._check_lexem('begin')
        O(self._reader).check()
        self._check_lexem('end')

class I(State):
    def check(self):
        I1(self._reader).check()
        self._check_lexem(':')
        T(self._reader).check()
        self._check_lexem(";")
class I1(State):
    def check(self):
        I2(self._reader).check()
        if self._check_lexem(','):
            I1(self._reader).check()
            I2(self._reader).check()

class T(State):
    def check(self):
        lt = self._lexem_tools
        if not (lt.eq("int") or lt.eq("float") or lt.eq("bool")):
            raise SyntaxError(self._reader.readed_lexem())

class I2(State):
    def check(self):
        if not self._lexem_tools.is_identifier():
            raise SyntaxError(self._reader.readed_lexem())



class O(State):
    def check(self):
        O1(self._reader).check()
        if self._check_lexem(';'):
            O(self._reader).check()
            O1(self._reader).check()

class O1(State):
    def check(self):
        lt = self._lexem_tools
        r = self._reader
        if lt.eq(":") or lt.eq("\n"):
            r.read()
        elif lt.is_identifier():
            A(r).check()
        elif lt.eq("if"):
            E(self._reader).check()
            r.read()
            self._check_lexem("then")
            O1(self._reader).check()
            r.read()
            if lt.eq("else"):
                O1(self._reader).check()
        elif lt.eq("for"):
            A(r).check()
            self._check_lexem("to")
            r.read()
            E(r).check()
            self._check_lexem("do")
            O1(r).check()
        elif lt.eq("while"):
            E(r).check()
            self._check_lexem("do")
            O1(r).check()
        elif lt.eq("read"):
            self._check_lexem("(")
            I1(r).check()
            self._check_lexem(")")
        elif lt.eq("write"):
            self._check_lexem("(")
            E1(r).check()
            self._check_lexem(")")

class E1(State):
    def check(self):
        E(self._reader).check()
        if self._lexem_tools.eq(","):
            E1(self._reader).check()

class E(State):
    def check(self):
        Z(self._reader).check()
        if Z1.is_(self._lexem_tools):
            Z1(self._reader).check()
            E(self._reader).check()


class Z(State):
    def check(self):
        J(self._reader).check()
        if J1.is_(self._lexem_tools):
            J1(self._reader).check()
            Z(self._reader).check()

class Z1(State):
    def check(self):
        pass
    @staticmethod
    def is_(lt:LexemTools):
        #NE|EQ|LT|LE|GT|GE
        return lt.eq('NE') or lt.eq("EQ") or lt.eq("LT") or lt.eq("GE") or lt.eq("GT") or lt.eq("LE")


class J(State):
    def check(self):
        M(self._reader).check()
        self._reader.read()
        if M1.is_(self._lexem_tools):
            M1(self._reader).check()
            J(self._reader).check()

class M(State):
    def check(self):
        lt = self._lexem_tools
        r = self._reader
        if lt.is_identifier() or lt.is_bool() or lt.is_number():
            pass
        elif lt.eq("~"):
            r.read()
            M(r).check()
        elif lt.eq("("):
            E(r).check()
            r.read()
            self._check_lexem(")")
        else:
            raise SyntaxError(self._reader.readed_lexem())

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
        if not(lt.eq("plus") or lt.eq("min") or lt.eq("or")):
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
        self._lexem_tools.eq("as")
        self._reader.read()
        if not (self._lexem_tools.is_identifier() or self._lexem_tools.is_number() or self._lexem_tools.is_bool()):
            raise SyntaxError(self._reader.readed_lexem())



class SyntaxAnalyzer:
    def __init__(self):
        self._reader = LexemReader()
        self._lexem_tools = LexemTools(self._reader)

    def analyze(self):
        P(self._reader).check()


