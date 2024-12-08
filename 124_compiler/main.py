import subprocess
import sys
import os
from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator



def run_mars(asm_file):
    # Path to Mars.jar (update this to your actual path)
    mars_path = "C:/Users/Dongkor/Downloads/Mars4_5.jar"
    
    # Run the subprocess and capture the output
    command = ["java", "-jar", mars_path, "sm", asm_file]

    try:
        # Run MARS in headless mode with the assembly file
        subprocess.run(command, check=True)
        print("MARS console executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing MARS: {e}")



class compiler:
    def __init__(self, code, text_file, compile_only):
        self.code = code
        self.memory = {}
        self.text_file = text_file
        self.compile_only = compile_only

    def compile(self):
        # lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # for token in tokens:
        #     print(token)
        parser = Parser(tokens)
        ast = parser.parse()
        # print("\nAST:")
        # print(ast)

        # code generator
        generator = CodeGenerator()
        generator.generate(ast)

        # running MARS
        asm = generator.get_data() + generator.get_code()  + generator.exit()
        output_dir = os.path.dirname(self.text_file)
        output_filename = os.path.splitext(os.path.basename(self.text_file))[0] + ".asm"
        output_path = os.path.join(output_dir, output_filename)
        # print(output_path)
        with open(output_path, "w") as file:
            file.write(asm)
        if not self.compile_only:
            run_mars(output_path)
        else:
            print(output_filename + " has been created successfully!\n\nContent:\n", asm)


# print('Hi')

text_file = sys.argv[1]
compile_only = ''
# print(len(sys.argv))
if len(sys.argv) == 3 and sys.argv[2] == "yes":
    compile_only = sys.argv[2]
with open(text_file, "r") as file:
    file_contents = file.read()

code = file_contents

# print(compile_only)

processed_code = compiler(code, text_file, compile_only)
processed_code.compile()

