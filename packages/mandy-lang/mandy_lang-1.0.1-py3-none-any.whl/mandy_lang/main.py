import re
import sys

# Token definitions
TOKEN_TYPES = {
    "WRITE": r"(?i)write",
    "TAKE": r"(?i)take",
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "NUMBER": r"\d+(\.\d+)?",
    "STRING": r'"[^"]*"',
    "OPERATOR": r"[+\-*/%^]",
    "EQUALS": r"=",
    "COMMENT": r"!!.*",
    "WHITESPACE": r"\s+"
}

# Lexer class
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        code = self.source_code.strip()
        while code:
            match = None
            for token_type, pattern in TOKEN_TYPES.items():
                regex = re.match(pattern, code, re.IGNORECASE)
                if regex:
                    match = regex.group(0)
                    if token_type == "COMMENT":
                        code = code[len(match):].strip()
                        break
                    if token_type != "WHITESPACE":
                        if token_type in ["WRITE", "TAKE"]:
                            match = match.lower()
                        self.tokens.append({"type": token_type, "value": match})
                    code = code[len(match):].strip()
                    break
            if not match:
                raise ValueError(f"Unexpected token: {code[0]}")
        return self.tokens

# AST Nodes
class ASTNode:
    pass

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class VariableNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

# Mandy Virtual Machine
class MandyVM:
    def __init__(self):
        self.variables = {}

    def execute(self, ast):
        for node in ast:
            if isinstance(node, PrintNode):
                self.handle_print(node.expression)
            elif isinstance(node, VariableNode):
                self.handle_variable(node)

    def handle_print(self, expression):
        result = self.evaluate_expression(expression)
        print(result)

    def handle_variable(self, node):
        value = self.evaluate_expression(node.value)
        self.variables[node.name] = value

    def evaluate_expression(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            return self.variables.get(node.name, f"Error: Undefined variable '{node.name}'")
        elif isinstance(node, BinaryOpNode):
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)
            if node.operator == "+":
                return left + right
            elif node.operator == "-":
                return left - right
            elif node.operator == "*":
                return left * right
            elif node.operator == "/":
                return left / right if right != 0 else "Error: Division by zero"
            elif node.operator == "%":
                return left % right
            elif node.operator == "**":
                return left ** right
        return node

# Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self):
        if self.pos >= len(self.tokens):
            return None
        token = self.tokens[self.pos]

        if token["type"] == "WRITE":
            return self.parse_print_statement()
        elif token["type"] == "TAKE":
            return self.parse_variable_assignment()
        else:
            raise ValueError(f"Unexpected token: {token}")

    def parse_print_statement(self):
        self.pos += 1  
        expression = self.parse_expression()
        return PrintNode(expression)

    def parse_variable_assignment(self):
        self.pos += 1  
        var_name = self.tokens[self.pos]
        if var_name["type"] != "IDENTIFIER":
            raise ValueError("Expected variable name after 'Take'")
        
        self.pos += 1  
        if self.tokens[self.pos]["type"] != "EQUALS":
            raise ValueError("Expected '=' after variable name")
        
        self.pos += 1  
        value = self.parse_expression()
        return VariableNode(var_name["value"], value)

    def parse_expression(self):
        return self.parse_term()

    def parse_term(self):
        left = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos]["type"] == "OPERATOR" and self.tokens[self.pos]["value"] in ("+", "-"):
            operator = self.tokens[self.pos]["value"]
            self.pos += 1  
            right = self.parse_factor()
            left = BinaryOpNode(left, operator, right)
        return left

    def parse_factor(self):
        left = self.parse_exponent()
        while self.pos < len(self.tokens) and self.tokens[self.pos]["type"] == "OPERATOR" and self.tokens[self.pos]["value"] in ("*", "/", "%"):
            operator = self.tokens[self.pos]["value"]
            self.pos += 1  
            right = self.parse_exponent()
            left = BinaryOpNode(left, operator, right)
        return left

    def parse_exponent(self):
        left = self.parse_primary()
        while self.pos < len(self.tokens) and self.tokens[self.pos]["type"] == "OPERATOR" and self.tokens[self.pos]["value"] == "^":
            operator = "**"
            self.pos += 1  
            right = self.parse_primary()
            left = BinaryOpNode(left, operator, right)
        return left

    def parse_primary(self):
        token = self.tokens[self.pos]
        self.pos += 1  

        if token["type"] == "NUMBER":
            return NumberNode(float(token["value"]))
        elif token["type"] == "IDENTIFIER":
            return IdentifierNode(token["value"])
        elif token["type"] == "STRING":
            return token["value"]  
        else:
            raise ValueError(f"Unexpected token in expression: {token}")

def main():
    if len(sys.argv) < 2:
        print("Usage: mandyc <filename>.mnd")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            source_code = file.read()
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        vm = MandyVM()
        vm.execute(ast)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
