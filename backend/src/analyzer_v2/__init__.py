from src.analyzer_v2.lex.analyze import analyze_lex
from src.analyzer_v2.syntax.analyze import analyze_syntax, analyze_syntax_input
from src.analyzer_v2.syntax.identifiers import flush

code = """
program var 
    a, b, c: int; 
    d: float; 
    e, f: bool; 
    g, s, hex, decFromBinary, decFromBinary2: int;
    i: int;
    lol: int;
begin
    read(a);
    lol as 123;
    a as 5 plus 7;
    b as 7 min 0;
    d as 7.5e+5;
    d as 5.5 mult 3;
    e as true or ~false;
    f as false and false;
    s as 2343o;             
    {b as 0101b;}
    hex as 123ABCDh;        
    decFromBinary as 18;    
    decFromBinary2 as 18d;
    
    if a LT b
    then 
        dwad111 as b;
    else
        b as 5 plus b:
        a as 7:
        a as b:
        b as g:
        g as s;
        
    {for i as 7 to a plus 7 
    do a as a plus a: b as a;
    write(a plus a plus a);
    while e do a as g plus 2}
    
    123 321 321 3 123
    
end.
"""
simple = """program
varik
"""
analyze_lex(code)
# analyze_syntax_input()

# try:
analyze_syntax(code)
# except Exception as e:
#     print(str(e))
#     flush()

