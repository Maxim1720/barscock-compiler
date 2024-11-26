import re

from src.conf import get_global_config as config


def lex_table_from_file() -> list[list[int]]:
    lex_table: list[list[int]] = []
    with open(f'{config().OUT_DIR}/lex/lex.txt', 'r') as f:
        for l in f.readlines():
            numbers = re.split(" ", l)
            numbers[1] = numbers[1].strip()
            numbers = list(map(int, numbers))
            lex_table.append(numbers)
    return lex_table