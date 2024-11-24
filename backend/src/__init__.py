import os.path
import re

from analyzer.lexical.const import TableLexem
from analyzer.lexical.lexical_analyzer import Analyzer
from analyzer.syntax.syntax_analyzer import SyntaxAnalyzer
from conf import get_global_config as config
from files import read_res, read_out

files = [
    "tw","tl","ti", "tn", "lex"
]

for file in files:
    file = f"{config().OUT_DIR}/lex/{file}.txt"
    if os.path.exists(file):
        os.remove(file)
    with open(file, "a+") as f:
        f.write("")

code = """
    program var a,b: int; c, d: float; e, f: bool; g: int;
    begin a as 5
    b as 7: e as 7.5e+575: d as c: e as true: f as false
    g as 010101abh
    s as 2343o
    b as b min a
    if b LT a then a as a plus b else b as b min 5
    end.
    """

def __main__():

    state = Analyzer(code).analyze()

    print("ti")
    print(read_out("ti"))
    print("tn")
    print(read_out("tn"))
    print("tw")

    tw = []
    tl = []
    with open(f"{config().OUT_DIR}/lex/lex.txt", "r") as f:
        for line in f.readlines():
            numbers = re.split(" ", line)
            numbers[1] = numbers[1].strip()
            if int(numbers[0]) == TableLexem.TL.value:
                type = "tl"
            elif int(numbers[0]) == TableLexem.TW.value:
                type = "tw"
            else:
                continue

            for index, l in enumerate(read_res(type)):
                if index == int(numbers[1]):
                    if type == "tl":
                        tl.append(l)
                    else:
                        tw.append(l)
    print(tw)
    print("tl")
    print(tl)


    print(state)


    SyntaxAnalyzer().analyze()

if __name__ == '__main__':
    # print(
    #     re.split(r"[^\w]", code.strip())
    # )
    __main__()