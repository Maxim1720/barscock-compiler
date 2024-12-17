import unittest


class AssignTest(unittest.TestCase):
    def test_simple(self):
        a_as = AssignNode("a")
        b_var = IdentifierNode("b")

        a_as.add_input(b_var)


    def test_plus_min(self):
        instructions = [
            IdentifierNode("b"),
            MultNode("10"),
            DivNode("20"),
            AddNode("7"),
            MinNode("5"),
            AssignNode("a"),
        ]


        for i in instructions:
            print(i.generate_code())


class DefaultSectionsTest(unittest.TestCase):
    def test_simple(self):
        var_section = VarSectionNode()

        var_section.add_input(DefinitionNode('a', 'int'))
        var_section.add_input(DefinitionNode('b', 'float'))
        var_section.add_input(DefinitionNode('c', 'bool'))

        buffer_section = BufferSection()
        var_section.add_input(buffer_section)

        print(var_section.generate_code())
        self.assertEqual(var_section.generate_code(), """
global _start
section .data
a dd 0
b dq 0.0
c db 0
section .bss
buffer resb 32""")




if __name__ == '__main__':
    unittest.main()