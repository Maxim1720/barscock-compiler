import ply.yacc as yacc
from src.analyzer_v2.lex import tokens
from src.analyzer_v2.syntax.parser import *

parser = yacc.yacc(debug=True, start=start)

def analyze_syntax(code):
    result = parser.parse(code)
    print(f"Syntax analyze result: {str(result)}")

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
