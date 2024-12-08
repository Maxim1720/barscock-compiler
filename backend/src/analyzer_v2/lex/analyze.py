import ply.lex as lexer
from src.analyzer_v2.lex import *

lex = lexer.lex(debug=True)

def analyze_lex(code):
    lex.input(code)
    while True:
        tok = lex.token()
        if not tok:
            break
        print(tok)