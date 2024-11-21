import code
import logging
import re

from .const import State, TableSrc, TableOut, TableLexem
from ...conf import get_global_config


# CH = ""
# S = ""
# B = ""
# CS = State.START
# t: TableOut|None = None
# z = 0

logger = logging.getLogger(__name__)
logging.basicConfig(filename="analyzer.log", level=logging.INFO, filemode="w")

class GC:
    def __init__(self, data: str):
        self.data = data
        self.index = -1
        self.ch: str = ""

    def has_next(self):
        return self.index+1 < len(self.data)

    def is_next_let(self):
        if self.has_next():
            return self.data[self.index+1].isalpha()
        return False

    def is_next_digit(self):
        if self.has_next():
            return self.data[self.index+1].isdigit()
        return False

    def read(self):
        logger.info(f"index: {self.index} of {len(self.data)}")
        self.ch = self.data[self.index]
        self.index += 1

    def next(self):
        logger.info(f"index: {self.index} of {len(self.data)}")
        self.index += 1
        self.ch = self.data[self.index]

    def is_next_has_pattern(self, pattern):
        if self.has_next():
            return re.fullmatch(pattern, self.data[self.index+1])
        return False

    def get_index(self):
        return self.index

    def get_ch(self) -> str:
        return self.ch



# gc: GC|None = None

# def let():
#     return CH.isalpha()
#
# def digit():
#     return CH.isdigit()
#
# def nill():
#     global S
#     S = ""
#
# def add():
#     global S
#     S += CH
#
# def look(t: TableSrc):
#     with open(t.value, 'r', encoding="utf-8") as table_file:
#         for index, line in enumerate(table_file):
#             if S == line:
#                 return index
#
#     return -1
#
# def put(t: TableOut):
#     with open(t.value, 'a+', encoding="utf-8") as table_file:
#         lines = table_file.readlines()
#         for index, line in lines:
#             if S == line:
#                 return index
#         table_file.write(S)
#         return len(lines)
#
# def out(n: TableLexem, k: int):
#     path = f"{get_global_config().OUT_DIR}/lex/lex.txt"
#     with open(path, "a+", encoding="utf-8") as lex:
#         lexem = f"{n.value} {k}\n"
#         lex.write(lexem)




class Reader:
    def __init__(self, code: str):
        self.code = code
        self.gc = GC(code)
        self.state = State.START
        self.buffer = ""
        self.number = ""

    def let(self):
        return self.gc.get_ch().isalpha()

    def digit(self):
        return self.gc.get_ch().isdigit()

    def nill(self):
        self.buffer = ""



    def add(self):
        self.buffer += self.gc.get_ch()
        logger.info(f"buffer: {self.buffer}, ch: {self.gc.get_ch()}")

    def look(self, t: TableSrc):
        logger.info(f"table for look: {t.value}")
        with open(t.value, 'r', encoding="utf-8") as table_file:
            lines = table_file.readlines()
            for i in range(len(lines)):
                line = lines[i].strip()
                logger.info(f"looking: '{line}', buffer: '{self.buffer}'")
                if self.buffer == line:
                    return i
            # for index, line in enumerate(table_file):
            #     if self.buffer == line:
            #         return index
        return -1

    def put(self, t: TableOut):
        def search_in_lines(lines):
            for i in range(len(lines)):
                line = lines[i].strip()
                if self.buffer == line:
                    return i
            return -1

        logger.info("putting...")
        with open(t.value, 'r+', encoding="utf-8") as table_file:
            lines = table_file.readlines()
            in_file = search_in_lines(lines)
            if in_file != -1:
                return in_file
            table_file.write(self.buffer + "\n")
            logger.info(f"file after put {table_file.readlines()}")
        return len(lines)

    def out(self, n: TableLexem, k: int):
        path = f"{get_global_config().OUT_DIR}/lex/lex.txt"
        logger.info(f"out: {n} {k}")
        with open(path, "a+", encoding="utf-8") as lex:
            lexem = f"{n.value} {k}\n"
            lex.write(lexem)
            
    def check_pattern(self, pattern: str):
        return re.fullmatch(pattern, self.gc.get_ch())

    # def white_spaces(self):
    #     return re.fullmatch("\\s", self.gc.get_ch())

