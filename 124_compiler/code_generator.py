
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
        # print(node)
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
        elif isinstance(node, ConditionalNode):
            return self.visit_conditional(node)
        else:
            raise ValueError(f"Unknown node type: {node.type} {node}")

    def visit_number(self, node):
        reg = self.new_register()
        self.instructions.append(f"li {reg}, {node.value}")  # Load immediate value
        return reg

    def visit_string(self, node, assign=None):
        if not assign:
            label = f"str_{self.new_label()}"
            self.symbol_table[label] = f"{label}: .asciiz {node.value}"  # Allocate string in .data
            reg = self.new_register()
            self.instructions.append(f"la {reg}, {label}") 
        else: 
            # print(assign)
            label = f"{assign}"
            self.symbol_table[label] = f"{label}: .asciiz {node.value}"  # Allocate string in .data
            reg = ""
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
        if isinstance(node.value, StringNode):
            # print("here", node)
            result_reg = self.visit_string(node.value, node.identifier)
            # print(self.symbol_table)
        else:
            # Handle direct assignment
            # print(node.value)
            result_reg = self._generate_node(node.value)
            # print(result_reg)

        # Assign memory location for the variable if not already done
        if node.identifier not in self.symbol_table:
            self.symbol_table[node.identifier] = f"{node.identifier}_mem"

        # Store the value in the assigned memory location
        memory_location = self.symbol_table[node.identifier]
        if not memory_location.endswith('"'):
            self.instructions.append(f"sw {result_reg}, {memory_location}")
            # memory_location = memory_location.split(':')[0]
          # Store value into memory

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
                # Check for division by zero
            zero_check_label = self.new_label()
            end_label = self.new_label()
            label = f"div_by_zero_error"
            self.symbol_table[label] = f'{label}: .asciiz "Error: Division by zero."'

            # Check if right_reg is zero
            self.instructions.append(f"beqz {right_reg}, {zero_check_label}")
            self.instructions.append(f"div {left_reg}, {right_reg}")
            self.instructions.append(f"mflo {result_reg}")
            self.instructions.append(f"j {end_label}")

            # Division by zero error handling
            self.instructions.append(f"{zero_check_label}:")
            self.instructions.append(f'li $v0, 4')  # syscall for print string
            self.instructions.append(f'la $a0, div_by_zero_error')  # Load error message
            self.instructions.append(f'syscall')
            self.instructions.append(f'li $v0, 10')  # syscall for exit
            self.instructions.append(f'syscall')

            self.instructions.append(f"{end_label}:")
            
            
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
        # print(node, self.symbol_table) 
        
        if node.name not in self.symbol_table:
            raise ValueError(f"Variable '{node.name}' is not declared.")

        memory_location = self.symbol_table[node.name]
        # print(memory_location)

        # print(memory_location)
        self.instructions.append("li $v0, 5  # Syscall for reading integer")
        self.instructions.append("syscall")
        self.instructions.append(f"sw $v0, {memory_location}  # Store the input value in memory")

    def visit_print(self, node):
        # print("visit_print:", node, self.symbol_table)
        value_reg = None
        if isinstance(node.value, NumberNode):
            value_reg = self._generate_node(node.value)  # Generate code for the value to print

        if isinstance(node.value, StringNode):
            value_reg = self._generate_node(node.value)
        
        # Check the type of value and emit appropriate print syscalls
        if isinstance(node.value, VariableNode):
            # Handle variables (assumes memory is already allocated)
            variable = node.value
            # print("var", variable.identifier)
            if variable.identifier in self.symbol_table:
                # print("here", self.symbol_table)
                if self.symbol_table[variable.identifier].endswith('"'):
                    # Print string
                    self.instructions.append(f"la $a0, {self.symbol_table[variable.identifier].split(':')[0]} # Print string syscall")
                    self.instructions.append("li $v0, 4  # Print string syscall")
                else:
                    # Print integer
                    self.instructions.append(f"la $a0, {self.symbol_table[variable.identifier]} # Print integer syscall")
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

    def visit_conditional(self, node):
        # Visit the condition and generate code for it (e.g., x == 1)
        condition_code = self.visit_condition(node.condition)
        label_true = self.new_label()
        label_end = "END"+self.new_label()
        
        # Handle main IF condition
        if node.condition.operator == "==":
            self.instructions.append(f"beq {condition_code}, $zero, {label_true}")
        elif node.condition.operator == "!=":
            self.instructions.append(f"bne {condition_code}, $zero, {label_true}")
        else:
            raise ValueError(f"Unsupported operator in condition: {node.condition.operator}")
        if len(node.elif_branches) > 0:
            self.instructions.append(f"j NEXT0")
        if node.else_branch:
            self.instructions.append(f"j ELSE")
        self.instructions.append(f"j {label_end}") 
        # Handle TRUE branch (THEN)
        self.instructions.append(f"{label_true}:")
        self._generate_node(node.true_branch)  # Generate code for the true branch
        self.instructions.append(f"j {label_end}")  # Jump to the end after the true branch

        if len(node.elif_branches)>0:
            # Handle Elif branches
            i = 0  # Ensure i is initialized outside the loop
            
            for elif_branch in node.elif_branches:
                self.instructions.append(f"NEXT{i}:")
                condition_code = self.visit_condition(elif_branch[0])
                elif_label_true = "elif" + str(i)
                i += 1  # Increment i for each elif condition to get unique labels
                
                # Check the elif condition
                if elif_branch[0].operator == "==":
                    self.instructions.append(f"beq {condition_code}, $zero, {elif_label_true}")
                elif elif_branch[0].operator == "!=":
                    self.instructions.append(f"bne {condition_code}, $zero, {elif_label_true}")
                else:
                    raise ValueError(f"Unsupported operator in elif condition: {elif_branch[0].operator}")
                if i < len(node.elif_branches):
                    self.instructions.append(f"j NEXT{i}")
                else:
                    self.instructions.append(f"j ELSE")
                # Jump to END if elif condition is false
                # self.instructions.append(f"j {label_end}")  
                self.instructions.append(f"{elif_label_true}:")
                self._generate_node(elif_branch[1])  # Generate code for the elif true branch
                self.instructions.append(f"j {label_end}")  # Jump to the end after the elif true branch

        # Handle ELSE case (false branch) after all elif branches
        if node.else_branch:
            self.instructions.append(f"ELSE:")
            self._generate_node(node.else_branch)  # Generate code for the else branch
        self.instructions.append(f"j {label_end}")  # Jump to the end after the else branch

        # End of the entire conditional block
        self.instructions.append(f"{label_end}:")


    def visit_condition(self, node):
        # print(node)
        if isinstance(node.left, VariableNode):
            left_reg = self.load_variable(node.left.identifier)
        else:
            left_reg = self._generate_node(node.left)

        if isinstance(node.right, VariableNode):
            right_reg = self.load_variable(node.right.identifier)
        else:
            right_reg = self._generate_node(node.right)

        result_reg = self.new_register()
        self.instructions.append(f"sub {result_reg}, {left_reg}, {right_reg}")
        
        return result_reg

        
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
