register = "rax"
register_prefix = "r"

class Node:
    def __init__(self, name):
        self.name = name
        self.inputs:list[Node] = []  # Входные узлы
        self.outputs:list[Node] = []  # Выходные узлы
        self._booleans = {
            "true": '1',
            "false": '0',
        }

    def add_input(self, node):
        """Связывает текущий узел с предыдущим (входным)"""
        self.inputs.append(node)
        node.outputs.append(self)

    def evaluate(self):
        """Метод выполнения операции для данного узла"""
        raise NotImplementedError("This method should be implemented in subclasses")

    def generate_code(self):
        """Метод генерации кода для данного узла"""
        raise NotImplementedError("This method should be implemented in subclasses")





class ValueNode(Node):

    booleans = {
        "false": '0',
        "true": '1',
    }

    """Узел, представляющий литерал"""
    def __init__(self, value):
        super().__init__("Value")
        self.value = self.booleans[value] if value in self.booleans else value

    def evaluate(self):
        return self.value

    def generate_code(self):
        return f"mov {register}, {self.value}"


class TextSectionNode(Node):
    def __init__(self):
        super().__init__("TextSection")

    def generate_code(self):
        return "section .text"



