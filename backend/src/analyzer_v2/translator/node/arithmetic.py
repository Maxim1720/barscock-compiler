from .node import Node, register, register_prefix
from ...semantic.identifier import IdentifierChecker


class AddNode(Node):
    """Узел для сложения"""
    def __init__(self, value_to_add):
        super().__init__("Add")
        self.value_to_add = value_to_add if not IdentifierChecker(value_to_add).exists() else f'[{value_to_add}]'

    def evaluate(self):
        input_value = self.inputs[0].evaluate()
        return input_value + self.value_to_add

    def generate_code(self):
        return f"add {register}, {self.value_to_add}"


class MinNode(Node):
    """Узел для нахождения минимума"""
    def __init__(self, min_value):
        super().__init__("Min")
        self.min_value = min_value if not IdentifierChecker(min_value).exists() else f'[{min_value}]'

    def generate_code(self):
        return f"sub {register}, {self.min_value}"


class MultNode(Node):
    def __init__(self, val):
        super().__init__("Mult")
        self.val = val if not IdentifierChecker(val).exists() else f'[{val}]'

    def generate_code(self):
        return f"mov {register_prefix}bx, {self.val}\nimul {register_prefix}bx"

class DivNode(Node):
    def __init__(self, val):
        super().__init__("Div")
        self.val = val if not IdentifierChecker(val).exists() else f'[{val}]'

    def generate_code(self):
        return f"mov {register_prefix}bx, {self.val}\nidiv {register_prefix}bx"

class AndNode(Node):
    def __init__(self, val):
        super().__init__("And")
        self.val = val if not IdentifierChecker(val).exists() else f'[{val}]'
        self.val = self._booleans[self.val] if val in self._booleans else self.val

    def generate_code(self):
        return f"mov {register_prefix}bx, {self.val}\nand {register}, {register_prefix}bx"


class OrNode(Node):
    def __init__(self, val):
        super().__init__("Or")
        self.val = val if not IdentifierChecker(val).exists() else f'[{val}]'
        self.val = self._booleans[self.val] if val in self._booleans else self.val

    def generate_code(self):
        return f'mov {register_prefix}bx, {self.val}\nor {register_prefix}bx, {register}'

