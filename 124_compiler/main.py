from enum import Enum, auto
from lexer import Lexer
from parser import Parser
# from parser import Parser


# Example usage
# code = '''SPILL x SAYING "Input first number:"
# SPILL y SAYING "Input second number:"
# FLEX ("Sum of x and y is: ", x + y)
# '''

code="LET x = (7-6 / 15*5+6"

lexer = Lexer(code)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
parser = Parser(tokens)
ast = parser.parse()
print("\nAST:")
print(ast)
# print(repr(ast))
