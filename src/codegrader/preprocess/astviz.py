#!/usr/bin/python3
import ast
import sys
import re
import numbers
from uuid import uuid4 as uuid
from pprint import pprint

import graphviz as gv


def view_ast(code: str, graph: bool = True) -> None:
    """View ast graph and print AST structure

    Args:
        code (str): _description_
    """
    code_ast = ast.parse(code)
    pprint(ast.dump(code_ast))
    if not graph:
        return
    transformed_ast = transform_ast(code_ast)

    renderer = GraphRenderer()
    renderer.render(transformed_ast, label="Code")


def transform_ast(code_ast):
    """Transform AST to a dict

    Args:
        code_ast (Module): AST module

    Returns:
        dict | list: AST as a dict
    """
    if isinstance(code_ast, ast.AST):
        node = {
            to_camelcase(k): transform_ast(getattr(code_ast, k))
            for k in code_ast._fields
        }
        node["node_type"] = to_camelcase(code_ast.__class__.__name__)
        return node
    if isinstance(code_ast, list):
        return [transform_ast(el) for el in code_ast]
    return code_ast


def to_camelcase(string: str) -> str:
    """Convert string to camelcase

    Args:
        string (str): input string

    Returns:
        str: camelcase string
    """
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()


class GraphRenderer:
    """
    this class is capable of rendering data structures consisting of
    dicts and lists as a graph using graphviz
    """

    graphattrs = {
        "labelloc": "t",
        "fontcolor": "white",
        "bgcolor": "#333333",
        "margin": "0",
    }

    nodeattrs = {
        "color": "white",
        "fontcolor": "white",
        "style": "filled",
        "fillcolor": "#006699",
    }

    edgeattrs = {
        "color": "white",
        "fontcolor": "white",
    }

    _graph = None
    _rendered_nodes = None

    @staticmethod
    def _escape_dot_label(string):
        return (
            string.replace("\\", "\\\\")
            .replace("|", "\\|")
            .replace("<", "\\<")
            .replace(">", "\\>")
        )

    def _render_node(self, node):
        if isinstance(node, (str, numbers.Number)) or node is None:
            node_id = uuid()
        else:
            node_id = id(node)
        node_id = str(node_id)

        if node_id not in self._rendered_nodes:
            self._rendered_nodes.add(node_id)
            if isinstance(node, dict):
                self._render_dict(node, node_id)
            elif isinstance(node, list):
                self._render_list(node, node_id)
            else:
                self._graph.node(node_id, label=self._escape_dot_label(str(node)))

        return node_id

    def _render_dict(self, node, node_id):
        self._graph.node(node_id, label=node.get("node_type", "[dict]"))
        for key, value in node.items():
            if key == "node_type":
                continue
            child_node_id = self._render_node(value)
            self._graph.edge(node_id, child_node_id, label=self._escape_dot_label(key))

    def _render_list(self, node, node_id):
        self._graph.node(node_id, label="[list]")
        for idx, value in enumerate(node):
            child_node_id = self._render_node(value)
            self._graph.edge(
                node_id, child_node_id, label=self._escape_dot_label(str(idx))
            )

    def render(self, data, *, label=None):
        # create the graph
        graphattrs = self.graphattrs.copy()
        if label is not None:
            graphattrs["label"] = self._escape_dot_label(label)
        graph = gv.Digraph(
            graph_attr=graphattrs, node_attr=self.nodeattrs, edge_attr=self.edgeattrs
        )

        # recursively draw all the nodes and edges
        self._graph = graph
        self._rendered_nodes = set()
        self._render_node(data)
        self._graph = None
        self._rendered_nodes = None

        # display the graph
        graph.format = "pdf"
        graph.view()
