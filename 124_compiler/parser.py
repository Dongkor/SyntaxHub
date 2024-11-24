from ast_1 import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0  # Tracks the current position in the token list
        self.current_token = self.tokens[self.idx]

    def parse(self):
        return self.statement()
    
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
            print(self.current_token.type + ": " + self.current_token.value)
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
        if self.current_token.type == "LET":
            return self.variable_declaration()
        elif self.current_token.type == "FLEX":
            print("printing")
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.value}")
        
    def variable_declaration(self):
        # Handle a 'LET' statement: 'LET x = 5 + 5'
        self.consume("LET", "Expected 'LET' keyword.")
        
        # The next token should be an identifier (the variable name) - x
        identifier = self.consume("IDENTIFIER", "Expected a variable name.").value
        
        # Next, consume the equal sign '='
        self.consume("EQUAL", "Expected '=' after variable name.") 
        
        # Now we parse the expression on the right-hand side of the '='
        value = self.expression()

        # Create an AST node for the assignment and return it
        return AssignmentNode(identifier, value)

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
        else:
            raise SyntaxError("Unexpected token: " + self.current_token.type)
        
        # return left