import re

from ply.lex import LexToken
from ply.yacc import YaccProduction

from .exceptions import AlreadyExistsError
from .identifiers import *
from ..semantic.expression import Expression, TypeChecker, NumberTypeParser
from ..semantic.identifier import IdChecker, AssignmentChecker, IdentifierChecker
from ..translator.node.arithmetic import MultNode, DivNode, AndNode, AddNode, MinNode, OrNode
from ..translator.node.boolean_operations import LTNode, GTNode, LENode, GENode, NEQNode, EQNode
from ..translator.node.default import UtilsFuncsNode
from ..translator.node.id import IdentifierNode, DefinitionNode, VarSectionNode, AssignNode, BufferSection
from ..translator.node.node import Node, ValueNode, TextSectionNode, EndNode
from ..translator.node.operator.condition import IfNode, ElseNode, EndIfNode, ThenEndNode, ElseEndNode
from ..translator.node.operator.io import ReadNode, WriteNode
from ..translator.node.operator.loop.for_loop import ForAssignNode, ForToNode, ForConditionNode, ForIncrementNode, \
    ForEndNode, ForLoopNode
from ..translator.node.operator.loop.while_loop import WhileLoopNode, WhileEndNode, WhileConditionNode
from src import debug

from src.analyzer.lex import *

start = '_P'

instructions: list[Node] = []


def p_error(p: LexToken):
    if p is None:
        print("Syntax error end of input'")
    else:
        print(f"Syntax error at {p} ")


def p_p(p):
    """_P : PROGRAM _D _B DOT"""
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    lol = instructions
    with open('output.asm', 'w') as f:
        for i in instructions:
            f.write(i.generate_code()+'\n')
        # print(i.generate_code())


def p_b(p):
    """_B : BEGIN _O END"""
    p[0] = f'{p[1]} {p[2]} {p[3]}'
    instructions.append(
        EndNode()
    )


def p_d(p):
    """
    _D : VAR D1
    | VAR
    """
    p[0] = p[1]
    instructions.append(BufferSection())
    instructions.append(VarSectionNode())
    for i in founded:
        instructions.append(DefinitionNode(i.name, i.type))
    instructions.append(TextSectionNode())
    instructions.append(UtilsFuncsNode())



def p_d1_rec(p):
    """D1 : _I D1"""
    p[0] = f'{p[1]} {p[2]}'


def p_d1(p):
    """D1 : _I"""
    p[0] = p[1]


def p_i(p):
    """_I : I1 COLON _T SEMICOLON"""
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    ids = re.split(r'[ \t,]+', p[1])
    for i in ids:
        add_id(
            Identifier(name=i, type=p[3])
        )
    for i in founded:
        if i.count > 1:
            raise AlreadyExistsError(f"Identifier '{i.name}' already exists")

    if debug:
        print(f'ids: {[f.name for f in founded]}')


def p_i1(p):
    """I1 : I2"""
    p[0] = p[1]


def p_i1_comma(p):
    """I1 : I1 COMMA I2"""
    p[0] = f'{p[1]}{p[2]}{p[3]}'


def p_i2(p: YaccProduction):
    """I2 : ID"""
    p[0] = p[1]


def p_o(p):
    """_O : O1"""
    p[0] = p[1]


def p_os(p):
    """_O : O1 SEMICOLON _O"""
    p[0] = f'{p[1]}{p[2]}{p[3]}'


def p_o_empty(p):
    """_O : """
    pass


def p_o2(p):
    """
    O2 : _S
    """
    l = p[1]
    p[0] = p[1]


def p_s(p):
    """
    _S : O1
    """
    l = p[1]
    p[0] = p[1]


def p_s_rec(p):
    """_S : _S S1 O1"""
    p[0] = f'{p[1]} {p[3]}'
    p[0] = {
        'nodes': p[1]['nodes']
    }
    temp = p[0]
    p[0]['nodes'].extend(p[3]['nodes'])


def p_o1(p):
    """
    O1 : _A
    | _F
    | _W
    | _Y
    | _U
    | _V
    """
    p[0] = p[1]
    if debug:
        print(f"O1: {p[0]}")
    for i in p[1]['nodes']:
        instructions.append(i)


def p_s1(p):
    """
    S1 : COLON
    """
    p[0] = p[1]


