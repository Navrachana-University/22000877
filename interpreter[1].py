class Environment:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def eval(self, node):
        match node:
            case Number(value):
                return value
            case String(value):
                return value
            case Var(name):
                return self.vars[name]
            case BinOp(left, op, right):
                l = self.eval(left)
                r = self.eval(right)
                return eval(f"{l} {op} {r}")
            case Assign(name, value):
                self.vars[name] = self.eval(value)
            case Print(value):
                print(self.eval(value))
            case IfElse(condition, true_block, false_block):
                if self.eval(condition):
                    self.eval(true_block)
                else:
                    self.eval(false_block)
            case Block(statements):
                for stmt in statements:
                    self.eval(stmt)
            case FuncDef(name, params, body):
                self.funcs[name] = (params, body)
            case FuncCall(name, args):
                params, body = self.funcs[name]
                local_env = Environment()
                for p, a in zip(params, args):
                    local_env.vars[p] = self.eval(a)
                local_env.funcs = self.funcs  # Share functions
                return local_env.eval(body)
