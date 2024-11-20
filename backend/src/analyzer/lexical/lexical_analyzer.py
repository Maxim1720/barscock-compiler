import re

from .const import State, TableSrc, TableOut, TableLexem
from ...conf import get_global_config

CH = ""
S = ""
B = ""
CS = State.START
t: TableOut|None = None
z = 0


class GC:
    def __init__(self, data: str):
        self.data = data
        self.index = 0

    def read(self):
        global CH
        if self.index >= len(self.data):
            return False
        CH = self.data[self.index]
        self.index += 1
        return self.index != len(self.data)

gc: GC|None = None

def let():
    return CH.isalpha()

def digit():
    return CH.isdigit()

def nill():
    global S
    S = ""

def add():
    global S
    S += CH

def look(t: TableSrc):
    with open(t.value, 'r', encoding="utf-8") as table_file:
        for index, line in enumerate(table_file):
            if S == line:
                return index

    return -1

def put(t: TableOut):
    with open(t.value, 'a+', encoding="utf-8") as table_file:
        lines = table_file.readlines()
        for index, line in lines:
            if S == line:
                return index
        table_file.write(S)
        return len(lines)

def out(n: TableLexem, k: int):
    path = f"{get_global_config().OUT_DIR}/lex/lex.txt"
    with open(path, "a+", encoding="utf-8") as lex:
        lexem = f"{n.value} {k}\n"
        lex.write(lexem)

def analyze(code: str):
    global CS
    global gc
    gc = GC(code)
    while (CS != State.ERROR or CS != State.END) and gc.read():
        CS = State.START
        if let():
            identifier_state()
        elif digit():
            number_state()
        elif CH=='{':
            comment_state()
        elif CH=='.':
            if S == "end":
                add()
                CS = State.END
            float_state()
        else:
            delimiter_state()
    return CS


def identifier_state():
    global CS
    CS = State.IDENTIFIER
    while let() or digit():
        gc.read()
    z = look(TableSrc.TW)
    if z != -1:
        out(TableLexem.TW, z)
    else:
        z = look(TableSrc.TL)
        if z != -1:
            out(TableLexem.TL, z)
        else:
            z = put(TableOut.TI)
            out(TableLexem.TI, z)

def number_state():
    add()
    global CS
    CS = State.NUMBER
    if(re.fullmatch("[0-1]", CH)):
        binary_state()
    elif re.fullmatch("[2-7]", CH):
        oct_state()
    elif re.fullmatch("[8-9]", CH):
        dec_state()
    elif re.fullmatch("[0-9A-Fa-f]", CH):
        hex_state()

def binary_state():
    global CS
    while re.fullmatch("[0-1]", CH) and gc.read():
        add()
    if check_pattern('[Bb]'):
        gc.read()
        add()
        if check_pattern('[0-9A-Fa-f]'):
            hex_state()
        elif check_pattern("[Hh]"):
            pass
        elif white_spaces():
            z = put(TableOut.TN)
            out(TableLexem.TN, z)
        else:
            CS = State.ERROR

    elif check_pattern("[2-7]"):
        oct_state()
    elif check_pattern("[8-9]"):
        dec_state()
    elif check_pattern("[ACFacf]"):
        hex_state()
    elif check_pattern('\\.'):
        float_state()
    elif check_pattern('[Ee]'):
        exponent_state()
    elif check_pattern('[Oo]'):
        pass
    elif check_pattern('[Dd]'):
        pass
    elif check_pattern('[Hh]'):
        pass
    else:
        CS = State.ERROR

def oct_state():
    while re.fullmatch("[0-7]", CH) and gc.read():
        add()
    if check_pattern("[8-9]"):
        dec_state()
    elif check_pattern("\\."):
        float_state()
    elif check_pattern("[Ee]"):
        exponent_state()
    elif check_pattern("[Dd]"):
        add()
    elif check_pattern("[ACFacf]"):
        add()
    elif check_pattern("[Hh]"):
        add()
    elif check_pattern("[Oo]"):
        add()

    gc.read()
    if white_spaces():
       z = put(TableOut.TN)
       out(TableLexem.TN, z)
    else:
        global CS
        CS = State.ERROR

def dec_state():
    while re.fullmatch("[0-9]", CH) and gc.read():
        add()
    if check_pattern("[Hh]"):
        add()
    elif check_pattern("[Ee]"):
        exponent_state()
    elif check_pattern("\\."):
        float_state()
    elif check_pattern("[ACFacf]"):
        hex_state()
    elif check_pattern("[Dd]"):
        add()
        gc.read()
        if check_pattern("[A-Fa-f0-9]"):
            hex_state()
        elif check_pattern("[Hh]"):
            add()
    gc.read()
    if white_spaces():
       z = put(TableOut.TN)
       out(TableLexem.TN, z)
    else:
        global CS
        CS = State.ERROR

def hex_state():
    while re.fullmatch("[0-9A-Fa-f]+", CH) and gc.read():
        add()
    if check_pattern('[Hh]'):
        z = put(TableOut.TN)
        out(TableLexem.TN, z)
    else:
        global CS
        CS = State.ERROR


def float_state():
    while re.fullmatch("[0-9]", CH) and gc.read():
        add()
    if check_pattern("[Ee]"):
        float_exponent_state()
    if white_spaces():
        z = put(TableOut.TN)
        out(TableLexem.TN, z)


def exponent_state():
    global CS
    gc.read()
    if check_pattern("[+-]"):
        add()
        while check_pattern("[0-9]") and gc.read():
            add()
        if white_spaces():
            z = put(TableOut.TN)
            out(TableLexem.TN, z)
        else:
            CS = State.ERROR
    elif check_pattern("[0-9]"):
        while check_pattern("[0-9]") and gc.read():
            add()
        if check_pattern("[A-Fa-f]"):
            hex_state()
        elif check_pattern("[Hh]"):
            add()

        if white_spaces():
            z = put(TableOut.TN)
            out(TableLexem.TN, z)
        else:
            CS = State.ERROR
    elif check_pattern("[A-Fa-f]"):
        add()
        hex_state()
    elif check_pattern('[Hh]'):
        add()
        z = put(TableOut.TN)
        out(TableLexem.TN, z)
    else:
        CS = State.ERROR


def float_exponent_state():
    global CS
    gc.read()
    if check_pattern("[+-]"):
        add()
        while check_pattern("[0-9]") and gc.read():
            add()
        if white_spaces():
            z = put(TableOut.TN)
            out(TableLexem.TN, z)
        else:
            CS = State.ERROR
    if check_pattern("[0-9]"):
        add()
        while check_pattern("[0-9]") and gc.read():
            add()
        if white_spaces():
            z = put(TableOut.TN)
            out(TableLexem.TN, z)
        else:
            CS = State.ERROR
    else:
        CS = State.ERROR

def comment_state():
    while gc.read() and CH != '}':
        pass

def delimiter_state():
    z = look(TableSrc.TL)
    if z!=-1:
        out(TableLexem.TL, z)
    else:
        global CS
        CS = State.ERROR

def check_pattern(pattern: str):
    return re.fullmatch(pattern, CH)

def white_spaces():
    return re.fullmatch("\s", CH)

