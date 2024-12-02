import subprocess
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

def run_qtspim_with_gui(asm_file):
    qtspim_path = "C:/Users/Dongkor/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/QtSpim"  # Example for Windows

    # Command to run QTSPIM in headless mode (without GUI)
    command = [qtspim_path, "-file", asm_file]  # Load the assembly file

    try:
        # Launch QTSPIM in console mode
        subprocess.run(command)
        print("QTSPIM console started with the given assembly file.")
    except Exception as e:
        print(f"Error launching QTSPIM: {e}")



class compiler:
    def __init__(self, code):
        self.code = code
        self.memory = {}

    def compile(self):
        # lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # for token in tokens:
        #     print(token)
        # parser
        parser = Parser(tokens)
        ast = parser.parse()
        print("\nAST:")
        print(ast)

        # code generator
        generator = CodeGenerator()
        generator.generate(ast)

        # running MARS
        asm = generator.get_data() + generator.get_code()  + generator.exit()
        # print(asm)
        with open("output.asm", "w") as file:
            file.write(asm)
        run_mars("output.asm")
        # print(output)


code = '''INT x;
INT y;
FLEX "Enter first num:";
SPILL x;
FLEX "Enter second num:";
SPILL y;
INT res = x + y;
FLEX "The sum is:";
FLEX res;
STR h ="hi";
FLEX h;
FLEX "Hello world!";
'''

processed_code = compiler(code)
processed_code.compile()

# print(processed_code.memory)

# for token in tokens:
#     print(token)


# print("\nAST:")
# print(ast)
# print(repr(ast))

# Generate the assembly code using your code generator


# Get the generated assembly code

# print("Generated Assembly Code:")
# print(asm)


# Save the assembly code to a file


# print("Assembly code saved to 'output.asm'")

# Run the generated assembly code in MARS and capture the output

# print(lines)

# print("MARS Output:\n", lines, variables)
