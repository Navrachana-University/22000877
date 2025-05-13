from lexer import tokenize
from parser import Parser
from interpreter import Environment

with open("program.brainrot", "r") as f:
    code = f.read()

tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()

env = Environment()
env.eval(ast)
