from lark import Lark

pyeg_GRAMMAR = """
    start: expr
    expr: term (("+"|"-") term)*
    term: factor (("*"|"/") factor)*
    factor: NUMBER | "(" expr ")"
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


class pyegParser:
    def __init__(self):
        self.parser = Lark(pyeg_GRAMMAR, parser="earley")

    def parse(self, expression):
        return self.parser.parse(expression)
