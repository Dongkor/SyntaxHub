
from ast_1 import *

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
        elif isinstance(node, VariableNode):
            return self.visit_variable(node)
        elif isinstance(node, AssignmentNode):
            return self.visit_assignment(node)
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def visit_number(self, node):
        reg = self.new_register()
        self.instructions.append(f"li {reg}, {node.value}")  # Load immediate value
        return reg

    def visit_variable(self, node):
        if node.name not in self.symbol_table:
            raise ValueError(f"Undefined variable: {node.name}")
        return self.symbol_table[node.name]

    def visit_assignment(self, node):
        # Generate code for the value on the right-hand side
        value_reg = self._generate_node(node.value)

        # Assign a memory location for the variable if not already done
        if node.identifier not in self.symbol_table:
            self.symbol_table[node.identifier] = f"{node.identifier}_mem"

        # Store the value in the assigned memory location
        memory_location = self.symbol_table[node.identifier]
        self.instructions.append(f"sw {value_reg}, {memory_location}")  # Store value into memory

        return value_reg

    def visit_binary_op(self, node):
        left_reg = self._generate_node(node.left)
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

    def get_code(self):
        code = ".text\n"
        # data.join(self.instructions)
        for instruction in self.instructions:
            code += instruction + "\n"
        return code
    
    def get_data(self):
        data = ".data\n"
        variables = self.symbol_table.items()
        for variable in variables:
            data += variable[1] + ": .word 0" + "\n"
        return data
