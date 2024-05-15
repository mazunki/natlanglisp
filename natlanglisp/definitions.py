#!/usr/bin/env python

from typing import Union, Collection
from .sexpressions import *
import abc

__all__ = ("Sense", "Concept", "Proposition")

FregeUnits = Union["Sense", "Concept", "Proposition"]
Propositionable = Union["Concept", "Proposition"]
Conceptualizable = Union["Sense", "Concept"]


class Fregian(abc.ABC):
    children: Collection[FregeUnits]
    denotation: Literal

    def __str__(self) -> str:
        return self.__format__("0")

    def __format__(self, fmt):
        depth = int(fmt)

        return self.express(depth)

    @abc.abstractmethod
    def express(self, depth: int) -> str:
        pass


class Sense(Fregian):
    sexpr = LiteralExpression()

    def __init__(self, literal: str):
        self.denotation = Literal(literal)

    def __str__(self):
        return str(self.denotation)

    def __repr__(self):
        return f"«{self.denotation}»"

    def express(self, depth: int) -> str:
        return self.sexpr.express(depth, self.denotation)


class Concept(Fregian):
    sexpr = CurlyExpression()

    def __init__(self, *elements: Conceptualizable):
        self.children = set(elements)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.children})"

    def __iter__(self):
        return iter(self.children)

    def express(self, depth: int) -> str:
        return self.sexpr.express(depth, self.children)


class Proposition(Concept):
    sexpr = TriangleExpression()

    def __init__(self, lhs: Propositionable, rhs: Propositionable, /):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f"{self.__class__.__name__}<{repr(self.lhs)}, {repr(self.rhs)}>"

    def express(self, depth: int) -> str:
        return self.sexpr.express(depth, [self.lhs, self.rhs])


#  vim: set sw=4 ts=4 expandtab
