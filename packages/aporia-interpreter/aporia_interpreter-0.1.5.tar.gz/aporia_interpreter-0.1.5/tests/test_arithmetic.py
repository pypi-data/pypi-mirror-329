import unittest
import aporia.parser.parser as parser
import aporia.interpreter as interpreter

def interpret(source:str):
    ast = parser.parse(source)
    return interpreter.InterpLcfi().interp(ast)


class TestArithmetic(unittest.TestCase):
    def test_order_of_operations(self):
        source = """
        true: print("", 1 - (3 + 2) * 2)
        """
        self.assertEqual('-9', interpret(source))  # add assertion here

    def test_float(self):
        source = """
        true: print("", 0.1 + 0.8)
        """
        self.assertEqual('0.9', interpret(source))  # add assertion here


if __name__ == '__main__':
    unittest.main()
