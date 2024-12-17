import subprocess

from src.analyzer_v2.lex import *
from src.analyzer_v2.lex.analyze import analyze_lex
from src.analyzer_v2.syntax.analyze import analyze_syntax


def main():
    with open('code.txt', 'r') as f:
        code = f.read()
    analyze_lex(code)
    print("Лексический анализ прошел успешно!")
    analyze_syntax(code)
    print("Синтаксический и семантический анализ прошли успешно")

    import os
    subprocess.run(['nasm', '-f', 'elf64',
                    f'{os.getcwd()}/output.asm',
                    '-o', f'{os.getcwd()}/output.o'])

    print("Объектный файл успешно скомпилирован!")
if __name__ == '__main__':
    main()
