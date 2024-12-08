from ply.lex import LexToken, Lexer
from ply.yacc import YaccProduction, LRParser

start = '_P'

def p_error(p: LexToken):
    if p is None:
        print("Syntax error end of input'")
    else:
        print(f"Syntax error at {p} ")

def p_p(p):
    """_P : PROGRAM _D _B DOT"""


def p_b(p):
    """_B : BEGIN _O END"""


def p_d(p):
    """_D : VAR
    | VAR D1"""


def p_d1(p):
    """D1 : _I
    | _I D1"""


def p_i(p):
    """_I : I1 COLON _T SEMICOLON"""

def p_i1(p):
    """I1 : I2
    | I1 COMMA I2"""


def p_i2(p: YaccProduction):
    """I2 : ID"""
    p[0] = p[1]

def p_o(p):
    """
    _O : O1
    | O1 SEMICOLON _O
    |
    """
    if len(p) > 2:
        p[0] = f'{p[1]}{p[2]}{p[3]}'
    elif len(p) == 2:
        p[0] = p[1]


def p_o2(p):
    """
    O2 : _S
    """
    p[0] = p[1]

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
    print(f'A: {p[0]}')


def p_f(p):
    """
    _F : F1
      | F1 ELSE O2
    """


def p_f1(p):
    """
    F1 : IF _E THEN O2
    """


def p_w(p):
    """_W : FOR _A TO _E DO O2 """


def p_y(p):
    """
    _Y : WHILE _E DO O2
    """


def p_u(p):
    """
    _U : READ LPAREN I1 RPAREN
    """


def p_v(p):
    """
    _V : WRITE LPAREN E1 RPAREN
    """


def p_e1(p):
    """E1 : E1 COMMA _E
    | _E
    """


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
    _E : _E Z1 _Z
    | _Z
    """
    if len(p) > 2:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:
        p[0] = p[1]
    print(f"E: {[f for f in p]}")


def p_z(p):
    """
    _Z : _J
      | _Z J1 _J
    """
    if len(p) > 2:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:
        p[0] = p[1]
    print(f"Z: {[f for f in p]}")


def p_j(p):
    """
    _J : _M
      | _J M1 _M
    """
    if len(p) > 2:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:
        p[0] = p[1]
    print(f"J: {[f for f in p]}")

def p_m(p):
    """
    _M : I2
      | _N
      | _L
      | NOT_M
      | PAREN_M
    """
    p[0] = p[1]
    print(f"M: p[1]={p[1]}")

def p_not_m(p):
    """
    NOT_M : NOT _M
    """
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
    p[0] = p[1]


def p_m1(p):
    """
    M1 : MULT
       | DIV
       | AND
    """
    p[0] = p[1]
    print(f"M1: p[1]={p[1]}")

def p_j1(p: YaccProduction):
    """
    J1 : PLUS
       | MIN
       | OR
    """
    p[0] = p[1]

def p_z1(p):
    """
    Z1 : NEQ
       | EQ
       | LT
       | LE
       | GT
       | GE
    """
    p[0] = p[1]

def p_n(p):
    """_N : NUMBER"""
    p[0] = p[1]


def p_t(p):
    """
    _T : INT
      | FLOAT
      | BOOL
    """
    p[0] = p[1]
