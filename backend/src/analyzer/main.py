import subprocess

from src.analyzer.lex import *
from src.analyzer.lex.analyze import analyze_lex
from src.analyzer.syntax.analyze import analyze_syntax
import os

def main():
    with open(f'{os.getcwd()}/code.txt', 'r') as f:
        code = f.read()
    analyze_lex(code)
    print("Лексический анализ прошел успешно!")
    analyze_syntax(code)
    print("Синтаксический и семантический анализ прошли успешно")

    subprocess.run(['nasm', '-f', 'elf64',
                    f'{os.getcwd()}/output.asm',
                    '-o', f'{os.getcwd()}/output.o'])

    print("Объектный файл успешно скомпилирован!")
if __name__ == '__main__':
    main()
