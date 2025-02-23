from typing import List, Optional, Union, Set


class AST:
    """Base class for all AST nodes."""

    def pretty(self, indent_str: str = "  ", level: int = 0) -> str:
        """Returns a nicely formatted string representation of this AST node."""
        lines = []
        prefix = indent_str * level
        node_name = self.__class__.__name__
        lines.append(f"{prefix}{node_name}")

        for attr, value in vars(self).items():
            lines.append(self._pretty_attr(attr, value, indent_str, level + 1))

        return "\n".join(line for line in lines if line)

    def _pretty_attr(self, name, value, indent_str, level):
        prefix = indent_str * level
        if isinstance(value, AST):
            return f"{prefix}{name}:\n{value.pretty(indent_str, level + 1)}"

        elif isinstance(value, list):
            lines = [f"{prefix}{name}:"]
            for item in value:
                if isinstance(item, AST):
                    lines.append(item.pretty(indent_str, level + 1))
                else:
                    lines.append(f"{indent_str * (level + 1)}{repr(item)}")
            return "\n".join(lines)

        else:
            return f"{prefix}{name}: {repr(value)}"


class L_cfi(AST):
    __match_args__ = ("declar", "stmt")

    def __init__(self, declar: List["Declar"], stmt: List["Stmt"]) -> None:
        self.declar = declar
        self.stmt = stmt

    def __str__(self):
        return ('\n'.join([str(decl) for decl in self.declar])
                + '\n'
                + '\n'.join([str(stmt) for stmt in self.stmt]))

class Var(AST):
    __match_args__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name


class Type(AST):
    pass


class Bool(Type):
    def __str__(self):
        return "bool"


class Int(Type):
    def __str__(self):
        return "int"


class Float(Type):
    def __str__(self):
        return "float"



class Exp(AST):
    pass

class Var(Exp):
    __match_args__ = ("name",)
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name

class Declar(AST):
    __match_args__ = ("lcfi_type", "var")

    def __init__(self, lcfi_type: Type, var: Union[Var, Set[Var]]) -> None:
        self.lcfi_type = lcfi_type
        self.var = var

    def __str__(self):
        if isinstance(self.var, Var):
            return f"{self.lcfi_type} {self.var}"
        else:
            return f"{self.lcfi_type} {', '.join(str(var) for var in self.var)}"

class Constant(Exp):
    __match_args__ = ("value",)

    def __init__(self, value: int | float) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)


class Bools(Exp):
    __match_args__ = ("value",)

    def __init__(self, value: bool) -> None:
        self.value = value

    def __str__(self):
        return "true" if self.value else "false"


class Pred(AST):
    __match_args__ = ("value",)

    def __init__(self, value: Union[Bools, Var]) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)


class Inst(AST):
    pass


class Stmt(AST):
    __match_args__ = ("label", "pred", "inst")

    def __init__(self, label: Optional[str], pred: Pred, inst: Inst) -> None:
        self.label = label
        self.pred = pred
        self.inst = inst

    def __str__(self):
        return f"{self.pred}: {self.inst}"


class PrintInst(Inst):
    __match_args__ = ("string", "exp")

    def __init__(self, string: str, exp: Optional[Exp]) -> None:
        self.string = string
        self.exp = exp

    def __str__(self):
        if self.exp:
            return f"print(\"{self.string}\", {self.exp})"
        else:
            return f"print(\"{self.string}\")"


class ExpInst(Inst):
    __match_args__ = ("exp",)

    def __init__(self, exp: Exp) -> None:
        self.exp = exp

    def __str__(self):
        return str(self.exp)


class Assign(AST):
    __match_args__ = ("var", "exp")

    def __init__(self, var: Var, exp: Exp) -> None:
        self.var = var
        self.exp = exp

    def __str__(self):
        return f"{self.var} = {self.exp}"


class AssignInst(Inst):
    __match_args__ = ("assign",)

    def __init__(self, assign: Assign) -> None:
        self.assign = assign

    def __str__(self):
        return str(self.assign)


class Operator(AST):
    pass


class BoolOperator(Operator):
    pass


class BinaryBoolOperator(BoolOperator):
    pass


class And(BinaryBoolOperator):
    def __str__(self):
        return "&&"


class Or(BinaryBoolOperator):
    def __str__(self):
        return "||"


class UnaryBoolOperator(BoolOperator):
    pass


class Not(UnaryBoolOperator):
    def __str__(self):
        return "!"


class NumOperator(Operator):
    pass


class BinaryNumOperator(NumOperator):
    pass


class Add(BinaryNumOperator):
    def __str__(self):
        return "+"


class Sub(BinaryNumOperator):
    def __str__(self):
        return "-"


class Mult(BinaryNumOperator):
    def __str__(self):
        return "*"


class Div(BinaryNumOperator):
    def __str__(self):
        return "/"


class Mod(BinaryNumOperator):
    def __str__(self):
        return "%"


class UnaryNumOperator(NumOperator):
    pass


class UAdd(UnaryNumOperator):
    def __str__(self):
        return ""


class USub(UnaryNumOperator):
    def __str__(self):
        return "-"


class Comparator(AST):
    pass


class Eq(Comparator):
    def __str__(self):
        return "=="


class Neq(Comparator):
    def __str__(self):
        return "!="


class Gt(Comparator):
    def __str__(self):
        return ">"


class Ge(Comparator):
    def __str__(self):
        return ">="


class Lt(Comparator):
    def __str__(self):
        return "<"


class Le(Comparator):
    def __str__(self):
        return "<="


class UnaryOp(Exp):
    __match_args__ = ("op", "operand")

    def __init__(self, op: Union[str, Operator], operand: Exp) -> None:
        self.op = op
        self.operand = operand

    def __str__(self):
        match self.operand:
            case Constant() | Bools() | Var():
                return f"{self.op}{self.operand}"
            case _:
                return f"{self.op}({self.operand})"


class BinOp(Exp):
    __match_args__ = ("left", "op", "right")

    def __init__(
        self, left: Exp, op: Union[str, Operator, Comparator], right: Exp
    ) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        match self.right:
            case Constant() | Bools() | Var():
                return f"{self.left} {self.op} {self.right}"
            case _:
                return f"{self.left} {self.op} ({self.right})"

