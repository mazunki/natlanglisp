#!/usr/bin/env python

from typing import Union, Collection, Self
from .sexpressions import Sexpressable, Literal, JsonExpression
import abc
import json

__all__ = ("Sense", "Concept", "Proposition", "Sentence", "Function")

Fregians = Union["Sense", "Concept", "Proposition", "Sentence", "Function"]
Conceptualizable = Union["Sense", "Concept"]
Propositionable = Union["Concept", "Proposition"]


class Fregian(abc.ABC):
    """an important linguist, i guess"""

    children: Collection["Fregian"]
    denotation: Literal
    label: str
    is_literal: bool = False

    def __str__(self):
        return f"{self.__class__.__name__}({",".join(map(str, self.children))})"

    @abc.abstractmethod
    def __json__(self) -> dict:
        pass

    def pprint(self):
        print(JsonExpression().format_sexpr(self.__json__()))


class Sense(Fregian):
    """the sense of an object is what its name expresses. frege, 1892"""

    label = "sense"

    def __init__(self, literal: str):
        self.denotation = Literal(literal)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.denotation}')"

    def __str__(self):
        return self.denotation.data

    def __json__(self) -> dict:
        return {
            "label": self.label,
            "sopen": "«",
            "sclose": "»",
            "denotation": self.denotation.data,
        }


class Concept(Fregian):
    """concepts are essentially the properties of an object when you take away
    its reference in the real world. they are formed by combining concepts,
    propositions, and senses"""

    label = "concept"

    def __init__(self, *elements: Conceptualizable):
        self.children = set(elements)

    def __json__(self) -> dict:
        children = [child.__json__() for child in self.children]

        return {
            "label": "concept",
            "children": children,
        }


class Proposition(Concept):
    """a proposition is a tree of concepts"""

    label = "proposition"

    def __init__(self, lhs: Propositionable, rhs: Propositionable, /):
        self.lhs = lhs
        self.rhs = rhs
        self.children = self.lhs, self.rhs

    def __json__(self) -> dict:
        return {
            "label": self.label,
            "sopen": "<",
            "sclose": ">",
            "children": [child.__json__() for child in self.children],
        }


class Sentence(Proposition):
    """a proposition is a complete tree of concepts. it has a truth value"""

    label = "sentence"


class Function(Proposition):
    """a proposition is an unresolved tree of concepts. it needs another proposition to be completed"""

    label = "function"


#  vim: set sw=4 ts=4 expandtab