class Analyzer:
    def __init__(self, code: str):
        self._code = code

        ## Нужно распознавать вот так же, только итерироваться по токенам
        ## Токены - текст без пробелов в массиве

        self._splitted_code = re.split(r"\s+", code.strip())
        logger.info(f"splitted:\n{'\n'.join(self._splitted_code)}")
        self._reader = Reader(self._splitted_code[0])
        
    def analyze(self) -> State:
        for token in self._splitted_code:
            self._reader = Reader(token)
            logger.info(f"reader: {self._reader.__dict__}")
                #program
            while self._reader.gc.has_next() and self._reader.state != State.ERROR and self._reader.state != State.END:
                self._reader.gc.next()
                #p
                logger.info(f"ch: {self._reader.gc.get_ch()}")

                if (self._reader.let()):
                    self._reader = IdentifierAnalyzer(self._reader).analyze()
                elif self._reader.digit():
                    self._reader = NumberAnalyzer(self._reader).analyze()
                # elif self._reader.gc.get_ch() == '{':
                #     CommentAnalyzer(self._reader).analyze()
                # elif self._reader.gc.get_ch() == '.':
                #     if self._reader.buffer == "end":
                #         self._reader.add()
                #         self._reader.state = State.END
                #     else:
                #         self._reader.state = FloatNumberAnalyzer(self._reader).analyze()
                else:
                    logger.info(f"ch: {self._reader.gc.get_ch()} is delimiter")
                    self._reader = DelimiterAnalyzer(self._reader).analyze()


        return self._reader.state



class SubAnalyzer:
    def __init__(self, reader: Reader):
        self._reader = reader
        self._reader.nill()
        self._reader.add()
        logger.info(f"buffer in {self.__class__} constructor: {self._reader.buffer}")
        logger.info(f"ch in {self.__class__} constructor: {self._reader.gc.get_ch()}")

    def analyze(self):
        pass

class IdentifierAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.IDENTIFIER

        # buffer: p
        # ch: p


    def analyze(self) -> Reader:
        while self._reader.gc.is_next_let() or self._reader.gc.is_next_digit():
            logger.info(f"Identifier ch: {self._reader.gc.get_ch()}")
            self._reader.gc.next()
            self._reader.add()


        logger.info(f"Identifier buffer: {self._reader.buffer}")
        z = self._reader.look(TableSrc.TW)
        logger.info(f"z: {z}")

        if z != -1:
            self._reader.out(TableLexem.TW, z)
        else:
            z = self._reader.look(TableSrc.TL)
            if z != -1:
                self._reader.out(TableLexem.TL, z)
            else:
                z = self._reader.put(TableOut.TI)
                logger.info(f"putted identifier z: {z}")
                self._reader.out(TableLexem.TI, z)

        return self._reader

class NumberAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.NUMBER
    def analyze(self) -> Reader:
        if self._reader.check_pattern("[0-1]"):
            self._reader.state = BinaryNumberAnalyzer(code[self._reader.gc.get_index():]).analyze()
        elif self._reader.check_pattern("[2-7]"):
            self._reader.state = OctNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[8-9]"):
            self._reader.state = DecimalAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[0-9A-Fa-f]"):
            self._reader.state = HexAnalyzer(self._reader).analyze()
        return self._reader


class BinaryNumberAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.check_pattern("[0-1]") and self._reader.gc.has_next():
            self._reader.add()

        if self._reader.check_pattern('[Bb]'):

            if self._reader.gc.read():
                self._reader.add()
                if self._reader.check_pattern('[0-9A-Fa-f]'):
                    self._reader.state = HexAnalyzer(self._reader).analyze()

            self._reader.gc.read()
            self._reader.add()
            if self._reader.check_pattern('[0-9A-Fa-f]'):
                self._reader.state = HexAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[Hh]"):
                pass
            elif self._reader.white_spaces():
                z = self._reader.put(TableOut.TN)
                self._reader.out(TableLexem.TN, z)
            else:
                self._reader.state = State.ERROR
        elif self._reader.check_pattern("[2-7]"):
            self._reader.state = OctNumberAnalyzer(self._reader).analyze()

        elif self._reader.check_pattern("[8-9]"):
            self._reader.state = DecimalAnalyzer(self._reader).analyze()

        elif self._reader.check_pattern("[ACFacf]"):
            self._reader.state = HexAnalyzer(self._reader).analyze()

        elif self._reader.check_pattern('\\.'):
            self._reader.state = FloatNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern('[Ee]'):
            self._reader.state = ExponentAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern('[Oo]'):
            self._reader.number = self._reader.buffer
            pass
        elif self._reader.check_pattern('[Dd]'):
            pass
        elif self._reader.check_pattern('[Hh]'):
            pass
        else:
            self._reader.state = State.ERROR
        return self._reader

class CommentAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.COMMENT
    def analyze(self) -> Reader:
        while self._reader.gc.read() and self._reader.gc.get_ch() != '}':
            pass
        if self._reader.gc.get_ch() != '}':
            self._reader.state = State.ERROR
        self._reader.state = State.COMMENT
        return self._reader

class FloatNumberAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.check_pattern("[0-9]") and self._reader.gc.has_next():
            self._reader.add()
        if self._reader.check_pattern("[Ee]"):
            self._reader.state =  FloatExponentAnalyzer(self._reader).analyze()
        if self._reader.white_spaces():
            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)
        return self._reader

class FloatExponentAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        self._reader.gc.read()
        if self._reader.check_pattern("[+-0-9]"):
            self._analyze()
        else:
            self._reader.state = State.ERROR
        return self._reader

    def _analyze(self):
        self._reader.add()
        while self._reader.check_pattern("[0-9]") and self._reader.gc.has_next():
            self._reader.add()
        if self._reader.white_spaces():
            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)
        else:
            self._reader.state = State.ERROR

class OctNumberAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.gc.is_next_has_pattern("[0-7]"):
            self._reader.gc.next()
            self._reader.add()
        #547545

        if self._reader.gc.has_next():
            self._reader.gc.next()
            if self._reader.check_pattern("[8-9]"):
                self._reader.state = DecimalAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("\\."):
                self._reader.state = FloatNumberAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[Ee]"):
                self._reader.state = ExponentAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[Dd]"):
                self._reader.add()
            elif self._reader.check_pattern("[ACFacf]"):
                self._reader.add()
            elif self._reader.check_pattern("[Hh]"):
                self._reader.add()
            elif self._reader.check_pattern("[Oo]"):
                self._reader.add()
        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)
        return self._reader

class DecimalAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.check_pattern("[0-9]") and self._reader.gc.has_next():
            self._reader.gc.next()
            self._reader.add()

        if self._reader.gc.has_next():
            self._reader.gc.next()
            if self._reader.check_pattern("[Hh]"):
                self._reader.add()
            elif self._reader.check_pattern("[Ee]"):
                self._reader.state = ExponentAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("\\."):
                self._reader.state = FloatNumberAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[ACFacf]"):
                self._reader.state = HexAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[Dd]"):
                self._reader.add()
                self._reader.gc.read()
                if self._reader.check_pattern("[A-Fa-f0-9]"):
                    self._reader.state = HexAnalyzer(self._reader).analyze()
                elif self._reader.check_pattern("[Hh]"):
                    self._reader.add()
            else:
                self._reader.state = State.ERROR

        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        return self._reader

# def analyze(code: str):
#     global CS
#     global gc
#     gc = GC(code)
#     while (CS != State.ERROR or CS != State.END) and gc.read():
#         CS = State.START
#         if let():
#             identifier_state()
#         elif digit():
#             number_state()
#         elif CH=='{':
#             comment_state()
#         elif CH=='.':
#             if S == "end":
#                 add()
#                 CS = State.END
#             float_state()
#         else:
#             delimiter_state()
#     return CS
#

