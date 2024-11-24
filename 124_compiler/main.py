from enum import Enum, auto
from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator
# from parser import Parser


# Example usage
# code = '''SPILL x SAYING "Input first number:"
# SPILL y SAYING "Input second number:"
# FLEX ("Sum of x and y is: ", x + y)
# '''

code = '''LET x = 1+2;
LET y = 2+2;
'''

lexer = Lexer(code)
tokens = lexer.tokenize()
# for token in tokens:
#     print(token)
parser = Parser(tokens)
ast = parser.parse()
# print("\nAST:")
# print(ast)
# print(repr(ast))
generator = CodeGenerator()
generator.generate(ast)

asm = generator.get_data() + generator.get_code()
print(asm)

# Save the assembly code to a file
with open("output.asm", "w") as file:
    file.write(asm)

print("Assembly code saved to 'output.asm'")