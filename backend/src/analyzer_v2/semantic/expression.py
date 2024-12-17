import re
from dataclasses import dataclass



@dataclass
class Expression:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []

    def __repr__(self):
        return f"Expr({self.type}, {self.value})"

types = {

    #int
    ('int', 'int', 'plus') : 'int',
    ('int', 'int', 'min') : 'int',
    ('int', 'int', 'mult') : 'int',
    ('int', 'int', 'div') : 'int',


    #float
    ('float', 'float', 'plus') : 'float',
    ('float', 'float', 'min') : 'float',
    ('float', 'float', 'mult') : 'float',
    ('float', 'float', 'div') : 'float',

    # float from int
    ('float', 'int', 'plus') : 'float',
    ('float', 'int', 'min') : 'float',
    ('float', 'int', 'mult') : 'float',
    ('float', 'int', 'div') : 'float',

    ('int', 'float', 'plus') : 'float',
    ('int', 'float', 'min') : 'float',
    ('int', 'float', 'mult') : 'float',
    ('int', 'float', 'div') : 'float',


    # bool
    ('bool', 'bool', 'and') : 'bool',
    ('bool', 'bool', 'or') : 'bool',

    ('bool', '~bool', 'and'): 'bool',
    ('bool', '~bool', 'or'): 'bool',

    ('~bool', '~bool', 'and'): 'bool',
    ('~bool', '~bool', 'or'): 'bool',

    ('~bool', 'bool', 'and'): 'bool',
    ('~bool', 'bool', 'or'): 'bool',

    ('bool', '~bool', 'and'): 'bool',
    ('bool', '~bool', 'or'): 'bool',


    ('bool', '~bool', 'as'): 'bool',

    ('int', 'int', 'LT'): 'bool',
    ('int', 'int', 'LE'): 'bool',
    ('int', 'int', 'GT'): 'bool',
    ('int', 'int', 'GE'): 'bool',
    ('int', 'int', 'EQ'): 'bool',
    ('int', 'int', 'NEQ'): 'bool',

    ('float', 'float', 'LT'): 'bool',
    ('float', 'float', 'LE'): 'bool',
    ('float', 'float', 'GT'): 'bool',
    ('float', 'float', 'GE'): 'bool',
    ('float', 'float', 'EQ'): 'bool',
    ('float', 'float', 'NEQ'): 'bool',

    ('int', 'float', 'LT'): 'bool',
    ('int', 'float', 'LE'): 'bool',
    ('int', 'float', 'GT'): 'bool',
    ('int', 'float', 'GE'): 'bool',
    ('int', 'float', 'EQ'): 'bool',
    ('int', 'float', 'NEQ'): 'bool',

    ('float', 'int', 'LT'): 'bool',
    ('float', 'int', 'LE'): 'bool',
    ('float', 'int', 'GT'): 'bool',
    ('float', 'int', 'GE'): 'bool',
    ('float', 'int', 'EQ'): 'bool',
    ('float', 'int', 'NEQ'): 'bool',



 }


class TypeChecker:
    def compare(self, left, right, operator) -> str:
        return types[(left, right, operator)]


class NumberTypeParser:
    def __init__(self, _value):
        self.value = _value

    def get_value_type(self) -> str:
        _type = 'int'

        print(f'value is : {self.value}' )

        if re.fullmatch(r"\d+[bBoO]", self.value):
            pass
            suffix = self.value[-1].lower()
            base = {
                'h': 16,
                'o': 8,
                'b': 2,
            }
            # p[0] = int(f"0{suffix}{n[:-1]}", base[suffix])
        elif re.fullmatch(r"\d+[dD]", self.value):
            pass
            # p[0] = int(n[:-1])
        elif re.fullmatch(r"[\dA-Fa-f]+[hH]", self.value):
            pass
            # p[0] = int(n[:-1], 16)
        elif '.' in self.value:
            _type = 'float'

        return _type
