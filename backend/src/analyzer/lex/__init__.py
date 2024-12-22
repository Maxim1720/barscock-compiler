import os
import re


from src.analyzer.lex.file import exists, is_tw, is_tl, write_lex
from src.analyzer.lex.writer import write, flush

os.makedirs(os.path.join(os.getcwd(), 'out'), exist_ok=True)

flush(os.path.join(os.getcwd(),'out','lex','ti.txt'))
flush(os.path.join(os.getcwd(),"out","lex","tl.txt"))
flush(os.path.join(os.getcwd(),"out","lex","tw.txt"))
flush(os.path.join(os.getcwd(),"out","lex","tn.txt"))
flush(os.path.join(os.getcwd(),"out","lex","lex.txt"))

result_table = {
    "tw": [],
    "tl": [],
    "tn": [],
    "ti": []
}

lines_count = 0

tokens = (
    # key words
    'PROGRAM',
    'VAR',
    'BEGIN',
    'INT',
    'FLOAT',
    'BOOL',
    'IF',
    'THEN',
    'ELSE',
    'TO',
    'DO',
    'FOR',
    'WHILE',
    'WRITE',
    'READ',
    'END',
    'AS',
    'TRUE',
    'FALSE',

    # delimiters
    "PLUS",
    "MIN",
    "MULT",
    "DIV",
    "LPAREN",
    "RPAREN",
    # "LBRACE",
    # "RBRACE",
    "DOT",
    "COMMA",
    "SEMICOLON",
    "COLON",
    'OR',
    'AND',
    'LT',
    'LE',
    'EQ',
    'NEQ',
    'GT',
    'GE',
    'NOT',
    # "NEWLINE",

    # "DELIMITER",
    # other

    "NUMBER",
    'ID',

    # number
    "NEWLINE",
)

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)

def t_ignore_COMMENT(t):
    r"\{[^}]*\}"

    path_to_table = os.path.join(os.getcwd(), 'out','lex','tl.txt')

    bracers = ["{", "}"]
    for i in bracers:
        if not exists(i, path_to_table):
            write(i, path_to_table)
            result_table['tl'].append(f"'{i}'")




t_NEWLINE = r'\n'
t_ignore = ' \t'



literals = [
    '(',
    ')',
    ';',
    ":",
    ",",
    '.',
    '~',
    '{',
    '}'
    , 'A'
    , 'B'
    , 'C'
    , 'D'
    , 'E'
    , 'F'
    , 'G'
    , 'H'
    , 'I'
    , 'J'
    , 'K'
    , 'L'
    , 'M'
    , 'N'
    , 'O'
    , 'P'
    , 'Q'
    , 'R'
    , 'S'
    , 'T'
    , 'U'
    , 'V'
    , 'W'
    , 'X'
    , 'Y'
    , 'Z'
    , 'a'
    , 'b'
    , 'c'
    , 'd'
    , 'e'
    , 'f'
    , 'g'
    , 'h'
    , 'i'
    , 'j'
    , 'k'
    , 'l'
    , 'm'
    , 'n'
    , 'o'
    , 'p'
    , 'q'
    , 'r'
    , 's'
    , 't'
    , 'u'
    , 'v'
    , 'w'
    , 'x'
    , 'y'
    , 'z'
    , '0'
    , '1'
    , '2'
    , '3'
    , '4'
    , '5'
    , '6'
    , '7'
    , '8'
    , '9'
            ]

precedence = (
    ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NEQ'),  # Nonassociative operators
    ('left', 'PLUS', 'MIN'),
    ('left', 'MULT', 'DIV'),
    ('right', 'NOT'),  # Unary minus operator
)



reserved = {
    "as": 'AS',
    "plus": 'PLUS',
    "min": 'MIN',
    "mult": 'MULT',
    "div": 'DIV',
    "LT": 'LT',
    "GT": 'GT',
    "LE": 'LE',
    "EQ": 'EQ',
    "NEQ": 'NEQ',
    "begin": 'BEGIN',
    "end": 'END',
    "var": 'VAR',
    "program": 'PROGRAM',
    "write": "WRITE",
    "read": "READ",
    'do': 'DO',
    'to': 'TO',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'or': 'OR',
    'and': 'AND'
}

def t_NUMBER(t):
    r"""[0-1]+[bB]|
        [0-7]+[oO]|
        [0-9a-fA-F]+[hH]|
        (?:\d*\.\d+|\d+)(?:[eE][+-]?\d+)?[dD]?
        """
    path_to_table = os.getcwd()+"/out/lex/tn.txt"
    if not exists(t.value, path_to_table):
        write(t.value, path_to_table)
        write_lex(t.value, 'tn')
        result_table["tn"].append(t.value)
    return t


def t_DELIMITER(t):
    r"""\.|;|:|,|~|\(|\)"""
    types = {
        ".": "DOT",
        ":": "COLON",
        ";": "SEMICOLON",
        ",": "COMMA",
        "~": "NOT",
        "(": "LPAREN",
        ")": "RPAREN",
    }
    t.type = types[t.value]
    if t.type == 'DOT':
        t.lexer.lexstate = "END"
    path_to_table = os.path.join(os.getcwd(), 'out','lex','tl.txt')
    if not exists(t.value, path_to_table):
        write(t.value, path_to_table)
        write_lex(t.value, 'tl')
        result_table['tl'].append(f"'{t.value}'")
    return t









def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9]*"
    t.type = reserved.get(t.value, 'ID')

    tables_path = os.path.join(os.getcwd(), "out", "lex")
    ti = os.path.join(tables_path,'ti.txt')
    tw = os.path.join(tables_path,'tw.txt')
    tl = os.path.join(tables_path,'tl.txt')

    if not exists(t.value, ti):
        if t.type == "ID":
            write(t.value, ti)
            write_lex(t.value, 'ti')
            result_table['ti'].append(t.value)
        else:
            if is_tw(t.value) and not exists(t.value, tw):
                write(t.value, tw)
                write_lex(t.value, 'tw')
                result_table['tw'].append(t.value)
            elif is_tl(t.value) and not exists(t.value, tl):
                write(t.value, tl)
                write_lex(t.value, 'tl')
                result_table['tl'].append(t.value)

    return t





def t_error(t):
    t.lexer.skip(1)
    raise SyntaxError(f"Недопустимый символ '{t.value[0]}'. Строка {t.lineno}")


def t_eof(t):
    if t.lexer.lexstate != 'END':
        raise SyntaxError(f"Неожиданный конец файла")