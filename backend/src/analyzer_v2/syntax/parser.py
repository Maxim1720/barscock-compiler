import re
import ast

from ply.lex import LexToken, Lexer
from ply.yacc import YaccProduction, LRParser

from .exceptions import AlreadyExistsError, UnknownIdentifierError
from .identifiers import *

start = '_P'

def p_error(p: LexToken):
    if p is None:
        print("Syntax error end of input'")
    else:
        print(f"Syntax error at {p} ")

def p_p(p):
    """_P : PROGRAM _D _B DOT"""
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'

def p_b(p):
    """_B : BEGIN _O END"""
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_d(p):
    """
    _D : VAR D1
    | VAR
    """
    p[0] = p[1]

# def p_d_d1(p):
#     """_D : VAR D1"""
#     p[0] = f'{p[1]} {p[2]}'


def p_d1_rec(p):
    """D1 : _I D1"""
    p[0] = f'{p[1]} {p[2]}'

def p_d1(p):
    """D1 : _I"""
    p[0] = p[1]

def p_i(p):
    """_I : I1 COLON _T SEMICOLON"""
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    ids = re.split(r'[ \t,]+', p[1])
    for i in ids:
        add_id(
            Identifier(name=i, type=p[3])
        )
    for i in founded:
        if i.count > 1:
            raise AlreadyExistsError(f"Identifier '{i.name}' already exists")

    print(f'ids: {[f.name for f in founded]}')


def p_i1(p):
    """I1 : I2"""
    p[0] = p[1]

def p_i1_comma(p):
    """I1 : I1 COMMA I2"""
    p[0] = f'{p[1]} {p[2]} {p[3]}'


def p_i2(p: YaccProduction):
    """I2 : ID"""
    p[0] = p[1]

def p_o(p):
    """_O : O1"""
    p[0] = p[1]

def p_os(p):
    """_O : O1 SEMICOLON _O"""
    p[0] = f'{p[1]}{p[2]}{p[3]}'

def p_o_empty(p):
    """_O : """
    pass


def p_o2(p):
    """
    O2 : _S
    """
    p[0] = p[1]

def p_s(p):
    """
    _S : O1
    | _S S1 O1
    """
    if len(p) > 2:
        p[0] = f'{p[1]}{p[2]}{p[3]}'
    else:
        p[0] = p[1]
    print(f'S: {p[0]}')


def p_o1(p):
    """
    O1 : _A
    | _F
    | _W
    | _Y
    | _U
    | _V
    """
    p[0] = p[1]
    print(f"O1: {p[0]}")


def p_s1(p):
    """
    S1 : COLON
    """
    p[0] = p[1]
def p_a(p):
    """
    _A : I2 AS _E
    """
    p[0] = f'{p[1]} {p[2]} {p[3]}'
    p0 = p[0]
    p3 = p[3]

    id = None
    for i in founded:
        if i.name == p[1]:
            id = i
            break
    if id is None:
        raise UnknownIdentifierError(f"Identifier '{id}' not defined")
    print(f"types: {id.type} {type(p[3])}")

    need_type = f"<class '{id.type}'>"
    print(f"need type: {need_type}")

    if str(type(p[3])) != need_type:
        raise TypeError(f"Type error: {type(p[3])} -> {id.type}, identifier is '{id.name}'")
    id.value = p[3]
    print(f'A: {p[0]}')


def p_f(p):
    """
    _F : F1
      | F1 ELSE O2
    """
    print(p[0])


def p_f1(p):
    """
    F1 : IF _E THEN O2
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    print(f'F1: {p[0]}')


def p_w(p):
    """_W : FOR _A TO _E DO O2 """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}'


def p_y(p):
    """
    _Y : WHILE _E DO O2
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'


def p_u(p):
    """
    _U : READ LPAREN I1 RPAREN
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'


def p_v(p):
    """
    _V : WRITE LPAREN E1 RPAREN
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'


def p_e1(p):
    """E1 : E1 COMMA _E
    | _E
    """
    if len(p) > 2:
        p[0] = f'{p[1]} {p[2]} {p[3]}'
    else:
        p[0] = p[1]


