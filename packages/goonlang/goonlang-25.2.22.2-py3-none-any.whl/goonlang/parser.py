from lark import Lark

class Parser:

    def __init__(self, code, grammar):
        self.parser = Lark.open(grammar)
        self.code = self.parser.parse(code)