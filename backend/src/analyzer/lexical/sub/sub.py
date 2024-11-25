from src.analyzer.lexical import logger
from src.analyzer.lexical.reader import Reader


class SubAnalyzer:
    def __init__(self, reader: Reader):
        self._reader = reader
        # self._reader.nill()
        self._reader.add()
        logger.info(f"buffer in {self.__class__} constructor: {self._reader.buffer}")
        logger.info(f"ch in {self.__class__} constructor: {self._reader.get_ch()}")

    def analyze(self):
        pass
