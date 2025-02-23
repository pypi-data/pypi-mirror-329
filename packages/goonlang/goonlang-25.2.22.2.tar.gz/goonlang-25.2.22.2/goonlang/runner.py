from lark import Transformer
from goonlang.parent import Parent

class Runner(Transformer):
    def __init__(self, parser):
        self.parser = parser
        self.vars = {}

    def code_block(self, block):
        pass

    def function(self, func):
        if func[0] == "print":
            print(func[1])
            return None
        return None

    def string(self, s):
        (s,) = s
        return s[1:-1]
    
    def number(self, n):
        (n,) = n
        return n
    
    def declaration(self, dec):
        self.vars[dec[0]] = dec[1]
        return dec[1]
    
    def value(self, val):
        if hasattr(val[0], "data"):
            if val[0].data=="variable":
                return self.vars[val[0].children[0]]
        return val[0]

    def term(self, val):
        if val[0].data=="variable":
            if type(self.vars[val[0].children[0]]) == int or type(self.vars[val[0].children[0]]) == float:
                pass
            else:
                return self.vars[val[0].children[0]]
            
    def sum(self, val):
        return int(val[0]) + int(val[1])
    
    def difference(self, val):
        return int(val[0]) - int(val[1])
        


    # entry point stuffsss
    def run(self, code):
        #print(code.pretty())
        parenter = Parent()
        parenter.visit(code)
        self.transform(code)



# old code, might need later
""" 
    def run(self):
        print(self.parser.code.pretty())
        for inst in self.parser.code.children:
            self.run_instruction(inst)

    def run_instruction(self, inst):
        if inst.data == "function":
            type, value = inst.children
            print(value)
"""
