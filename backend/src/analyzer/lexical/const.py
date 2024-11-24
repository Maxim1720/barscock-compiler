from enum import Enum
from conf import get_global_config

class State(Enum):
    START = 0
    IDENTIFIER = 1
    NUMBER = 2
    COMMENT = 3
    DV = 4
    DELIMITER = 5
    END = 6
    ERROR = 7


class TableSrc(Enum):
    TW = f"{get_global_config().RES_DIR}/tw.txt"
    TL = f"{get_global_config().RES_DIR}/tl.txt"
    TI = f"{get_global_config().RES_DIR}/ti.txt"
    TN = f"{get_global_config().RES_DIR}/tn.txt"

class TableOut(Enum):
    TW = f"{get_global_config().OUT_DIR}/lex/tw.txt"
    TL = f"{get_global_config().OUT_DIR}/lex/tl.txt"
    TI = f"{get_global_config().OUT_DIR}/lex/ti.txt"
    TN = f"{get_global_config().OUT_DIR}/lex/tn.txt"

class TableLexem(Enum):
    TW = 1
    TL = 2
    TI = 3
    TN = 4


__all__ = [
    "TableSrc",
    "TableOut",
    "TableLexem",
]

