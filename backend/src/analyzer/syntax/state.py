from .reader import LexemReader, LexemTools


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
