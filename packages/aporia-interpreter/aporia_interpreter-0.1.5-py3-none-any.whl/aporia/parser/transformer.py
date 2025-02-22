from typing import Any
from lark import Transformer, v_args
from aporia.aporia_ast import (
    Add,
    And,
    Assign,
    AssignInst,
    BinOp,
    Bool,
    Bools,
    Declar,
    Div,
    Eq,
    ExpInst,
    Float,
    Ge,
    Gt,
    Int,
    L_cfi,
    Constant,
    Le,
    Lt,
    Mod,
    Mult,
    Neq,
    Not,
    Or,
    Pred,
    PrintInst,
    Stmt,
    Sub,
    UAdd,
    USub,
    UnaryOp,
    Var,
)


class LcfiTransformer(Transformer[Any, L_cfi]):
    def start(self, children):
        return children[0]

    def l_cfi(self, children):
        declar_list = []
        stmt_list = []
        for c in children:
            if isinstance(c, Declar):
                declar_list.append(c)
            else:
                stmt_list.append(c)
        return L_cfi(declar_list, stmt_list)

    def declar(self, children):
        t = children[0]
        v = children[1].children
        return Declar(t, v)

    def type(self, children):
        match children[0]:
            case "bool":
                return Bool()
            case "int":
                return Int()
            case "float":
                return Float()

    def stmt(self, children):
        pred = children[0]
        inst = children[1]
        return Stmt(None, pred, inst)

    def LABEL(self, token):
        return str(token)

    def pred(self, children):
        return Pred(children[0])

    def inst(self, children):
        if len(children) == 1:
            if isinstance(children[0], Assign):
                return AssignInst(children[0])
            elif isinstance(children[0], PrintInst):
                return children[0]
            else:
                return ExpInst(children[0])
        else:
            raise ValueError("Unknown inst form: children = {}".format(children))

    def print_inst(self, children):
        string_value = None
        exp_node = None
        if len(children) == 1:
            if isinstance(children[0], str):
                string_value = children[0]
            else:
                exp_node = children[0]
        elif len(children) == 2:
            string_value = children[0]
            exp_node = children[1]
        return PrintInst(string_value, exp_node)

    @v_args(inline=True)
    def STRING(self, s):
        return s[1:-1]

    def assign(self, children):
        v = children[0]
        e = children[1]
        return Assign(v, e)

    def bools(self, children):
        val = children[0]
        return Bools(val == "true")

    @v_args(inline=True)
    def NUMBER(self, token):
        return Constant(int(token))

    @v_args(inline=True)
    def FLOATINGNUMBER(self, token):
        return Constant(float(token))

    def var(self, children):
        return Var(children[0])

    @v_args(inline=True)
    def VAR(self, token):
        return str(token)

    def binop(self, children):
        left, token_op, right = children
        op = self.convert_op(token_op)
        return BinOp(left, op, right)

    def unaryop(self, children):
        (token_op, expr) = children
        op = self.convert_unaryop(token_op)
        return UnaryOp(op, expr)

    def cmpop(self, children):
        left, token_op, right = children
        return BinOp(left, token_op, right)

    @v_args(inline=True)
    def cmp(self, token):
        match token:
            case "<":
                return Lt()
            case "<=":
                return Le()
            case ">":
                return Gt()
            case ">=":
                return Ge()
            case "==":
                return Eq()
            case "!=":
                return Neq()
        return str(token)

    def convert_op(self, token):
        match token:
            case "+":
                return Add()
            case "-":
                return Sub()
            case "*":
                return Mult()
            case "/":
                return Div()
            case "%":
                return Mod()
            case "||":
                return Or()
            case "&&":
                return And()
            case _:
                raise ValueError(f"Unknown operator: {token}")

    def convert_unaryop(self, token):
        match token:
            case "!":
                return Not()
            case "+":
                return UAdd()
            case "-":
                return USub()
            case _:
                raise ValueError(f"Unknown unary operator: {token}")

    def atom(self, children):
        return children[0]
