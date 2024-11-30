import unittest

from src import SyntaxAnalyzer, lex_table_from_file, Analyzer
from src.analyzer.syntax.reader import LexemReader
from src.analyzer.syntax.syntax_analyzer import P

code = """
    program 
var 
    a, b, c: int; 
    c, d: float; 
    e, f: bool; 
    g, s, hex, decFromBinary, decFromBinary2: int;

begin
    read(a);
    a as 5 plus 7;
    b as 7 min 0;
    e as 7.5e+575;
    d as c mult 3;
    e as true or ~false;
    f as false and false;
    g as 010101b or 0101b;           
    s as 2343o;             
    b as 0101b;
    hex as 123ABCDh;        
    decFromBinary as 18;    
    decFromBinary2 as 18d;
    if b LT a then 
        a as b
    else
        b as 5 plus b: 
        a as 7:
        a as b:
        b as g:
        g as s;
    for i as 7 to a plus 7 do a as a plus a: b as a;
    write(a)
end.

    """

class Program(unittest.TestCase):
    def test_program(self):
        Analyzer(code).analyze()
        lex_table = lex_table_from_file()
        SyntaxAnalyzer(lex_table).analyze()


if __name__ == '__main__':
    unittest.main()
