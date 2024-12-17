
import ply.lex as lexer
from src.analyzer_v2.lex import *

from src import debug

lex = lexer.lex(debug=debug)

def analyze_lex(code):
    lex.input(code)
    while True:
        tok = lex.token()
        if not tok:
            break
        if debug:
            print(tok)