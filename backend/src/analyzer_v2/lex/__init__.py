from src.files import read_res

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

    # other

    "NUMBER",
    'ID',

    #number
    "BINARY"
)

print(tokens)
t_ignore = ' \t\n'

literals = ['(', ')', ';', ":", ",", '.', '~', '{', '}'
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

t_ignore_COMMENT = r"\{[^}]*\}"
t_DOT = r'\.'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_NOT = r'~'
t_LPAREN = r'\('
t_RPAREN = r'\)'

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

t_NUMBER = r"""
    [0-1]+[bB]|
    [0-7]+[oO]|
    [0-9a-fA-F]+[hH]|
    \d+(?:\.\d+)?(?:[eE][+-]?\d+)?[dD]?
    """



def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9]*"
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
