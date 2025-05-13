from collections import namedtuple

# AST Nodes
Number = namedtuple("Number", ["value"])
String = namedtuple("String", ["value"])
Var = namedtuple("Var", ["name"])
BinOp = namedtuple("BinOp", ["left", "op", "right"])
Print = namedtuple("Print", ["value"])
Assign = namedtuple("Assign", ["name", "value"])
IfElse = namedtuple("IfElse", ["condition", "true_block", "false_block"])
Block = namedtuple("Block", ["statements"])
FuncDef = namedtuple("FuncDef", ["name", "params", "body"])
FuncCall = namedtuple("FuncCall", ["name", "args"])

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else (None, None)

    def advance(self):
        tok = self.peek()
        self.i += 1
        return tok

    def expect(self, expected_type, expected_value=None):
        tok_type, value = self.advance()
        if tok_type != expected_type or (expected_value and value != expected_value):
            raise SyntaxError(f"Expected {expected_type} {expected_value}, got {value}")
        return value

    def parse(self):
        stmts = []
        while self.peek()[0]:
            stmts.append(self.parse_statement())
        return Block(stmts)

    def parse_statement(self):
        tok_type, tok_val = self.peek()
        if tok_val == "vibe":
            return self.parse_declaration()
        elif tok_val == "spill":
            return self.parse_print()
        elif tok_val == "delulu":
            return self.parse_ifelse()
        elif tok_val == "funk":
            return self.parse_function()
        elif tok_type == "ID":
            # could be assignment or function call
            next_tok = self.tokens[self.i + 1]
            if next_tok[1] == "=":
                return self.parse_assignment()
            else:
                return self.parse_func_call()
        else:
            raise SyntaxError(f"Unexpected token {tok_val}")

    def parse_declaration(self):
        self.expect("KEYWORD", "vibe")
        name = self.expect("ID")
        self.expect("SYMBOL", "=")
        expr = self.parse_expression()
        self.expect("SYMBOL", ";")
        return Assign(name, expr)

    def parse_assignment(self):
        name = self.expect("ID")
        self.expect("SYMBOL", "=")
        expr = self.parse_expression()
        self.expect("SYMBOL", ";")
        return Assign(name, expr)

    def parse_print(self):
        self.expect("KEYWORD", "spill")
        expr = self.parse_expression()
        self.expect("SYMBOL", ";")
        return Print(expr)

    def parse_ifelse(self):
        self.expect("KEYWORD", "delulu")
        cond = self.parse_expression()
        true_block = self.parse_block()
        self.expect("KEYWORD", "nah")
        false_block = self.parse_block()
        return IfElse(cond, true_block, false_block)

    def parse_function(self):
        self.expect("KEYWORD", "funk")
        name = self.expect("ID")
        self.expect("SYMBOL", "(")
        params = []
        while self.peek()[1] != ")":
            params.append(self.expect("ID"))
            if self.peek()[1] == ",":
                self.advance()
        self.expect("SYMBOL", ")")
        body = self.parse_block()
        return FuncDef(name, params, body)

    def parse_func_call(self):
        name = self.expect("ID")
        self.expect("SYMBOL", "(")
        args = []
        while self.peek()[1] != ")":
            args.append(self.parse_expression())
            if self.peek()[1] == ",":
                self.advance()
        self.expect("SYMBOL", ")")
        self.expect("SYMBOL", ";")
        return FuncCall(name, args)

    def parse_block(self):
        self.expect("SYMBOL", "{")
        stmts = []
        while self.peek()[1] != "}":
            stmts.append(self.parse_statement())
        self.expect("SYMBOL", "}")
        return Block(stmts)

    def parse_expression(self):
        left = self.parse_primary()
        while self.peek()[1] in (">=", ">", "<=", "<", "==", "+", "-", "*", "/"):
            op = self.advance()[1]
            right = self.parse_primary()
            left = BinOp(left, op, right)
        return left

    def parse_primary(self):
        tok_type, val = self.advance()
        if tok_type == "NUMBER":
            return Number(int(val))
        elif tok_type == "STRING":
            return String(val.strip('"'))
        elif tok_type == "ID":
            return Var(val)
        else:
            raise SyntaxError(f"Unexpected primary token: {val}")
