from src.analyzer_v2.translator.node.node import Node


class UtilsFuncsNode(Node):
    def __init__(self):
        super().__init__("UtilsFuncsNode")

    def generate_code(self):
        return """
; Функция для преобразования строки в число
; Вход: RSI - адрес строки
; Выход: RAX - число (результат)
string_to_int:
    xor rax, rax         ; Обнуляем RAX (итоговое число)
    xor rbx, rbx         ; RBX = 0 (используется для цифры)
    xor rcx, rcx         ; RCX = 0 (флаг отрицательного числа)

    ; Проверка на знак числа
    mov al, [rsi]        ; Считываем первый символ
    cmp al, '-'          ; Проверяем на минус
    jne parse_digits     ; Если не минус, переходим к парсингу
    inc rsi              ; Пропускаем знак '-'
    mov rcx, 1           ; Устанавливаем флаг отрицательного числа
parse_digits:
    mov al, [rsi]        ; Считываем символ
    cmp al, 0            ; Проверяем на конец строки
    je finish_parsing    ; Если конец строки, завершаем парсинг
    cmp al, 10           ; Проверка на символ новой строки \\n
    je finish_parsing    ; Завершаем, если новая строка
    sub al, '0'          ; Преобразуем символ в цифру (ASCII '0' -> 0)
    jb finish_parsing    ; Если символ меньше '0', завершаем
    cmp al, 9            ; Проверяем, цифра ли это
    ja finish_parsing    ; Если больше '9', завершаем

    imul rax, rax, 10    ; Умножаем текущее число на 10
    add rax, rbx         ; Добавляем предыдущую цифру
    mov rbx, rax         ; Сохраняем текущее значение
    mov rax, rbx

    inc rsi              ; Переходим к следующему символу
    jmp parse_digits     ; Повторяем цикл
finish_parsing:
    ; Если число отрицательное, меняем знак
    cmp rcx, 1
    jne done
    neg rax              ; Меняем знак числа на отрицательный
    
done:
    ret                  ; Возвращаемся из функции"""