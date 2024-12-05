from src.files import read_res
from src.analyzer.symantic.analyzer.utils import is_op, semantic_analysis
from src.analyzer.symantic.files import get_identifiers_from_file
from src.analyzer.syntax.reader import LexemReader


class TypesAnalyzer:
    def __init__(self, reader: LexemReader):
        self._reader = reader

    def analyze(self):
        src_lexemes = self._reader.readed_lexemes().copy()
        lexemes = self._reader.readed_lexemes().copy()
        # print(lexemes)

        # if len(lexemes) <= 1:
        #     return

        for index, l in enumerate(lexemes):
            if is_op(l):
                continue
            is_id = False
            for i in get_identifiers_from_file():
                if i.name == l:
                    lexemes[index] = i.type
                    is_id = True
                    break
            if is_id:
                continue

            if l in read_res('tn'):
                if '.' in l:
                    lexemes[index] = 'float'
                else:
                    lexemes[index] = 'int'
                continue

            if l == 'true' or l == 'false':
                lexemes[index] = 'bool'
                continue

            raise SyntaxError(f"unexpected type for '{l}'")

        try:
            return semantic_analysis(lexemes)
        except TypeError as t:
            t.add_note(" ".join(src_lexemes))
            raise t

    # a plus b
    # a plus 6
    # a plus 7.6568e+656