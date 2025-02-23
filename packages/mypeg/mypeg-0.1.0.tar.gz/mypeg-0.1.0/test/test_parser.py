import unittest
from mypeg.parser import PEGParser

class TestPEGParser(unittest.TestCase):
    def setUp(self):
        self.parser = PEGParser()

    def test_parse_simple_expression(self):
        result = self.parser.parse("3 + 5")
        self.assertIsNotNone(result)

    def test_parse_with_parentheses(self):
        result = self.parser.parse("(2 + 3) * 4")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
