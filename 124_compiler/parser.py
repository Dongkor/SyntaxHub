from ast_nodes import *
from lexer import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0  # Tracks the current position in the token list
        self.current_token = self.tokens[self.idx]
        self.symbol_table = {}  # Tracks declared variables and their types
        self.conditional = False

    def parse(self):
        nodes = []  # Store all parsed statements
        while self.current_token.type != "EOF":  # Continue until the end of file token
            nodes.append(self.statement())  # Parse a statement
        return nodes  # Return a list of AST nodes
    
    def match(self, *token_types):
        # If the current token matches one of the specified token types, consume it
        for token_type in token_types:
            if self.current_token.type == token_type:
                # self.advance()
                return True
        return False

    def consume(self, token_type, error_message):
        # Consume a token of the specified type, or raise an error if it's not found
        if self.current_token.type == token_type:
            # print(self.current_token.type + ": " + self.current_token.value)
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(f"{error_message}, but got '{self.current_token.value}'")

    def advance(self):
        # Move to the next token
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_token = self.tokens[self.idx]

    def statement(self):
        if self.current_token.type == "INT" or self.current_token.type == "STR":
            node =  self.variable_declaration()
        elif self.current_token.type == "PRINT":
            node = self.printing_statement()
        elif self.current_token.type == "INPUT":
            node = self.input_statement()
        elif self.current_token.type == "IF":
            node = self.conditional_statement()
            self.conditional = True
        elif self.current_token.type == "IDENTIFIER" and self.current_token.value in self.symbol_table:
            # print(self.symbol_table, self.current_token.value)
            node = self.assignment_statement()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.value}")
        

        if self.current_token.type == "SEMICOLON" or self.conditional:
            if self.current_token.type == "SEMICOLON":
                self.advance()  # Consume the semicolon
        else:
            raise SyntaxError(f"Missing semicolon at the end of the statement at line {self.current_token.line} index {self.current_token.index}")

        return node
        
    def variable_declaration(self):
        reserved_words = {"INT", "STR", "FLEX", "SPILL", "BET", "THEN", "OTHER_BET", "OTHER"}
        # Handle type (INT or STR)
        if self.current_token.type == "INT":
            var_type = "INT"
        elif self.current_token.type == "STR":
            var_type = "STR"
        else:
            raise SyntaxError("Expected type keyword (INT or STR)")

        self.advance()  # Consume type token

        # Handle variable name
        identifier = self.consume("IDENTIFIER", "Expected variable name").value

        if identifier in reserved_words:
            raise SyntaxError(f"'{identifier}' is a reserved word and cannot be used as a variable name.")

        # Check for initialization
        if self.current_token.type == "EQUAL":
            self.advance()  # Consume '='
            if var_type == "INT":
                # Parse an expression
                expr_node = self.expression()
                self.symbol_table[identifier] = {"type": var_type, "value": None}  # Set to None initially
                # print("sexpr_node:", expr_node)
                return AssignmentNode(identifier, expr_node)
            elif var_type == "STR":
                value = self.consume("STRING", "Expected a string value").value
                self.symbol_table[identifier] = {"type": var_type, "value": value}
                return AssignmentNode(identifier, StringNode(value))
        else:
            # Uninitialized variable
            self.symbol_table[identifier] = {"type": var_type, "value": None}
            return VariableNode(identifier, var_type)

    
    def printing_statement(self):
        self.consume("PRINT", "Expected 'PRINT' keyword.")

        if self.current_token.type == "STRING":
            value = StringNode(self.current_token.value)
            self.advance()
        elif self.current_token.type == "IDENTIFIER":
            variable_name = self.current_token.value
            # print(self.symbol_table)
            if variable_name not in self.symbol_table:
                raise ValueError(f"Variable '{variable_name}' is not declared.")
            
            variable = self.symbol_table[variable_name]

            value = VariableNode(variable_name,variable['type'])
            self.advance()
        elif self.current_token.type == "NUMBER":
            value = NumberNode(self.current_token.value)
            self.advance()
        else:
            raise SyntaxError("Expected a string, variable, or number to print.")

        return PrintNode(value)
    
    def input_statement(self):
        self.consume("INPUT", "Expected 'INPUT' keyword.")

        # Handle variable input
        variable_name = self.consume("IDENTIFIER", "Expected a variable name").value

        if variable_name not in self.symbol_table:
            raise ValueError(f"Variable '{variable_name}' is not declared before input.")
        
        variable = self.symbol_table[variable_name]
        
        # print(variable['type'], variable_name)
        # Return InputNode, linking to the variable
        return InputNode(variable_name, variable['type'])
    def assignment_statement(self):
        identifier = self.consume("IDENTIFIER", "Expected variable name").value
        if self.current_token.type == "EQUAL":
            self.advance()  # Consume '='

        if self.current_token.type == "STRING":
            expr_node = StringNode(self.current_token.value)
            self.advance()
        else:
            expr_node = self.expression()
        
        return AssignmentNode(identifier, expr_node)
    def conditional_statement(self):
        self.consume("IF", "Expected 'BET' keyword.")

        left = self.expression()

        if self.current_token.type not in ("IS_EQUAL", "NOT_EQUAL", "LESS_THAN", "GREATER_THAN", "LESS_EQUAL", "GREATER_EQUAL"):
            raise SyntaxError("Expected a comparison operator (==, !=, <, >, <=, >=)")

        # Parse the comparison operator
        op = self.current_token
        self.advance()  # Consume the operator
        right = self.expression()

        # Create the condition node
        condition = ConditionNode(op.value, left, right)

        # Ensure 'THEN' keyword follows
        self.consume("THEN", "Expected 'THEN' keyword after condition")
        
        # Parse the statement for the true branch (code to execute if condition is true)
        true_branch = self.statement()

         # Parse optional 'OTHER_BET' (elif) branches
        elif_branches = []
        while self.current_token.type == "ELIF":
            self.consume("ELIF", "Expected 'OTHER_BET' keyword.")
            
            # Parse left operand for elif condition
            elif_left = self.expression()
            
            # Ensure there is a valid comparison operator for elif
            if self.current_token.type not in ("IS_EQUAL", "NOT_EQUAL", "LESS_THAN", "GREATER_THAN", "LESS_EQUAL", "GREATER_EQUAL"):
                raise SyntaxError("Expected a comparison operator in 'OTHER_BET' (elif)")
            
            # Parse operator for elif condition
            elif_op = self.current_token
            self.advance()  # Consume the operator
            
            # Parse right operand for elif condition
            elif_right = self.expression()
            
            # Create elif condition node
            elif_condition = ConditionNode(elif_op.value, elif_left, elif_right)
            
            # Ensure 'THEN' follows for elif
            self.consume("THEN", "Expected 'THEN' keyword after 'OTHER_BET' condition")
            
            # Parse the statement for the elif branch
            elif_branch = self.statement()
            
            # Append the elif condition and branch
            elif_branches.append((elif_condition, elif_branch))
        
        # Parse optional 'OTHER' (else) block
        else_branch = None
        if self.current_token.type == "ELSE":
            self.consume("ELSE", "Expected 'OTHER' keyword.")
            # print("else before", self.current_token)
            else_branch = self.statement()
            # print("else", else_branch, self.current_token)

        return ConditionalNode(condition, true_branch, elif_branches, else_branch)

    def expression(self):
        # Parse lower precedence operators first (e.g., +, -)
        node = self.term()
        while self.current_token.type in ("PLUS", "MINUS"):
            op = self.current_token
            self.advance()  # consume operator
            right = self.term()
            node = BinaryOpNode(op.value, node, right)
        return node

    def term(self):
        # Parse higher precedence operators (e.g., *, /)
        node = self.factor()
        while self.current_token.type in ("MULTIPLY", "DIVIDE"):
            op = self.current_token
            self.advance()  # consume operator
            right = self.factor()
            node = BinaryOpNode(op.value, node, right)
        return node

    def factor(self):
        # Parse numbers or parentheses (to handle parentheses for precedence)
        if self.current_token.type == "NUMBER":
            value = self.current_token
            self.advance()
            return NumberNode(value.value)
        elif self.current_token.type == "LPAREN":
            self.advance()  # consume '('
            node = self.expression()  # recurse into expression
            if self.current_token.type != "RPAREN":
                raise SyntaxError("Expected ')'")
            self.advance()  # consume ')'
            return node
        if self.current_token.type == "IDENTIFIER":
            # print(self.symbol_table)
            variable_name = self.current_token.value
            if variable_name not in self.symbol_table:
                raise ValueError(f"Variable '{variable_name}' is not declared.")
            
            variable = self.symbol_table[variable_name]
            # print(variable['type'])
            node = VariableNode(variable_name, variable['type'])
            # print("node", node)
            self.advance()

            return node
        else:
            raise SyntaxError("Unexpected token: " + self.current_token.type + " in line " + str(self.current_token.line))
        
        # return left

        # E -> S
        # S -> expr | print | input | output