import re

from . import logger
from .const import State, TableSrc, TableOut, TableLexem
from src.conf import get_global_config
from src.files import read_res


class GC2:
    def __init__(self, data: str):
        self.data = data
        self.index = 0
        self.ch: str = data[0]

    def read(self):
        logger.info(f"index: {self.index} of {len(self.data)}")
        self.ch = self.data[self.index]
        self.index += 1
    def has_next(self):
        return self.index < len(self.data)
    def current_is_last(self):
        return self.current_index() == len(self.data) - 1
    def current_index(self):
        return self.index-1

class Reader:
    def __init__(self, code: str):
        self.code = code
        self.gc = GC2(code)
        self.state = State.START
        self.buffer = ""
        self.number = ""

    def let(self):
        return self.gc.ch.isalpha()

    def digit(self):
        return self.gc.ch.isdigit()

    def nill(self):
        self.buffer = ""

    def next(self):
        return self.gc.read()

    def has_next(self):
        return self.gc.has_next()

    def get_ch(self):
        return self.gc.ch

    def current_last(self):
        return self.gc.current_is_last()

    def add(self):
        self.buffer += self.gc.ch
        logger.info(f"buffer: {self.buffer}, ch: {self.gc.ch}")

    def look(self, t: TableSrc):
        logger.info(f"table for look: {t.value}")
        with open(t.value, 'r', encoding="utf-8") as table_file:
            lines = table_file.readlines()
            for i in range(len(lines)):
                if lines[i].isspace():
                    continue
                line = lines[i].strip()
                logger.info(f"looking: '{line}', buffer: '{self.buffer}'")
                if self.buffer == line:
                    return i
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
        return re.fullmatch(pattern, self.gc.ch)

    def is_delimiter(self):
        for l in read_res("tl"):
            if l == self.gc.ch:
                return True
        return False

    # def white_spaces(self):
    #     return re.fullmatch("\\s", self.gc.get_ch())