def p_a(p):
    """
    _A : I2 AS _E
    """
    p[0] = f'{p[1]} {p[2]} {p[3].value}'
    IdChecker(p[1]).check()
    AssignmentChecker().check(p[1], p[3].type)

    p[0] = {
        "nodes": []
    }
    p[0]['nodes'].append(AssignNode(p[1]))


if_counter = 0


def p_f(p):
    """
    _F : F1 ELSE O2
    """
    p[0] = f'{p[1]} {p[2]} {p[3]}'
    p[0] = {
        "nodes": p[1]['nodes']
    }
    global if_counter
    p[0]['nodes'].append(ElseNode(if_counter))
    p[0]['nodes'].extend(p[3]['nodes'])
    p[0]['nodes'].append(ElseEndNode(if_counter))
    p[0]['nodes'].append(EndIfNode(if_counter))

    if_counter += 1


def p_f_f1(p):
    """_F : F1"""
    p[0] = p[1]


def p_f1(p):
    """
    F1 : IF _E THEN O2
    """
    global if_counter
    p[0] = f'{p[1]} {p[2].value} {p[3]} {p[4]}'
    if debug:
        print(f'F1: {p[0]}')

    if p[2].type != 'bool':
        raise TypeError(f"Type error: {p[2]} != bool at if statement")

    p[0] = {
        "nodes": [IfNode(if_counter)]
    }
    p[0]['nodes'].extend(p[4]['nodes'])
    p[0]['nodes'].append(ThenEndNode(if_counter))
    # w = p[0]
    if debug:
        print(f"F1: {p[0]}")

for_counter = 0
def p_w(p):
    """_W : FOR _A TO _E DO O2 """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}'

    global for_counter
    p[0] = {
        "nodes": [
            *p[2]['nodes'],
            ForAssignNode(),
            # *p[4]['nodes'],
            ForToNode(),
            ForLoopNode(for_counter),
            ForConditionNode(for_counter),
            *p[6]['nodes'],
            ForIncrementNode(for_counter),
            ForEndNode(for_counter),
        ]
    }
    for_counter += 1

while_counter = 0

def p_y(p):
    """
    _Y : WHILE _E DO O2
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    if debug:
        print(f"Y: {p[0]}")

    if p[2].type != 'bool':
        raise TypeError(f"Type error: {p[2]} != bool at while statement")

    global while_counter
    p[0] = {
        "nodes": [
            ForAssignNode(),
            WhileLoopNode(while_counter),
            WhileConditionNode(while_counter),
            *p[4]['nodes'],
            WhileEndNode(while_counter)
        ]
    }
    while_counter += 1


def p_u(p):
    """
    _U : READ LPAREN I1 RPAREN
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    IdChecker(p[3]).check()
    if debug:
        print(f"READ: {p[0]}")

    p[0] = {
        "nodes": []
    }
    for i in re.split(",", p[3]):
        p[0]['nodes'].append(ReadNode(i))


def p_v(p):
    """
    _V : WRITE LPAREN E1 RPAREN
    """
    p[0] = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    p[0] = {
        "nodes": []
    }

    # for i in re.split(",", p[3].value):

    p[0]['nodes'].append(WriteNode(p[3].value))


def p_e1(p):
    """E1 : E1 COMMA _E
    | _E
    """
    if len(p) > 2:
        p[0] = f'{p[1]} {p[2]} {p[3]}'
        # p[0] = {
        #     'nodes': p[1]['nodes'].extend(p[3]['nodes'])
        # }
    else:
        l = p[1]
        p[0] = p[1]

        # p[0] = {
        #     "nodes": p[1]['nodes']
        # }


##
# Выражение должно возвращать тип и получившееся выражение
# type and value
# это нужно для семантического анализа
# но что делать с элементами выражения? в них тоже нужно вычислять тип
# только тип
# #


def p_e(p):
    """
    _E : _Z
    """
    # p[0] = to_typed_value(p[1])
    # print(f"E: {p[0]}")
    p[0] = p[1]


