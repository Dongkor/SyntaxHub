import re

TokenType = {
    "LET": re.compile(r"\bLET\b"),
    # "COOK": re.compile(r"\bCOOK\b"),
    "FLEX": re.compile(r"\bFLEX\b"),
    # "SPILL": re.compile(r"\bSPILL\b"),
    # "SAYING": re.compile(r"\bSAYING\b"),
    # "BET": re.compile(r"\bBET\b"),
    # "THEN": re.compile(r"\bTHEN\b"),
    # "OTHER": re.compile(r"\bOTHER\b"),
    # "KEEP_IT": re.compile(r"\bKEEP IT\b"),
    # "TIL": re.compile(r"\bTIL\b"),
    "EQUAL": re.compile(r"="),
    # "BINARY_OP": re.compile(r"[+\-*/]"),
    "PLUS": re.compile(r"\+"),
    "MINUS": re.compile(r"-"),
    "MULTIPLY": re.compile(r"\*"),
    "DIVIDE": re.compile(r"/"),
    # "IS_EQUAL": re.compile(r"=="),
    # "NOT_EQUAL": re.compile(r"!="),
    # "LESS_THAN": re.compile(r"<"),
    # "GREATER_THAN": re.compile(r">"),
    # "LESS_EQUAL": re.compile(r"<="),
    # "GREATER_EQUAL": re.compile(r">="),
    # "AND": re.compile(r"\bN\b"),
    # "OR": re.compile(r"\b’R\b"),
    "NUMBER": re.compile(r"\b\d+(\.\d+)?\b"),
    "STRING": re.compile(r"\"(.*?)\""),
    "IDENTIFIER": re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    "LPAREN": re.compile(r"\("),
    "RPAREN": re.compile(r"\)"),
    "COMMA": re.compile(r","),
    "SEMICOLON": re.compile(r";"),
}

class Token:
    def __init__(self, type, value, line, index):
        self.type = type
        self.value = value
        self.line = line
        self.index = index

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, index={self.index})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line = 1
        self.idx = 0

    def tokenize(self):
        index = 0
        while index < len(self.code):
            match = None

            # Skip whitespace and update line/index numbers
            if self.code[index].isspace():
                if self.code[index] == "\n":
                    self.line += 1
                    self.idx = 0
                else:
                    self.idx += 1
                index += 1
                continue

            # Try matching each token type
            for token_type, regex in TokenType.items():
                match = regex.match(self.code, index)
                if match:
                    # print(match)
                    value = match.group(0)
                    self.tokens.append(Token(token_type, value, self.line, self.idx))
                    index += len(value)
                    self.idx += len(value)
                    break

            if not match:
                raise SyntaxError(
                    f"Unknown character at line {self.line}, index {self.idx}: '{self.code[index]}'"
                )

        # Append EOF token
        self.tokens.append(Token("EOF", "", self.line, self.idx))
        return self.tokens
