from src.analyzer.lexical import logger
from src.analyzer.lexical.const import TableSrc, TableLexem, State
from src.analyzer.lexical.reader import Reader
from src.analyzer.lexical.sub.sub import SubAnalyzer

from src.files import write_out, read_out

counter = 0

class DelimiterAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.DELIMITER

    def __del__(self):
        self._reader.nill()

    def analyze(self) -> Reader:
        self._reader.nill()
        self._reader.add()

        if self._reader.current_last():
            self._reader.gc.ch = ""
        else:
            self._reader.next()
        logger.info(f"delimiter: {self._reader.get_ch()}")
        logger.info(f"delimiter buffer: {self._reader.get_ch()}")
        z = self._reader.look(TableSrc.TL)
        if z != -1:
            self._reader.out(TableLexem.TL, z)
            if self._reader.buffer not in read_out("tl"):
                write_out(TableLexem.TL.name.lower(), self._reader.buffer)
            global counter
            counter+=1
            logger.info(f"delimiter №{counter}: {self._reader.buffer}")
        else:
            self._reader.state = State.ERROR
        return self._reader

