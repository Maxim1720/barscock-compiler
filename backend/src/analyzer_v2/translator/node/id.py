from .node import Node, register, register_prefix

class AssignNode(Node):
    """Узел для операции присваивания"""
    def __init__(self, var_to):
        super().__init__("Assign")
        self.var_to = var_to

    def __repr__(self):
        return f"Assign({self.var_to})"

    def evaluate(self):
        value = self.inputs[0].evaluate()
        return {self.var_to: value}

    def generate_code(self):
        return f"mov [{self.var_to}], {register}"


class IdentifierNode(Node):
    """Узел, представляющий значение переменной"""
    def __init__(self, value):
        super().__init__("Value")
        self.value = value

    def evaluate(self):
        return self.value

    def generate_code(self):
        return f"mov {register}, [{self.value}]"




class DefinitionNode(Node):
    def __init__(self, var, type):
        super().__init__("Definition")
        self.var = var
        self.type = type

    def generate_code(self):
        code = ""
        if self.type == 'int':
            code = f"{self.var} dd 0"
        elif self.type == 'float':
            code = f"{self.var} dq 0.0"
        elif self.type == 'bool':
            code = f"{self.var} db 0"
        return code

class VarSectionNode(Node):
    def __init__(self):
        super().__init__("VarSection")

    def generate_code(self):
        return f'global _start\nsection .data'

class BufferSection(Node):
    def __init__(self):
        super().__init__("BufferSection")

    def generate_code(self):
        return f"""section .bss\nbuffer {register_prefix}esb 32"""