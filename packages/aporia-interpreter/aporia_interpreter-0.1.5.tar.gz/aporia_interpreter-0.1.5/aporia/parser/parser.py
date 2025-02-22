from lark import Lark
from aporia.parser.transformer import LcfiTransformer
from aporia.aporia_ast import L_cfi
from pathlib import Path


def parse(lcfi_program: str) -> L_cfi:
    grammar_path = Path(__file__).resolve().parent / "grammar.lark"
    parser = Lark.open(grammar_path, start="start", parser="lalr")
    tree = parser.parse(lcfi_program)
    ast = LcfiTransformer().transform(tree)
    return ast
