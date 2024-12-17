from src.analyzer_v2.translator.node.node import Node


class IfNode(Node):
    def __init__(self, count):
        super().__init__("IF")
        self.counter = count

    def generate_code(self):
        return f";if node\ncmp al, 0\nje else_label_{self.counter}"


class ThenNode(Node):
    def __init__(self, count):
        super().__init__("THEN")
        self.counter = count

    def generate_code(self):
        return f";then section\nthen_label_{self.counter}:"

class ThenEndNode(Node):
    def __init__(self, count):
        super().__init__("THENEND")
        self.counter = count

    def generate_code(self):
        return f"jmp enf_if_label_{self.counter}"

class ElseNode(Node):
    def __init__(self, count):
        super().__init__("ELSE")
        self.counter = count

    def generate_code(self):
        return f"; else section\nelse_label_{self.counter}:"

class ElseEndNode(Node):
    def __init__(self, count):
        super().__init__("ELSEEND")
        self.counter = count

    def generate_code(self):
        return f"jmp end_if_label_{self.counter}"

class EndIfNode(Node):
    def __init__(self, count):
        super().__init__("END IF")
        self.counter = count

    def generate_code(self):
        return f"end_if_label_{self.counter}:"