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
    
class ConditionalNode(ASTNode):
    def __init__(self, condition, true_branch=None, elif_branches=None, else_branch=None):
        super().__init__("Conditional")
        self.condition = condition  # Main condition (ConditionNode)
        self.true_branch = true_branch  # Code to execute if the condition is true
        self.elif_branches = elif_branches if elif_branches is not None else []   # List of (ConditionNode, statement) for 'OTHER_BET'
        self.else_branch = else_branch  # Code to execute if no condition is matched

    def to_dict(self):
        # Build the dictionary for the ConditionalNode
        return {
            "type": "Conditional",
            "condition": self.condition.to_dict(),  # Fix typo here, should be "condition"
            "true_branch": self.true_branch.to_dict() if self.true_branch else None,  # Ensure we call to_dict on nodes
            "elif_branches": [
                (elif_cond.to_dict(), elif_stmt.to_dict()) for elif_cond, elif_stmt in self.elif_branches
            ] if self.elif_branches else [],  # If there are elif branches, convert them, else an empty list
            "else_branch": self.else_branch.to_dict() if self.else_branch else None  # Convert else branch if it exists
        }
    

class ConditionNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("Condition")
        self.operator = operator
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": "Condition",
            "operator": self.operator,
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }