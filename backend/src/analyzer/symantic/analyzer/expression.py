#Задача анализа выражений - проверить описаны ли переменные, встре-
#чающиеся в выражениях, и соответствуют ли типы операндов друг другу и типу
#операции.
from src.analyzer.symantic.files import get_identifiers_from_file
# встречается в :
# for .. to <exp>
# white <exp>
# if <exp>
# as <exp>
# write(<exp>


from src.analyzer.syntax.reader import LexemReader


class ExpressionAnalyzer:
    def analyze(self):
        pass


class IdentifiersExistsAnalyzer:
    def __init__(self, reader: LexemReader):
        self._reader = reader

    def analyze(self):
        identifier = self._reader.readed_lexem()
        if not identifier in [x.name for x in get_identifiers_from_file()]:
            raise SyntaxError(f"identifier '{identifier}' is undefined")
