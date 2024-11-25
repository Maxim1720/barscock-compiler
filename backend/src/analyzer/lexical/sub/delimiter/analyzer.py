from src.analyzer.lexical import logger
from src.analyzer.lexical.const import TableSrc, TableLexem, State
from src.analyzer.lexical.reader import Reader
from src.analyzer.lexical.sub.sub import SubAnalyzer


class DelimiterAnalyzer(SubAnalyzer):

    def __del__(self):
        self._reader.nill()

    def analyze(self) -> Reader:
        self._reader.nill()
        self._reader.add()

        if self._reader.current_last():
            self._reader.gc.ch = ""
        else:
            self._reader.next()
        print(self._reader.buffer)
        logger.info(f"delimiter: {self._reader.get_ch()}")
        logger.info(f"delimiter buffer: {self._reader.get_ch()}")
        z = self._reader.look(TableSrc.TL)
        if z != -1:
            self._reader.out(TableLexem.TL, z)
        else:
            self._reader.state = State.ERROR
        return self._reader