def p_e_rec(p):
    """_E : _E Z1 _Z"""
    p[0] = f"{p[1].value} {p[2]} {p[3].value}"
    p[0] = Expression(TypeChecker().compare(p[1].type, p[3].type, p[2]), p[0])

    sign = {
        "LT": LTNode,
        "GT": GTNode,
        "LE": LENode,
        "GE": GENode,
        "NEQ": NEQNode,
        "EQ": EQNode,
    }

    left = p[1].value
    right = p[3].value

    instructions.append(
        ValueNode(left) if not IdentifierChecker(left).exists() else IdentifierNode(left)
    )
    instructions.append(
        sign[p[2]](f'[{right}]' if IdentifierChecker(right).exists() else right)
    )


def p_z(p):
    """_Z : _J"""
    p[0] = p[1]
    if debug:
        print(f"Z: {[f for f in p]}")


def p_z_rec(p):
    """_Z : _Z J1 _J"""
    p[0] = f"{p[1].value} {p[2]} {p[3].value}"
    p[0] = Expression(TypeChecker().compare(p[1].type, p[3].type, p[2]), p[0])

    sign = {
        "plus": AddNode,
        "min": MinNode,
        "or": OrNode,
    }

    instructions.append(
        sign[p[2]](p[3].value)
    )
    if debug:
        print(f"Z rec: {p[0]}")


def p_j(p):
    """_J : _M"""
    p[0] = p[1]
    if debug:
        print(f"J: {p[0]}")


def p_j_rec(p):
    """_J : _J M1 _M"""
    p[0] = f"{p[1].value} {p[2]} {p[3].value}"
    # p[0] = eval(p[0])
    if debug:
        print(f"rec J: {p[0]}")
    p[0] = Expression(TypeChecker().compare(p[1].type, p[3].type, p[2]), p[0])

    sign = {
        'mult': MultNode,
        'div': DivNode,
        'and': AndNode
    }
    instructions.extend([
        sign[p[2]](p[3].value)
    ])


def p_m1(p):
    """
    M1 : MULT
       | DIV
       | AND
    """
    sign = {
        'mult': '*',
        'div': '/',
        'and': '&',
    }
    # p[0] = sign[p[1]]
    p[0] = p[1]
    if debug:
        print(f"M1: p[1]={p[1]}")


def p_j1(p: YaccProduction):
    """
    J1 : PLUS
       | MIN
       | OR
    """
    p[0] = p[1]


def p_z1(p):
    """
    Z1 : NEQ
       | EQ
       | LT
       | LE
       | GT
       | GE
    """
    if debug:
        print(f"Z1: {[f for f in p]}")
    op = {
        'NEQ': '!=',
        "EQ": "==",
        "LT": "<",
        "LE": "<=",
        "GT": ">",
        "GE": ">=",
    }
    p[0] = p[1]


def p_m(p):
    """
    _M : _N
      | _L
      | NOT_M
      | PAREN_M
    """
    p[0] = p[1]
    if debug:
        print(f"M: p[1]={p[1]}")


def p_id(p):
    """_M : I2"""
    IdChecker(p[1]).check()
    _id = get_id_by_name(p[1])
    if debug:
        print(f"ID in expression: {_id}")
    p[0] = _id.type
    p[0] = Expression(p[0], p[1])

    instructions.append(IdentifierNode(p[1]))


def p_not_m(p):
    """
    NOT_M : NOT _M
    """
    if p[2].type != 'bool':
        raise TypeError(f"Expected: bool. Got type: {p[2]}'")

    bools = {
        "true": 1,
        "false": 0
    }

    p[0] = Expression('bool', f'{p[1]}{bools[p[2].value]}')


def p_paren_m(p):
    """
    PAREN_M : LPAREN _E RPAREN
    """
    p[0] = Expression(p[2].type, p[2].value)


def p_l(p):
    """
    _L : TRUE
      | FALSE
    """
    # p[0] = f'{p[1][:1].upper()}{p[1][1:]}'
    p[0] = Expression('bool', p[1])

    instructions.append(
        ValueNode(p[1])
    )


def p_n(p):
    """_N : NUMBER"""
    p[0] = 'int'
    n: str = p[1]
    if debug:
        print(f'value parse : {p[1]}')
    p[0] = Expression(NumberTypeParser(n).get_value_type(), p[1])
    if debug:
        print(f'number: {p[0]}')

    instructions.append(ValueNode(p[1]))


def p_t(p):
    """
    _T : INT
      | FLOAT
      | BOOL
    """
    p[0] = p[1]


import ast


def to_typed_value(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value
