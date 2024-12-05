import os.path
import re

from .analyzer.lexical.const import TableLexem
from .conf import get_global_config as config


def read_out(type: str):
    items = []
    with open(f"{config().OUT_DIR}/lex/{type}.txt", "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            items.append(line)
    return items

def read_res(type: str):
    items = []
    prefix_path = f"{config().RES_DIR}"
    if type == "tn" or type == 'ti':
        return read_out(type)

    with open(f'{prefix_path}/{type}.txt', "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            items.append(line)
    return items


def write_out(table_type: str, val: str):
    path = f"{config().OUT_DIR}/lex/{table_type}.txt"
    with open(path, "a", encoding='utf-8') as f:
        f.write(f'{val}\n')

def read_lexems(type: str):
    lexems = []

    t = None
    if type == "tw":
        t = TableLexem.TW
    elif type == "ti":
        t = TableLexem.TI
    elif type == "tn":
        t = TableLexem.TN
    elif type == "tl":
        t = TableLexem.TL

    with open(f"{config().OUT_DIR}/lex/lex.txt", "r") as f:
        for line in f.readlines():
            numbers = re.split(" ", line)
            numbers[1] = numbers[1].strip()
            if int(numbers[0]) == t.value:
                for index, l in enumerate(read_res(type)):
                    if index == int(numbers[1]):
                        lexems.append(l)
    return lexems

def flush_out():
    files = [
        "ti",
        "tn",
        "lex",
        "tw",
        "tl"
    ]

    if not os.path.exists(f"{config().OUT_DIR}/lex"):
        os.makedirs(f"{config().OUT_DIR}/lex")


    for f in files:
        path = f"{config().OUT_DIR}/lex/{f}.txt"
        if os.path.exists(path):
            os.remove(path)
        with open(path, "w", encoding='utf-8') as f:
            f.write("")



__all__ = [
    "read_out",
    "read_res",
    'read_lexems',
]