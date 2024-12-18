from src.analyzer.syntax.identifiers import id_exists
from src.analyzer.translator.node.node import Node, register, register_prefix


class ReadNode(Node):
    def __init__(self, val):
        super().__init__("READ")
        self.val = f"[{val}]" if id_exists(val) else val

    def generate_code(self):
        return f"""; Чтение строки из консоли
mov {register}, 0           ; sys_read (системный вызов для чтения)
mov {register_prefix}di, 0           ; Стандартный ввод (stdin)
mov {register_prefix}si, buffer      ; Адрес буфера
mov {register_prefix}dx, length      ; Максимальный размер ввода
syscall              ; Вызов ядра
mov {register_prefix}si, buffer      ; Адрес буфера (исходная строка)
call string_to_int   ; Вызов функции парсинга
mov {self.val}, {register}
        """


class WriteNode(Node):
    def __init__(self, val):
        super().__init__("WRITE")
        self.val = f"[{val}]" if id_exists(val) else val

    def generate_code(self):
        return f"""; Вывод строки в консоль
mov {register}, 1           
mov {register_prefix}di, 1           
mov {register_prefix}si, buffer      
mov {register_prefix}dx, length      
syscall              ; Вызов ядра
"""