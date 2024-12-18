import os

import ply.yacc as yacc

from src import debug
from src.analyzer.syntax.identifiers import flush
from src.analyzer.syntax.parser import *

parser = yacc.yacc(debug=True, start=start)

def analyze_syntax(code):
    result = parser.parse(code)
    # print(f"Syntax analyze result: {str(result)}")
    flush('')


def analyze_syntax_input():
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"Result: {result}")
    flush()