# def identifier_state():
#     global CS
#     CS = State.IDENTIFIER
#     while let() or digit():
#         gc.read()
#     z = look(TableSrc.TW)
#     if z != -1:
#         out(TableLexem.TW, z)
#     else:
#         z = look(TableSrc.TL)
#         if z != -1:
#             out(TableLexem.TL, z)
#         else:
#             z = put(TableOut.TI)
#             out(TableLexem.TI, z)
#
# def number_state():
#     add()
#     global CS
#     CS = State.NUMBER
#     if(re.fullmatch("[0-1]", CH)):
#         binary_state()
#     elif re.fullmatch("[2-7]", CH):
#         oct_state()
#     elif re.fullmatch("[8-9]", CH):
#         dec_state()
#     elif re.fullmatch("[0-9A-Fa-f]", CH):
#         hex_state()

# def binary_state():
#     global CS
#     while re.fullmatch("[0-1]", CH) and gc.read():
#         add()
#     if check_pattern('[Bb]'):
#         gc.read()
#         add()
#         if check_pattern('[0-9A-Fa-f]'):
#             hex_state()
#         elif check_pattern("[Hh]"):
#             pass
#         elif white_spaces():
#             z = put(TableOut.TN)
#             out(TableLexem.TN, z)
#         else:
#             CS = State.ERROR
#
#     elif check_pattern("[2-7]"):
#         oct_state()
#     elif check_pattern("[8-9]"):
#         dec_state()
#     elif check_pattern("[ACFacf]"):
#         hex_state()
#     elif check_pattern('\\.'):
#         float_state()
#     elif check_pattern('[Ee]'):
#         exponent_state()
#     elif check_pattern('[Oo]'):
#         pass
#     elif check_pattern('[Dd]'):
#         pass
#     elif check_pattern('[Hh]'):
#         pass
#     else:
#         CS = State.ERROR

# def oct_state():
#     while re.fullmatch("[0-7]", CH) and gc.read():
#         add()
#     if check_pattern("[8-9]"):
#         dec_state()
#     elif check_pattern("\\."):
#         float_state()
#     elif check_pattern("[Ee]"):
#         exponent_state()
#     elif check_pattern("[Dd]"):
#         add()
#     elif check_pattern("[ACFacf]"):
#         add()
#     elif check_pattern("[Hh]"):
#         add()
#     elif check_pattern("[Oo]"):
#         add()
#
#     gc.read()
#     if white_spaces():
#        z = put(TableOut.TN)
#        out(TableLexem.TN, z)
#     else:
#         global CS
#         CS = State.ERROR

# def dec_state():
#     while re.fullmatch("[0-9]", CH) and gc.read():
#         add()
#     if check_pattern("[Hh]"):
#         add()
#     elif check_pattern("[Ee]"):
#         exponent_state()
#     elif check_pattern("\\."):
#         float_state()
#     elif check_pattern("[ACFacf]"):
#         hex_state()
#     elif check_pattern("[Dd]"):
#         add()
#         gc.read()
#         if check_pattern("[A-Fa-f0-9]"):
#             hex_state()
#         elif check_pattern("[Hh]"):
#             add()
#     gc.read()
#     if white_spaces():
#        z = put(TableOut.TN)
#        out(TableLexem.TN, z)
#     else:
#         global CS
#         CS = State.ERROR


class HexAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.check_pattern("[0-9A-Fa-f]+") and self._reader.gc.has_next():
            self._reader.add()
        if self._reader.check_pattern('[Hh]'):
            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)
        else:
            self._reader.state = State.ERROR
        return self._reader

# def hex_state():
#     while re.fullmatch("[0-9A-Fa-f]+", CH) and gc.read():
#         add()
#     if check_pattern('[Hh]'):
#         z = put(TableOut.TN)
#         out(TableLexem.TN, z)
#     else:
#         global CS
#         CS = State.ERROR


