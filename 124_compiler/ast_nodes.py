import json

class ASTNode:
    def __init__(self, type):
        self.type = type

    def to_dict(self):
        return {"type": self.type}

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)

class AssignmentNode(ASTNode):
    def __init__(self, identifier, value):
        super().__init__("Assignment")
        self.identifier = identifier
        self.value = value

    def to_dict(self):
        return {
            "type": "Assignment",
            "identifier": self.identifier,
            "value": self.value.to_dict()
        }

class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("BinaryOp")
        self.operator = operator
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": "BinaryOp",
            "operator": self.operator,
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }

class VariableNode(ASTNode):
    def __init__(self, identifier, datatype):
        super().__init__("Variable")
        self.identifier = identifier
        self.datatype = datatype

    def to_dict(self):
        return {
            "type": "Variable",
            "name": self.identifier,
            "var_type": self.datatype
        }

class NumberNode(ASTNode):
    def __init__(self, value):
        super().__init__("Number")
        self.value = value

    def to_dict(self):
        return {
            "type": "Number",
            "value": self.value
        }
    
class StringNode(ASTNode):
    def __init__(self, value):
        super().__init__("String")
        self.value = value

    def to_dict(self):
        return {
            "type": "String",
            "value": self.value
        }
    
class InputNode(ASTNode):
    def __init__(self, name, datatype):
        super().__init__("Input")
        self.name = name
        self.datatype = datatype 
    
    def to_dict(self):
        return {
            "type": "Input",
            "name" : self.name,
            "datatype" : self.datatype
        }

class PrintNode(ASTNode):
    def __init__(self, value):
        super().__init__("Print")
        self.value = value

    def to_dict(self):
        return {
            "type": "Print",
            "value": self.value.to_dict()
        }
