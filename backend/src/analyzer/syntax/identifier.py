from src.analyzer.syntax.state import State


class A(State):
    def check(self):
        from src.analyzer.syntax.expression import E
        self._lexem_must_be("as")
        self._reader._readed = []
        self._reader.read()
        if not (self._lexem_tools.is_identifier() or self._lexem_tools.is_number() or self._lexem_tools.is_bool()):
            raise SyntaxError(f"unexpected  '{self._reader.readed_lexem()}'")
        else:
            self._reader = E(self._reader).check()
        return self._reader


class I2(State):
    def check(self):
        from src.analyzer.symantic.analyzer.identifier import IdentifiersExistsAnalyzer, IdentifierAssignTypesAnalyzer
        if not self._lexem_tools.is_identifier():
            raise SyntaxError(self._reader.readed_lexem())
        IdentifiersExistsAnalyzer(self._reader).analyze()
        # self._reader._readed = []
        IdentifierAssignTypesAnalyzer(self._reader).analyze()
        return self._reader