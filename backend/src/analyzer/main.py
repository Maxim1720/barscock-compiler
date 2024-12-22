import os.path
import subprocess

from colorama import Fore, Style

from src.analyzer.lex import *
from src.analyzer.lex.analyze import analyze_lex
from src.analyzer.lex.file import read_lexemes
from src.analyzer.syntax.analyze import analyze_syntax
from src.config import Config


def main():

    try:
        with open(f"{os.path.join(Config().ROOT_DIR,'code.txt')}", 'r') as f:
            code = f.read()
        print("Лексический анализ...")
        analyze_lex(code)
        print("-"*100)
        print("Лексический анализ прошел успешно!")
        for i in result_table:
            print(f"Результат для таблицы {i}:")
            print(", ".join(result_table[i]))
        print("-"*100)
        print("Таблица лексем: ")
        for index, i in enumerate(read_lexemes()):
            line = re.split(' ', i)
            print(f"({line[0]} {line[1]})", end=", ")
            if index % 6 == 0 and index!=0 :
                print()
        print()
        print("-"*100)

        print("Синтаксический анализ, Семантический анализ...")
        analyze_syntax(code)
        print("Синтаксический и семантический анализ прошли успешно")
        print("-" * 100)

        subprocess.run(['nasm', '-f', 'elf64',
                        f'{os.path.join(Config().ROOT_DIR, "output.asm")}',
                        '-o', f'{os.path.join(Config().ROOT_DIR, "output.o")}'])
        print("Объектный файл успешно скомпилирован!")
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
    finally:
        print("-" * 100)


if __name__ == '__main__':
    main()
