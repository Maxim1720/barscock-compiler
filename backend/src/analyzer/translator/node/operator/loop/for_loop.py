from src.analyzer.translator.node.node import Node, register, register_prefix


class ForLoopNode(Node):
    def __init__(self, count):
        super().__init__('FOR-LOOP')
        self.counter = count

    def generate_code(self):
        return f'for_loop_{self.counter}:'

class ForAssignNode(Node):
    def __init__(self):
        super().__init__("FOR")

    def generate_code(self):
        return f"mov {register_prefix}cx, {register}"

class ForToNode(Node):
    def __init__(self):
        super().__init__("FOR-TO")

    def generate_code(self):
        return f"mov {register_prefix}bx, {register}"

class ForConditionNode(Node):
    def __init__(self, count):
        super().__init__("FOR-Condition")
        self.count  = count
    def generate_code(self):
        return f"cmp {register_prefix}cx, {register_prefix}bx\njge end_for_{self.count}"

class ForIncrementNode(Node):
    def __init__(self, counter):
        super().__init__("FOR-Increment")
        self.counter = counter

    def generate_code(self):
        return f"inc {register_prefix}cx\njmp for_loop_{self.counter}"

class ForEndNode(Node):
    def __init__(self, counter):
        super().__init__("FOR-End")
        self.counter = counter

    def generate_code(self):
        return f"end_for_{self.counter}:"