import subprocess

from colorama import Fore, Style

from src.analyzer.lex import *
from src.analyzer.lex.analyze import analyze_lex
from src.analyzer.syntax.analyze import analyze_syntax


def main():
    with open(f"{os.path.join(os.getcwd(),'code.txt')}", 'r') as f:
        code = f.read()
    try:
        analyze_lex(code)
        print("-"*100)
        print("Лексический анализ прошел успешно!")
        for i in result_table:
            print(f"Результат для таблицы {i}:")
            print(", ".join(result_table[i]))
        print("-"*100)
        analyze_syntax(code)
        print("Синтаксический и семантический анализ прошли успешно")
        print("-" * 100)

        subprocess.run(['nasm', '-f', 'elf64',
                        f'{os.path.join(os.getcwd(), "output.asm")}',
                        '-o', f'{os.path.join(os.getcwd(), "output.o")}'])
        print("Объектный файл успешно скомпилирован!")
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
    finally:
        print("-" * 100)


if __name__ == '__main__':
    main()
