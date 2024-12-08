from enum import Enum

from src.conf import get_global_config

class TableSrc(Enum):
    TW = f"{get_global_config().RES_DIR}/tw.txt"
    TL = f"{get_global_config().RES_DIR}/tl.txt"
    TI = f"{get_global_config().RES_DIR}/ti.txt"
    TN = f"{get_global_config().RES_DIR}/tn.txt"

def look(val, t: TableSrc):
    with open(t.value, 'r', encoding="utf-8") as table_file:
        lines = table_file.readlines()
        for i in range(len(lines)):
            if lines[i].isspace():
                continue
            line = lines[i].strip()
            if val == line:
                return i
    return -1


__all__ = [
    'look'
]