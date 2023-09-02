"""Produce ast"""
import ast
from pprint import pprint


def print_ast(code):
    """Print ast of code"""
    ast.parse(code)
    pprint(ast.dump(ast.parse(code)))