#
# def p_binary_operators(p):
#     '''
#     expression : expression PLUS term
#     | expression MIN term
#     term : term MULT factor
#     | term DIV factor'''
#
#     if p[2] == 'plus':
#         p[0] = p[1] + p[3]
#     elif p[2] == 'min':
#         p[0] = p[1] - p[3]
#     elif p[2] == 'mult':
#         p[0] = p[1] * p[3]
#     elif p[2] == 'div':
#         p[0] = p[1] / p[3]
#
# def p_term_factor(p):
#     """term : factor"""
#     p[0] = p[1]
#
# def p_factor_num(p):
#     """factor : NUMBER
#     | ID
#     | _L
#     | NOT factor
#     """
#     p[0] = p[1]
#
# def p_factor_expr(p):
#     """factor : LPAREN expression RPAREN"""
#     p[0] = p[2]


def p_e(p):
    """
    _E : _Z
    """
    print(f'evaling {p[1]}')
    p[0] = p[1]
    print(f"E: {p[0]}")

def p_e_rec(p):
    """_E : _E Z1 _Z"""
    p[0] = f"{p[1]} {p[2]} {p[3]}"
    p[0] = eval(p[0])

def p_z(p):
    """_Z : _J"""
    p[0] = p[1]
    print(f"Z: {[f for f in p]}")

def p_z_rec(p):
    """_Z : _Z J1 _J"""
    p[0] = f"{p[1]} {p[2]} {p[3]}"
    p[0] = eval(p[0])
    print(f"Z rec: {p[0]}")

def p_j(p):
    """
    _J : _M
      | _J M1 _M
    """
    if len(p) > 2:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
        p[0] = eval(p[0])
    else:
        p[0] = p[1]
    print(f"J: {p[0]}")

def p_m(p):
    """
    _M : _N
      | _L
      | NOT_M
      | PAREN_M
    """
    p[0] = p[1]
    print(f"M: p[1]={p[1]}")


def p_id(p):
    """_M : I2"""
    for i in founded:
        if i.name == p[1]:
            p[0] = i.value
            break

def p_not_m(p):
    """
    NOT_M : NOT _M
    """
    for i in founded:
        if i.name == p[1]:
            if i.type != 'bool':
                raise TypeError(f"Type error: {i.type}. Expected: bool. identifier: '{i.name}'")
    p[0] = not p[1]

def p_paren_m(p):
    """
    PAREN_M : LPAREN _E RPAREN
    """
    p[0] = p[2]



def p_l(p):
    """
    _L : TRUE
      | FALSE
    """
    p[0] = f'{p[1][:1].upper()}{p[1][1:]}'


def p_m1(p):
    """
    M1 : MULT
       | DIV
       | AND
    """
    sign = {
        'mult': '*',
        'div': '/',
        'and': '&',
    }
    p[0] = sign[p[1]]
    print(f"M1: p[1]={p[1]}")

def p_j1(p: YaccProduction):
    """
    J1 : PLUS
       | MIN
       | OR
    """
    sign = {
        'plus': '+',
        'min': '-',
        'or': '|',
    }
    p[0] = sign[p[1]]

def p_z1(p):
    """
    Z1 : NEQ
       | EQ
       | LT
       | LE
       | GT
       | GE
    """
    print(f"Z1: {[f for f in p]}")
    op = {
        'NEQ': '!=',
         "EQ": "==",
         "LT": "<",
         "LE": "<=",
         "GT": ">",
         "GE": ">=",
    }
    p[0] = op[p[1]]

def p_n(p):
    """_N : NUMBER"""

    n:str = p[1]
    if re.fullmatch(r"\d+[bBhHoO]", n):
        suffix = n[-1].lower()
        base = {
            'h': 16,
            'o': 8,
            'b': 2,
        }
        p[0] = int(f"0{suffix}{n[:-1]}", base[suffix])
    elif re.fullmatch(r"\d+[dD]", n):
        p[0] = int(n[:-1])
    else:
        p[0] = p[1]
    print(f'number: {p[0]}')

def p_t(p):
    """
    _T : INT
      | FLOAT
      | BOOL
    """
    p[0] = p[1]
