from src.analyzer_v2.translator.node.node import Node, register, register_prefix


class WhileLoopNode(Node):
    def __init__(self, count):
        super().__init__("WHILE")
        self.count = count

    def generate_code(self):
        return f'while_loop_{self.count}:'


class WhileConditionNode(Node):
    def __init__(self, count):
        super().__init__("FOR-Condition")
        self.count  = count
    def generate_code(self):
        return f"cmp {register_prefix}cx, {register_prefix}bx\njge end_while_{self.count}"

class WhileEndNode(Node):
    def __init__(self, count):
        super().__init__("WHILEEND")
        self.count = count

    def generate_code(self):
        return f'end_while_{self.count}:'
