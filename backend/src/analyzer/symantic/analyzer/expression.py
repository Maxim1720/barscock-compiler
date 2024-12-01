#Задача анализа выражений - проверить описаны ли переменные, встре-
#чающиеся в выражениях, и соответствуют ли типы операндов друг другу и типу
#операции.
from src.analyzer.syntax.reader import LexemReader


class ExpressionAnalyzer:
    def analyze(self):
        pass


class IdentifiersExistsAnalyzer:
    def __init__(self, reader: LexemReader):
        self._reader = reader

    def analyze(self):
        pass