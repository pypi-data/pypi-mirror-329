from .equation import solve, Solve
from .likning import løs, Løs
from .function import function, Function
from .funksjon import funksjon, Funksjon
from .algebra import (
    expand,
    factor,
    utvid,
    Utvid,
    faktoriser,
    Faktoriser,
    div,
    Div,
    polynomdivisjon,
    Polynomdivisjon,
)
from .regression import make_model
from .regresjon import lag_modell

from .vector import vector, Vector2d

from .vektor import vektor, Vektor2d, vinkel

from . import abc


__all__ = [
    "solve",
    "løs",
    "Solve",
    "Løs",
    "function",
    "Function",
    "funksjon",
    "Funksjon",
    "expand",
    "factor",
    "utvid",
    "Utvid",
    "faktoriser",
    "Faktoriser",
    "div",
    "Div",
    "polynomdivisjon",
    "Polynomdivisjon",
    "vector",
    "Vector2d",
    "vektor",
    "Vektor2d",
    "vinkel",
    "lag_modell",
    "make_model",
]
