#!/usr/bin/env python

import abc
from typing import Iterable, Collection

__all__ = (
    "Literal",
    "SExpr",
    "Sexpressable",
    "BracketExpression",
    "CurlyExpression",
    "LiteralExpression",
    "TriangleExpression",
)


class Literal:
    def __init__(self, data: str):
        self.data = data

    def __str__(self) -> str:
        return self.data


class Sexpressable:
    pass


class SExpr(abc.ABC):
    content: Collection["SExpr"] | Literal
    level: int = 0
    indent_char: str = " "
    line_sep: str = "\n"
    sopen: str
    sclose: str

    def __str__(self):
        return self.__format__("0")

    def __format__(self, fmt):
        level = int(fmt)

        if isinstance(self.content, Literal):
            return self.indent(level, self.sopen + str(self.content) + self.sclose)

        if not isinstance(self.content, Iterable):
            return self.indent(level, self.sopen + str(self.content) + self.sclose)

        if len(self.content) == 1:
            sopen = self.sopen
            sclose = self.sclose
            for only_child in self.content:
                if isinstance(only_child, Literal):
                    return self.indent(
                        level, self.sopen + str(only_child) + self.sclose
                    )

        sopen = self.indent(level, self.sopen)
        lines = self.indent_all(level + 1, self.content)
        sclose = self.sclose

        return self.line_sep.join([sopen, lines + sclose])

    def indent(self, amount: int, item: str):
        return self.indent_char * amount + item

    def indent_all(self, amount: int, children: Collection["SExpr"]):
        if not isinstance(children, Iterable):
            return self.indent(amount, children)

        lines = []
        for child in children:
            lines.append(f"{child:{amount+1}}")

        return self.line_sep.join(lines)

    def express(self, level: int, objects: Collection | Literal) -> str:
        self.content = objects
        return f"{self:{level}}"


class JsonExpression(SExpr):
    sopen = "("
    sclose = ")"

    def __init__(self, stupid_mode=False):
        self.stupid_mode = stupid_mode

    def format_sexpr(self, obj, indent_len=0, use_indent=True):
        sopen = (
            obj["sopen"]
            if "sopen" in obj and not self.stupid_mode
            else (
                f"'{JsonExpression.sopen}"
                if "denotation" in obj
                else JsonExpression.sopen
            )
        )
        sclose = (
            obj["sclose"]
            if "sclose" in obj and not self.stupid_mode
            else JsonExpression.sclose
        )
        prefix = indent_len * " " if use_indent else ""
        label = obj["label"]

        if "denotation" in obj:
            return prefix + sopen + obj["denotation"] + sclose

        if "children" not in obj:
            return prefix + obj

        car, cdr = obj["children"][0], obj["children"][1:]
        next_indent = indent_len + len(sopen) + len(label) + 1
        car_str = self.format_sexpr(car, next_indent, False)

        if cdr:
            first_line = f"{prefix}{sopen}{label} {car_str}\n"

            cdr_str = "\n".join(
                [self.format_sexpr(child, next_indent, True) for child in cdr]
            )

            return f"{first_line}{cdr_str}{sclose}"

        else:
            return f"{prefix}{sopen}{label} {car_str}{sclose}"


class QuoteExpression(SExpr):
    sopen: str = "(quote"
    sclose: str = ")"
    multiline = False

    def __format__(self, fmt):
        level = int(fmt)
        return self.indent(level, self.sopen + f"{self.content}" + self.sclose)


class TriangleExpression(SExpr):
    sopen: str = "(proposition"
    sclose: str = ")"


class BracketExpression(SExpr):
    sopen: str = "("
    sclose: str = ")"


class CurlyExpression(SExpr):
    sopen: str = "(concept"
    sclose: str = ")"


class LiteralExpression(SExpr):
    sopen: str = '(literal "'
    sclose: str = '")'


#  vim: set sw=4 ts=4 expandtab
