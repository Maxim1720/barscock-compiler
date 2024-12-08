# from cProfile import label
#
#
# def translate_to_nasm(lexemes):
#     # Словарь для замены лексем на NASM-код
#     lexeme_to_nasm = {
#         "read": lambda var_name: f"""mov rdi, input\n    call read_int\n    mov dword [{var_name}], eax""",
#         "write": lambda vars: "\n".join([f"mov eax, [{var}]\n    call write_int" for var in vars]),
#         "as": lambda dest, value: f"mov dword [{dest}], {value}",
#         "plus": lambda a, b: f"mov eax, [{a}]\n    add eax, [{b}]",
#         "min": lambda a, b: f"mov eax, [{a}]\n    sub eax, [{b}]",
#         "mult": lambda a, b: f"mov eax, [{a}]\n    imul eax, [{b}]",
#         "div": lambda a, b: f"mov eax, [{a}]\n    xor edx, edx\n    idiv dword [{b}]",
#         "or": lambda a, b: f"mov eax, [{a}]\n    or eax, [{b}]",
#         "and": lambda a, b: f"mov eax, [{a}]\n    and eax, [{b}]",
#         "~": lambda a: f"mov eax, [{a}]\n    not eax",
#         "var": lambda vars, vals: f"section .data\n".join(f"\t{v}\tdd {vals[i]}" for i, v in enumerate(vars)),
#         "program": ""
#     }
#
# ##
#     #
#     # section .data
#     #     a       dd 0        ; Переменные типа int
#     #     b       dd 0
#     #     c       dd 0
#     #     d       dq 0.0      ; Переменная типа float (double precision)
#     #     e       db 0        ; Переменные типа bool (1 byte)
#     #     f       db 0
#     #     g       dd 0
#     #     s       dd 0
#     #     hex     dd 0
#     #     decBin  dd 0
#     #     decBin2 dd 0
#     #     i       dd 0
#     #     lol     dd 0
#     # #
#
#
#     nasm_code = []
#     i = 0
#     while i < len(lexemes):
#         lexeme = lexemes[i]
#
#         # Обработка операций со скобками (например, read(a), write(a, b))
#         if lexeme == "read":
#             if lexemes[i + 1] == "(":
#                 var_name = lexemes[i + 2]
#                 nasm_code.append(lexeme_to_nasm["read"](var_name))
#                 i += 4  # Пропустить read, (, переменную, )
#             else:
#                 raise ValueError("Ожидались скобки после 'read'.")
#
#         elif lexeme == "write":
#             if lexemes[i + 1] == "(":
#                 j = i + 2
#                 vars = []
#                 while lexemes[j] != ")":
#                     if lexemes[j] != ",":
#                         vars.append(lexemes[j])
#                     j += 1
#                 nasm_code.append(lexeme_to_nasm["write"](vars))
#                 i = j + 1
#             else:
#                 raise ValueError("Ожидались скобки после 'write'.")
#
#         # Обработка присваивания
#         elif lexeme == "as":
#             dest = lexemes[i - 1]
#             value = lexemes[i + 1]
#             nasm_code.append(lexeme_to_nasm["as"](dest, value))
#             i += 2  # Пропустить обработанное значение
#
#         # Обработка операций (например, plus, min)
#         elif lexeme in lexeme_to_nasm:
#             a = lexemes[i - 1]
#             b = lexemes[i + 1]
#             nasm_code.append(lexeme_to_nasm[lexeme](a, b))
#             i += 2  # Пропустить обработанные значения
#
#         else:
#             i += 1
#
#     return "\n".join(nasm_code)
#
#
# # Пример входных данных
# lexemes = [
#     "read", "(", "a", ")",
#     "a", "as", "123",
#     "a", "plus", "7",
#     "write", "(", "a", ",", "b", ")"
# ]
#
# # Генерация NASM-кода
# nasm_output = translate_to_nasm(lexemes)
# print(nasm_output)