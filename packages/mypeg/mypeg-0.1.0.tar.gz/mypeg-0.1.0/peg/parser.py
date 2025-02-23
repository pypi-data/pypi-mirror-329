from lark import Lark

PEG_GRAMMAR = """
    start: expr
    expr: term (("+"|"-") term)*
    term: factor (("*"|"/") factor)*
    factor: NUMBER | "(" expr ")"
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

class PEGParser:
    def __init__(self):
        self.parser = Lark(PEG_GRAMMAR, parser="earley")

    def parse(self, expression):
        return self.parser.parse(expression)
