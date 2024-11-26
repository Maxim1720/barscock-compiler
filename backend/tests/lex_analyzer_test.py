import abc
from abc import ABC, abstractclassmethod
from unittest import TestCase

from src import Analyzer
from src.analyzer.lexical.const import State
import unittest
from src.files import read_lexems, flush_out


def lexems_has(type, val)->bool:
    for l in read_lexems(type):
        if l == val:
            return True
    return False

class BaseTests:
    class BaseTest(unittest.TestCase):
        def __init__(self, code: str):
            flush_out()
            super().__init__('runTest')
            self.code = code
            self.analyzer = Analyzer(code)
            self.state = None

        def analyze(self):
            self.state = self.analyzer.analyze()

        def __del__(self):
            flush_out()

    class BaseIncorrectNumberTest(unittest.TestCase):
        def __init__(self, code: str):
            super().__init__('runTest')
            self.code = code
            self.analyzer = Analyzer(code)
            self.state = None

        def __del__(self):
            flush_out()

        def analyze(self):
            self.state = self.analyzer.analyze()

        def run_test(self):
            self.analyze()
            print(read_lexems('tn'))
            self.call_asserts()

        def call_asserts(self):
            self.assertIs(self.state, State.ERROR)
            self.assertIs(len(read_lexems("tn")), 0)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tw")), 0)
            self.assertIs(len(read_lexems("tl")), 0)


class TestExponenNumber(unittest.TestCase):
    def testWithoutSign(self):
        code = [
            "123e123",
        ]
        for c in code:
            flush_out()
            state = Analyzer(c).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")),1)
            flush_out()


    def test_with_delimiter(self):
        code = [
            "123e123;",
        ]
        for c in code:
            flush_out()
            state = Analyzer(c).analyze()
            self.assertIs(state, State.DELIMITER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("tl")), 1)
            flush_out()

    def test_with_bad_end(self):
        code = [
            "123e123z;",
        ]
        for c in code:
            flush_out()
            state = Analyzer(c).analyze()
            self.assertIs(state, State.ERROR)
            self.assertIs(len(read_lexems("tn")), 0)
            self.assertIs(len(read_lexems("tl")), 0)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()


class TestFromBinaryToDecimal(unittest.TestCase):
    code = "0189d"
    analyzer = Analyzer(code)

    def test(self):
        flush_out()
        self.analyzer.analyze()
        print(read_lexems('tw'))
        self.assertTrue(lexems_has("tn", self.code))
        self.assertIs(len(read_lexems("tn")), 1)
        self.assertIs(len(read_lexems("ti")), 0)
        self.assertIs(len(read_lexems("tw")), 0)
        self.assertIs(len(read_lexems("tl")), 0)

    def __del__(self):
        flush_out()


class TestFromBinaryToIncorrectSuffix(BaseTests.BaseTest):
    code = "0101z"

    def __init__(self, methodName='runTest'):
        super().__init__(self.code)  # Передача кода в BaseTest
        self._testMethodName = methodName  # Установка имени тестового метода


    def test(self):
        state = self.analyzer.analyze()
        self.assertTrue(not lexems_has("tn", self.code))
        print(read_lexems("tn"))
        self.assertIs(len(read_lexems("tn")), 0)
        self.assertIs(len(read_lexems("ti")), 0)
        self.assertIs(len(read_lexems("tw")), 0)
        self.assertIs(len(read_lexems("tl")), 0)
        self.assertIs(state, State.ERROR)



class TestRepeatHexEnd(BaseTests.BaseIncorrectNumberTest):
    code = "123abchh"

    def __init__(self, methodName='runTest'):
        super().__init__(self.code)
        self._testMethodName = methodName

    def test(self):
        self.run_test()


class TestRepeatBinaryEnd(BaseTests.BaseIncorrectNumberTest):
    code = "0101bb"

    def __init__(self, methodName='runTest'):
        super().__init__(self.code)
        self._testMethodName = methodName

    def test(self):
        self.run_test()
        self.assertFalse(lexems_has("tn", self.code))

