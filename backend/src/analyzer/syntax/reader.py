from src.files import read_res
from src.analyzer.lexical.const import TableLexem



class LexemReader:
    def __init__(self, lexem_table: list[list[int]]):
        self._lexem = None
        self._index = 0
        self._lexemes = lexem_table
        self._readed = []
        self._type = None

    def read(self):
        if not self.has_next():
            return False
        line = self._lexemes[self._index]
        read_dict = {
                TableLexem.TW.value: lambda : read_res('tw'),
                TableLexem.TL.value: lambda : read_res('tl'),
                TableLexem.TI.value: lambda : read_res('ti'),
                TableLexem.TN.value: lambda : read_res('tn'),
        }
        lines = read_dict[line[0]]()
        for index, l in enumerate(lines):
            if index == line[1]:
                self._lexem = l
                self._readed.append(l)
                break
        self._index += 1

    def readed_lexem(self):
        return self._lexem

    def has_next(self):
        return self._index < len(self._lexemes)

    def readed_lexemes(self) -> list[str]:
        return self._readed

    def set_type(self, type: str):
        self._type = type

    def get_type(self):
        return self._type

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