from src.files import read_res


def is_op(val):
    return val in read_res('tl')


# Таблица совместимости для операций
compatibility_table = {
    # Арифметические операции
    ('int', 'int', 'plus'): 'int',
    ('int', 'int', 'min'): 'int',
    ('int', 'int', 'mult'): 'int',
    ('int', 'int', 'div'): 'int',
    ('int', 'float', 'plus'): 'float',
    ('int', 'float', 'min'): 'float',

    ('int', 'float', 'mult'): 'float',
    ('float', 'int', 'mult'): 'float',

    ('int', 'float', 'div'): 'float',
    ('float', 'float', 'plus'): 'float',
    ('float', 'float', 'min'): 'float',
    ('float', 'float', 'mult'): 'float',
    ('float', 'float', 'div'): 'float',
    # Логические операции
        # Конъюнкция/Дизъюнкция
    ('bool', 'bool', 'or'): 'bool',
    ('bool', 'bool', 'and'): 'bool',
    ('int', 'bool', 'or'): 'bool',
    ('bool', 'int', 'or'): 'bool',
    ('float', 'bool', 'or'): 'bool',
    ('bool', 'float', 'or'): 'bool',
    ('int', 'int', 'or'): 'bool',
    ('float', 'float', 'or'): 'bool',

    ('int', 'bool', 'and'): 'bool',
    ('bool', 'int', 'and'): 'bool',
    ('float', 'bool', 'and'): 'bool',
    ('bool', 'float', 'and'): 'bool',
    ('int', 'int', 'and'): 'bool',
    ('float', 'float', 'and'): 'bool',

        # Отрицание
    ('bool', None, '~'): 'bool',


    # Сравнительные операции
    ('int', 'int', 'LT'): 'bool',
    ('int', 'int', 'LE'): 'bool',
    ('int', 'int', 'GT'): 'bool',
    ('int', 'int', 'GE'): 'bool',
    ('int', 'float', 'LT'): 'bool',
    ('int', 'float', 'LE'): 'bool',
    ('int', 'float', 'GT'): 'bool',
    ('int', 'float', 'GE'): 'bool',
    ('float', 'float', 'LT'): 'bool',
    ('float', 'float', 'LE'): 'bool',
    ('float', 'float', 'GT'): 'bool',
    ('float', 'float', 'GE'): 'bool',

    #присвоение
    ('int', 'int', 'as'): 'int',
    ('float', 'float', 'as'): 'float',
    ('bool', 'bool', 'as'): 'bool',

    ('int'): 'int',
    ('float'): 'float',
    ('bool'): 'bool',
}


def semantic_analysis(expression):
    """
    Анализирует совместимость типов в выражении.
    :param expression: Список вида [операнд, операция, операнд, операция, ...].
    :return: Тип результата выражения или ошибка при несовместимости.
    """
    if len(expression) < 1:
        return
    if len(expression) < 2:
        type = compatibility_table.get(expression[0])
        if type is None:
            raise ValueError("Выражение слишком короткое для анализа.")
        return type

    i = 0
    while i < len(expression):
        token = expression[i]

        if token == '~':  # Унарная операция
            if i + 1 >= len(expression):
                raise ValueError(f"Ожидается операнд после унарной операции '{token}'.")
            operand = expression[i + 1]
            if operand != 'bool':
                raise TypeError(f"Операция '{token}' не поддерживается для типа '{operand}'.")
            # Заменяем `~ operand` на `bool`
            expression[i] = 'bool'
            del expression[i + 1]
        else:
            i += 1

    # После обработки всех `~`, передаем результат для стандартного анализа
    return evaluate_expression(expression)


def evaluate_expression(expression):
    """
    Проводит семантический анализ оставшегося выражения.
    :param expression: Список после обработки унарных операторов.
    :return: Тип результата выражения или ошибка при несовместимости.
    """
    print(f"current expression: {expression}")
    if len(expression) < 3 or len(expression) % 2 == 0:
        raise ValueError("Выражение должно содержать чередующиеся операнды и операции.")

    current_type = expression[0]
    i = 1
    while i < len(expression):
        operator = expression[i]

        if operator == 'as':
            #float as float mult float
            expression = expression[i + 1:]
            next_operand = semantic_analysis(expression)

        else:
            next_operand = expression[i + 1]

        result_type = compatibility_table.get((current_type, next_operand, operator))
        if result_type is None:
            raise TypeError(f"Операция '{operator}' не поддерживается для типов '{current_type}' и '{next_operand}'.")
        current_type = result_type
        i += 2

    return current_type


