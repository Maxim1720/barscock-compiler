from src.analyzer_v2.translator.node.node import Node


class WhileLoopNode(Node):
    def __init__(self, count):
        super().__init__("WHILE")
        self.count = count

    def generate_code(self):
        return f'while_loop_{self.count}'


class WhileEndNode(Node):
    def __init__(self, count):
        super().__init__("WHILEEND")
        self.count = count

    def generate_code(self):
        return f'while_end_{self.count}'
