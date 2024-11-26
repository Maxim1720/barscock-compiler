from src.files import read_res
from src.analyzer.lexical.const import TableLexem

class LexemReader:
    def __init__(self, lexem_table: list[list[int]]):
        self._lexem = None
        self._index = 0
        self._lexemes = lexem_table
        self._readed = []

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