class TestRepeatOctEnd(BaseTests.BaseIncorrectNumberTest):
    code = "234oo"

    def __init__(self, methodName='runTest'):
        super().__init__(self.code)
        self._testMethodName = methodName

    def test(self):
        self.run_test()


class TestRepeatDecEnd(BaseTests.BaseIncorrectNumberTest):
    code = "98989dd"

    def __init__(self, methodName='runTest'):
        super().__init__(self.code)
        self._testMethodName = methodName

    def test(self):
        self.run_test()

class TestCorrectExponentNumber(BaseTests.BaseTest):
    code = "01010e+2"
    def __init__(self, methodName='runTest'):
        super().__init__(self.code)
        self._testMethodName = methodName

    def test(self):
        self.analyze()
        self.assertIs(self.state, State.NUMBER)
        self.assertTrue(lexems_has("tn", self.code))
        self.assertIs(len(read_lexems("tn")), 1)
        self.assertIs(len(read_lexems("ti")), 0)
        self.assertIs(len(read_lexems("tw")), 0)
        self.assertIs(len(read_lexems("tl")), 0)

class TestNumber(unittest.TestCase):

    def test_dec_with_delimiter(self):
        codes = [
            "111;",
            "123;",
            "123:",
            "234;",
            "789;",
            "8989;",
            "1234567890;"
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(f"numbers: {read_lexems("tn")}")
            self.assertIs(state, State.DELIMITER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tl")), 1)
            flush_out()


    def test_from_binary_to_exponent_to_hex_is_success(self):
        codes = [
            "111eacdh",
            "111eh",
            "01010eddddddh"
        ]

        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems("ti"))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()

    def test_from_binary_to_hex_with_delimiter(self):
        codes = [
            "1111eacdh;",
            "1111eh;",
        ]

        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems("tl"))
            self.assertIs(state, State.DELIMITER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tl")), 1)
            flush_out()


    def test_from_binary_to_dec_without_suffix(self):
        codes = [
            "018",
            "1111"
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()

    def test_from_binary_to_oct_without_suffix(self):
        codes = [
            "027",
            "022",
            "0333",
            "01017"
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()

    def test_oct_with_incorrect_end(self):
        codes = [
            "027z",
            "022z",
            "0333z",
            "01017z"
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.ERROR)
            self.assertIs(len(read_lexems("tn")), 0)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()


    def test_hex_with_incorrect_end(self):
        codes = [
            "027abcdha",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(self._testMethodName, read_lexems('tn'))
            self.assertIs(state, State.ERROR)
            self.assertIs(len(read_lexems("tn")), 0)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tl")), 0)
            flush_out()


class TestIdentifier(unittest.TestCase):
    def test_with_digit_at_end_success(self):
        flush_out()
        code = "testIdentifier2"
        a = Analyzer(code)
        state = a.analyze()
        self.assertIs(state, State.IDENTIFIER)
        self.assertTrue(lexems_has('ti', code))
        self.assertIs(len(read_lexems("ti")), 1)
        self.assertIs(len(read_lexems("tn")), 0)
        flush_out()
    def test_with_digit_at_end_with_delimiter(self):
        flush_out()
        code = "testIdentifier2;"
        a = Analyzer(code)
        state = a.analyze()
        self.assertIs(state, State.DELIMITER)
        self.assertTrue(lexems_has('ti', "testIdentifier2"))
        self.assertIs(len(read_lexems("ti")), 1)
        self.assertIs(len(read_lexems("tn")), 0)

        flush_out()

    def test(self):
        flush_out()
        code = """
        g as 010101abh
    s as 2343o
    b as 0101b
    hex as 123abcd123h
    decFromBinary as 018
    decFromBinary2 as 018d
        """
        a = Analyzer(code)
        state = a.analyze()
        print(read_lexems('ti'))
        self.assertTrue(lexems_has("ti", 'g'))
        self.assertTrue(lexems_has("ti", 's'))
        self.assertTrue(lexems_has("ti", 'b'))
        self.assertTrue(lexems_has("ti", 'hex'))
        self.assertTrue(lexems_has("ti", 'decFromBinary'))
        self.assertTrue(lexems_has("ti", 'decFromBinary2'))
        self.assertIs(len(read_lexems('ti')), 6)
        flush_out()


class TestFloatNumber(unittest.TestCase):

    def test_from_b_to_float(self):
        codes = [
            "0101.123",
            "0101.456",
            "0101.956",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()


    def test_from_o_to_float(self):
        codes = [
            "2222.123",
            "2323.456",
            "6767.956",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()

    def test_exponent_float(self):
        codes = [
            "2222.123e+2",
            "2323.456e-5",
            "6767.956e9",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            flush_out()


    def test_exponent_incorrect_end(self):
        codes = [
            "2222.123e",
            "2323.456e",
            "6767.956e",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.ERROR)
            self.assertIs(len(read_lexems("tn")), 0)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tl")), 0)
            flush_out()

    def test_empty_after_dot(self):
        codes = [
            "2222.",
            "2323.",
            "6767.",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.ERROR)
            self.assertIs(len(read_lexems("tn")), 0)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tl")), 0)
            flush_out()

    def test_empty_before_dot(self):
        codes = [
            ".123",
            ".345.",
            ".6789",
        ]
        for code in codes:
            flush_out()
            state = Analyzer(code).analyze()
            print(read_lexems('tn'))
            self.assertIs(state, State.NUMBER)
            self.assertIs(len(read_lexems("tn")), 1)
            self.assertIs(len(read_lexems("ti")), 0)
            self.assertIs(len(read_lexems("tl")), 0)
            flush_out()

program = """
    program var a,b: int; c, d: float; e, f: bool; g: int;
    begin a as 5
    b as 7: e as 7.5e+575: d as c: e as true: f as false
    g as 010101abh
    s as 2343o
    b as 0101b
    hex as 123abcd123h
    decFromBinary as 018
    decFromBinary2 as 018d
    b as b min a
    if b LT a then a as a plus b else b as b min 5
    end.
    """

program2 = """
    program 
var 
    a, b, c: int; 
    c, d: float; 
    e, f: bool; 
    g, s, hex, decFromBinary, decFromBinary2: int;

begin
    a as 5;
    b as 7;
    e as 7.5e+575;
    d as c;
    e as true;
    f as false;
    g as 010101b;           
    s as 2343o;             
    b as 0101b;
    hex as 123ABCDh;        
    decFromBinary as 18;    
    decFromBinary2 as 18d;
    b as b min a;
    if b LT a then 
        a as a plus b 
    else 
        b as b min {
        12dwa3123123 comment
        12
        dwa
        awdaw
        dwad
        a
        daw
        dwa
        ferg
        reg
        rt
        ghtr
        h
        trh
        }  5;
        {123}
        {dwad wa dwa dwa dw}
        {
        
        dwadwadaw
        
        
        }
end.

    """

class TestDelimiter(unittest.TestCase):
    def test_only_dots(self):
        code = "...."
        flush_out()
        state = Analyzer(code).analyze()
        self.assertIs(state, State.ERROR)
        self.assertIs(len(read_lexems("tn")), 0)
        self.assertIs(len(read_lexems("ti")), 0)
        self.assertIs(len(read_lexems("tl")), 0)
        flush_out()

    def test_program(self):
        code = program2
        flush_out()
        state = Analyzer(code).analyze()
        self.assertIs(state, State.END)
        print(read_lexems('tl'))
        self.assertIs(len(read_lexems("tl")), 50)

    def test_lexems_has_binaries(self):
        # code = program2
        flush_out()
        state = Analyzer(program2).analyze()
        b = '010101b'

        has = False
        for i in read_lexems('tn'):
            if i == b:
                has = True
        self.assertTrue(has)
        flush_out()


if __name__ == '__main__':
    unittest.main()
