"""
SimpleLang - Um interpretador para uma linguagem de programação simples.

Este módulo implementa um interpretador completo para SimpleLang,
incluindo análise léxica, sintática, semântica e execução.
"""

__version__ = "1.0.0"
__author__ = "Arthur Henrique Vieira, Gabriel Soares dos Anjos"

from .parser import Parser
from .transformer import transform_to_ast
from .runtime import Interpreter
from .errors import SimpleLangError

__all__ = [
    "Parser",
    "transform_to_ast", 
    "Interpreter",
    "SimpleLangError"
]

