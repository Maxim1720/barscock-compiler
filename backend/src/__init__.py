from backend.src.analyzer.lexical.lexical_analyzer import Analyzer
from backend.src.main import read_out, config

files = [
    "tw","tl","ti", "tn", "lex"
]

for file in files:
    with open(f"{config.OUT_DIR}/lex/{file}.txt", "w") as f:
        f.write("")



def __main__():
    code = """
    program var a,b : int; c, d: float; e, f: bool; begin a as 5
    b as 7: e as 7.5: d as c: e as true: f as false
    b as b minus a
    if b LT a then a as a plus b else b as b minus 5
    end.
    """



    state = Analyzer(code).analyze()

    print("ti")
    print(read_out("ti"))
    print("tn")
    print(read_out("tn"))

    print(state)

if __name__ == '__main__':
    __main__()