import os.path

from .writer import write


def exists(content, path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f.readlines():
                if line.strip() == content:
                    return True

    return False



def is_tw(token):
    with open(os.path.join(os.getcwd(), 'res', "tw.txt"), 'r') as f:
        for line in f.readlines():
            if line.strip() == token:
                return True
    return False


def is_tl(token):
    with open(os.path.join(os.getcwd(), 'res', "tl.txt"), 'r') as f:
        for line in f.readlines():
            if line.strip() == token:
                return True
    return False

def get_line_number(content, path):
    with open(path, 'r') as f:
        for index, line in enumerate(f.readlines()):
            if line.strip() == content:
                return index

    return -1


def write_lex(content, type):
    table_dict = {
        "tw": 1,
        "tl": 2,
        "ti": 3,
        "tn": 4
    }
    src_dir = os.path.join('out','lex')
    n = get_line_number(content, os.path.join(os.getcwd(), src_dir, f'{type}.txt'))
    write(f"{table_dict[type]} {n}", os.path.join(os.getcwd(), "out", "lex", "lex.txt"))


def read_lexemes():
    with open(os.path.join(os.getcwd(), 'out', 'lex', 'lex.txt'), 'r') as f:
        return map(lambda l: l.strip(), f.readlines())