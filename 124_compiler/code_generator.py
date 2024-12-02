
from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.instructions = []  # Stores the generated assembly code
        self.register_count = 0  # For managing registers dynamically
        self.label_count = 0  # For unique labels
        self.symbol_table = {}  # Maps variables to registers or memory

    def new_register(self):
        reg = f"$t{self.register_count}"
        self.register_count = (self.register_count + 1) % 10  # Limit to $t0-$t9
        return reg

    def new_label(self):
        label = f"label{self.label_count}"
        self.label_count += 1
        return label

    def generate(self, nodes):
        if isinstance(nodes, list):
            for node in nodes:  # Iterate over all AST nodes
                self._generate_node(node)
        else:
            self._generate_node(nodes)  # Handle single node (if needed)

    def _generate_node(self, node):
        if isinstance(node, NumberNode):
            return self.visit_number(node)
        elif isinstance(node, StringNode):
            return self.visit_string(node)
        elif isinstance(node, InputNode):
            return self.visit_input(node)
        elif isinstance(node, PrintNode):
            return self.visit_print(node)
        elif isinstance(node, VariableNode):
            return self.visit_variable(node)
        elif isinstance(node, AssignmentNode):
            return self.visit_assignment(node)
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)} {node.value}")

    def visit_number(self, node):
        reg = self.new_register()
        self.instructions.append(f"li {reg}, {node.value}")  # Load immediate value
        return reg

    def visit_string(self, node):
        label = f"str_{self.new_label()}"
        self.symbol_table[label] = f"{label}: .asciiz {node.value}"  # Allocate string in .data
        reg = self.new_register()
        self.instructions.append(f"la {reg}, {label}")  # Load address of string
        return reg


    def visit_variable(self, node):
        if node.identifier in self.symbol_table:
            raise ValueError(f"Variable '{node.identifier}' is already declared.")
    
        if node.datatype == "INT":
            memory_location = f"{node.identifier}_mem"
            self.symbol_table[node.identifier] = memory_location # Reserve space for an integer

        elif node.datatype == "STR":
            memory_location = f"{node.identifier}_mem"
            self.symbol_table[node.identifier] = memory_location # Reserve space for an integer

        else:
            raise ValueError(f"Unsupported type '{node.datatype}' for declaration.")
        

        # return self.symbol_table[node.identifier]

    def visit_assignment(self, node):
        if isinstance(node.value, BinaryOpNode):
            # Handle expressions
            result_reg = self.visit_binary_op(node.value)
        else:
            # Handle direct assignment
            result_reg = self._generate_node(node.value)

        # Assign memory location for the variable if not already done
        if node.identifier not in self.symbol_table:
            self.symbol_table[node.identifier] = f"{node.identifier}_mem"

        # Store the value in the assigned memory location
        memory_location = self.symbol_table[node.identifier]
        self.instructions.append(f"sw {result_reg}, {memory_location}")  # Store value into memory

        return result_reg

    def visit_binary_op(self, node):
        if isinstance(node.left, VariableNode):
            left_reg = self.load_variable(node.left.identifier)
        else:
            left_reg = self._generate_node(node.left)

        if isinstance(node.right, VariableNode):
            right_reg = self.load_variable(node.right.identifier)
        else:
            right_reg = self._generate_node(node.right)
        
        
        result_reg = self.new_register()

        if node.operator == "+":
            self.instructions.append(f"add {result_reg}, {left_reg}, {right_reg}")
        elif node.operator == "-":
            self.instructions.append(f"sub {result_reg}, {left_reg}, {right_reg}")
        elif node.operator == "*":
            self.instructions.append(f"mul {result_reg}, {left_reg}, {right_reg}")
        elif node.operator == "/":
            self.instructions.append(f"div {result_reg}, {left_reg}\nmflo {result_reg}")  # Division result in $lo
        else:
            raise ValueError(f"Unsupported operator: {node.operator}")

        return result_reg
    
    def load_variable(self, identifier):
        """
        Load the value of a variable from memory into a register.
        """
        if identifier not in self.symbol_table:
            raise ValueError(f"Variable '{identifier}' is not declared.")

        memory_location = self.symbol_table[identifier]
        
        # Generate a new register and load the variable value from memory
        reg = self.new_register()
        self.instructions.append(f"lw {reg}, {memory_location}")  # Load value from memory to register
        return reg
    
    def visit_input(self, node):
        # print(node, self.symbol_table) #implement this please
        
        if node.name not in self.symbol_table:
            raise ValueError(f"Variable '{node.name}' is not declared.")

        memory_location = self.symbol_table[node.name]

        # print(memory_location)
        self.instructions.append("li $v0, 5  # Syscall for reading integer")
        self.instructions.append("syscall")
        self.instructions.append(f"sw $v0, {memory_location}  # Store the input value in memory")

    def visit_print(self, node):
        print("visit_print:", node, self.symbol_table)
        value_reg = None
        if isinstance(node.value, NumberNode):
            value_reg = self._generate_node(node.value)  # Generate code for the value to print

        if isinstance(node.value, StringNode):
            value_reg = self._generate_node(node.value)
        
        # Check the type of value and emit appropriate print syscalls
        if isinstance(node.value, VariableNode):
            # Handle variables (assumes memory is already allocated)
            variable = node.value
            print("var", variable.identifier)
            if variable.identifier in self.symbol_table:
                if self.symbol_table[variable.identifier].endswith(".asciiz"):
                    # Print string
                    self.instructions.append(f"la $a0, {self.symbol_table[variable.identifier].split(':')[0]} # Print string syscallyow")
                    self.instructions.append("lw $a0, 0($a0)  # Load value from memory1")
                    self.instructions.append("li $v0, 4  # Print string syscall")
                else:
                    # Print integer
                    self.instructions.append(f"la $a0, {self.symbol_table[variable.identifier]} # Print integer syscallyow")
                    self.instructions.append("lw $a0, 0($a0)  # Load value from memory")
                    self.instructions.append("li $v0, 1  # Print integer syscall")
            else:
                raise ValueError(f"Undefined variable: {variable.identifier}")
        else:
            # For literals or computed expressions, the value is already in a register
            if isinstance(node.value, NumberNode):
                self.instructions.append("li $v0, 1  # Print integer syscall")
                self.instructions.append(f"move $a0, {value_reg}")
            elif isinstance(node.value, StringNode):
                self.instructions.append("li $v0, 4  # Print string syscall")
                self.instructions.append(f"move $a0, {value_reg}")

        # Trigger syscall
        self.instructions.append("syscall")

        # Print a newline after output for better formatting
        self.instructions.append("la $a0, newline")
        self.instructions.append("li $v0, 4  # Print newline syscall")
        self.instructions.append("syscall")


    def get_code(self):
        code = "\n.text\n"
        # data.join(self.instructions)
        for instruction in self.instructions:
            code += instruction + "\n"
        return code
    
    def get_data(self):
        data = "\n.data\n"
        data += "newline: .asciiz \"\\n\"\n"
        for variable, memory_location in self.symbol_table.items():
            # print(memory_location)
            if memory_location.endswith('"'):
                data += memory_location + "\n"
            else:
                data += f"{memory_location}: .word 0\n"
        return data

    
    def exit(self):
        return "\n# Exit program\nli $v0, 10\nsyscall\n"
