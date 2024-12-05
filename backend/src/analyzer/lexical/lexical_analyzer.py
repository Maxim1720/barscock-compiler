import re

from src.files import write_out
from src.files import read_out
from . import logger
from .const import State, TableSrc, TableOut, TableLexem
from src.analyzer.lexical.sub.number.analyzer import NumberAnalyzer, FloatNumberAnalyzer
from .reader import Reader
from .sub.sub import SubAnalyzer
from .sub.delimiter.analyzer import DelimiterAnalyzer


class Analyzer:
    def __init__(self, code: str):
        self._code = code
        code = code.strip()

        cleaned = False
        while not cleaned:
            cleaned = True
            if "{" in code and "}" in code:
                cleaned = False
                code = f'{code[0:code.index("{")]}{code[code.index("}") + 1:]}'


        self._splitted_code = re.split(r"\s+", code.strip())
        logger.info(f"splitted:\n{'\n'.join(self._splitted_code)}")
        self._reader = Reader(self._splitted_code[0])
    def analyze(self) -> State:
        for token in self._splitted_code:
            #b as b min 5;{123123123 comment}
            comment = False
            if token.startswith("{"):
                comment = True

            while comment:
                for i in token:
                    if i == '}':
                        comment = False
                break
            if comment:
                continue

            self._reader = Reader(token)
            self._reader.next()
            logger.info(f"reader: {self._reader.__dict__}")
            current_token_index = -1
            while not self._reader.get_ch() == "":
                if current_token_index == self._reader.gc.current_index():
                    break
                else:
                    current_token_index = self._reader.gc.current_index()
                logger.info(f"ch: {self._reader.get_ch()}")
                if self._reader.let():
                    self._reader = IdentifierAnalyzer(self._reader).analyze()
                elif self._reader.digit():
                    self._reader = NumberAnalyzer(self._reader).analyze()
                elif self._reader.get_ch() == '{':
                    self._reader = CommentAnalyzer(self._reader).analyze()
                elif self._reader.get_ch() == '.':
                    if self._reader.buffer == "end":
                        self._reader.nill()
                        self._reader = DelimiterAnalyzer(self._reader).analyze()
                        self._reader.state = State.END
                        self._reader.gc.ch = ""
                    else:
                        self._reader = FloatNumberAnalyzer(self._reader).analyze()
                else:
                    logger.info(f"ch: {self._reader.get_ch()} is delimiter")
                    self._reader = DelimiterAnalyzer(self._reader).analyze()
                logger.info(f"STATE: {self._reader.state}")
                if self._reader.state == State.ERROR:
                    return self._reader.state

        return self._reader.state




class IdentifierAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.IDENTIFIER
    def _condition(self):
        return self._reader.let() or self._reader.digit()
    def analyze(self) -> Reader:
        while self._reader.has_next():
            self._reader.next()
            if self._condition():
                self._reader.add()
                if self._reader.current_last():
                    self._reader.gc.ch = ""
            else:
                break
        logger.info(f"Identifier buffer: {self._reader.buffer}")
        z = self._reader.look(TableSrc.TW)
        logger.info(f"z: {z}")
        if z != -1:
            self._reader.out(TableLexem.TW, z)
            if self._reader.buffer not in  read_out("tw"):
                write_out(TableLexem.TW.name.lower(), self._reader.buffer)
        else:
            z = self._reader.look(TableSrc.TL)
            if z != -1:
                self._reader.out(TableLexem.TL, z)
                if self._reader.buffer not in read_out("tl"):
                    write_out(TableLexem.TL.name.lower(), self._reader.buffer)
                from .sub.delimiter.analyzer import counter
                counter += 1
                logger.info(f"delimiter №{counter}: {self._reader.buffer}")
            else:
                z = self._reader.put(TableOut.TI)
                logger.info(f"putted identifier z: {z}")
                self._reader.out(TableLexem.TI, z)
        return self._reader

class CommentAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.COMMENT

    def analyze(self) -> Reader:
        while self._reader.gc.read() and self._reader.get_ch() != '}':
            pass
        if self._reader.get_ch() != '}':
            self._reader.state = State.ERROR
        self._reader.state = State.COMMENT
        return self._reader

class CommentStartAnalyzer(SubAnalyzer):
    def analyze(self) -> Reader:
        pass

class CommentEndAnalyzer(SubAnalyzer):
    def analyze(self) -> Reader:
        pass