# def float_state():
#     while re.fullmatch("[0-9]", CH) and gc.read():
#         add()
#     if check_pattern("[Ee]"):
#         float_exponent_state()
#     if white_spaces():
#         z = put(TableOut.TN)
#         out(TableLexem.TN, z)

class ExponentAnalyzer(SubAnalyzer):
    def analyze(self) -> Reader:
        self._reader.gc.read()
        if self._reader.check_pattern("[+-]"):
            self._reader.add()
            while self._reader.check_pattern("[0-9]") and self._reader.gc.has_next():
                self._reader.add()
            if self._reader.white_spaces():
                z = self._reader.put(TableOut.TN)
                self._reader.out(TableLexem.TN, z)
            else:
                self._reader.state = State.ERROR
        elif self._reader.check_pattern("[0-9]"):
            while self._reader.check_pattern("[0-9]") and self._reader.gc.has_next():
                self._reader.add()
            if self._reader.check_pattern("[A-Fa-f]"):
                self._reader.state = HexAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[Hh]"):
                self._reader.add()
            if self._reader.white_spaces():
                z = self._reader.put(TableOut.TN)
                self._reader.out(TableLexem.TN, z)
            else:
                self._reader.state = State.ERROR
        elif self._reader.check_pattern("[A-Fa-f]"):
            self._reader.add()
            self._reader.state = HexAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern('[Hh]'):
            self._reader.add()
            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)
        else:
            self._reader.state = State.ERROR
        return self._reader


class DelimiterAnalyzer(SubAnalyzer):
    def analyze(self) -> Reader:
        logger.info(f"delimiter: {self._reader.gc.get_ch()}")
        logger.info(f"delimiter buffer: {self._reader.gc.get_ch()}")
        z = self._reader.look(TableSrc.TL)
        if z != -1:
            self._reader.out(TableLexem.TL, z)
        else:
            self._reader.state = State.ERROR
        return self._reader
# def exponent_state():
#     global CS
#     gc.read()
#     if check_pattern("[+-]"):
#         add()
#         while check_pattern("[0-9]") and gc.read():
#             add()
#         if white_spaces():
#             z = put(TableOut.TN)
#             out(TableLexem.TN, z)
#         else:
#             CS = State.ERROR
#     elif check_pattern("[0-9]"):
#         while check_pattern("[0-9]") and gc.read():
#             add()
#         if check_pattern("[A-Fa-f]"):
#             hex_state()
#         elif check_pattern("[Hh]"):
#             add()
#
#         if white_spaces():
#             z = put(TableOut.TN)
#             out(TableLexem.TN, z)
#         else:
#             CS = State.ERROR
#     elif check_pattern("[A-Fa-f]"):
#         add()
#         hex_state()
#     elif check_pattern('[Hh]'):
#         add()
#         z = put(TableOut.TN)
#         out(TableLexem.TN, z)
#     else:
#         CS = State.ERROR


# def float_exponent_state():
#     global CS
#     gc.read()
#     if check_pattern("[+-]"):
#         add()
#         while check_pattern("[0-9]") and gc.read():
#             add()
#         if white_spaces():
#             z = put(TableOut.TN)
#             out(TableLexem.TN, z)
#         else:
#             CS = State.ERROR
#     if check_pattern("[0-9]"):
#         add()
#         while check_pattern("[0-9]") and gc.read():
#             add()
#         if white_spaces():
#             z = put(TableOut.TN)
#             out(TableLexem.TN, z)
#         else:
#             CS = State.ERROR
#     else:
#         CS = State.ERROR

# def comment_state():
#     while gc.read() and CH != '}':
#         pass

# def delimiter_state():
#     z = look(TableSrc.TL)
#     if z!=-1:
#         out(TableLexem.TL, z)
#     else:
#         global CS
#         CS = State.ERROR

# def check_pattern(pattern: str):
#     return re.fullmatch(pattern, CH)
#
# def white_spaces():
#     return re.fullmatch("\s", CH)



class ReadResult:
    def __init__(self, index: int, state: State):
        self._index = index
        self.state = state
