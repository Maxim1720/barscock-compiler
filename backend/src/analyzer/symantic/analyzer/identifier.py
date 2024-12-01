from src.analyzer.syntax.tools import lex_table_from_file
from src.analyzer.syntax.reader import LexemReader
from src.conf import get_global_config
from src.analyzer.symantic.files import create_ti, get_identifiers_from_file
from src.analyzer.symantic.types import FoundedIdentifier


class IdentifiersAnalyzer:
    def __init__(self):
        create_ti()
        self._founded_identifiers: list[FoundedIdentifier] = []
        self._reader = LexemReader(
            lex_table_from_file()
        )
        self.identifiers_for_file = ""
        self.defineds = []

    def __handle_identifier(self):
        self._add_identifier()
        self._reader.read()

    def analyze(self):
        while self._reader.readed_lexem() != 'var':
            self._reader.read()
        self._reader.read()
        while self._reader.readed_lexem() != 'begin':
            self.__handle_identifier()
            while self._reader.readed_lexem() == ',':
                self._reader.read()
                self.__handle_identifier()
            self._reader.read()
            self._set_type()
            self.exclude()
            # self._founded_identifiers = []
            self._reader.read()
            self._reader.read()

        self.add_to_for_file()
        self._upload_to_file()
        self.__analyze_file()

    def _add_identifier(self):
        exist_index = -1
        for index, i in enumerate(self._founded_identifiers):
            if i.name == self._reader.readed_lexem():
                exist_index = index
        if exist_index == -1:
            self._founded_identifiers.append(
                FoundedIdentifier(name=self._reader.readed_lexem(), defined=1, type=None)
            )
        else:
            self._founded_identifiers[exist_index].defined = self._founded_identifiers[exist_index].defined + 1

    def _set_type(self):
        _type = self._reader.readed_lexem()
        ids = self._founded_identifiers
        for i in ids:
            if i.type is None:
                i.type = _type

    def exclude(self):
        ids = self._founded_identifiers
        for i in ids:
            if i.excluded == False or i.excluded is None:
                i.excluded = True

    def add_to_for_file(self):
        ids = self._founded_identifiers
        for i in ids:
            self.identifiers_for_file += f"{i.name} {i.defined} {i.type}\n"

    def _upload_to_file(self):
        with open(get_global_config().OUT_DIR + "/symantic/ti.txt", "w") as f:
            f.writelines(self.identifiers_for_file)


    def __analyze_file(self):
        ids = get_identifiers_from_file()
        for i in ids:
            if i.defined > 1:
                raise SyntaxError(f"duplicate definition identifier: {i.name}")