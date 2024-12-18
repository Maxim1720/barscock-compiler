from src.analyzer.translator.node.node import Node, register_prefix, register

compare_result_register = "al"

class __CompareNode(Node):
    def __init__(self, val):
        super().__init__("COMPARE")
        self.val = val

    def generate_code(self):
        return f"mov {register_prefix}bx, {self.val}\ncmp {register}, {register_prefix}bx"


class LTNode(__CompareNode):
    def __init__(self, val):
        super().__init__(val)

    def generate_code(self):
        return super().generate_code() + f"\nsetl {compare_result_register}"


class GTNode(__CompareNode):
    def __init__(self, val):
        super().__init__(val)

    def generate_code(self):
        return super().generate_code() + f"\nsetg {compare_result_register}"


class GENode(__CompareNode):
    def __init__(self, val):
        super().__init__(val)

    def generate_code(self):
        return super().generate_code() + f"\nsetge {compare_result_register}"


class LENode(__CompareNode):
    def __init__(self, val):
        super().__init__(val)

    def generate_code(self):
        return super().generate_code() + f"\nsetle {compare_result_register}"


class NEQNode(__CompareNode):
    def __init__(self, val):
        super().__init__(val)

    def generate_code(self):
        return super().generate_code() + f"\nsetne {compare_result_register}"


class EQNode(__CompareNode):
    def __init__(self, val):
        super().__init__(val)

    def generate_code(self):
        return super().generate_code() + f"\nsete {compare_result_register}"


