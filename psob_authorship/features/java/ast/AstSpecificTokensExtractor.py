from typing import List, Tuple

from psob_authorship.features.java.ast.Ast import Ast
from psob_authorship.features.java.ast.AstNode import AstNode
from psob_authorship.features.java.ast.AstVisitor import AstVisitor


class AstSpecificTokensExtractor:
    def __init__(self, ast: Ast) -> None:
        super().__init__()
        self.ast = ast

    def extract_tokens_by_nodes(self, node_names: List[List[int]]) -> List[Tuple[str, bool]]:
        visitor = AstSpecificNodesVisitor(node_names)
        self.ast.accept(visitor)
        return visitor.token_names


class AstSpecificNodesVisitor(AstVisitor):
    def __init__(self, node_names: List[List[int]]) -> None:
        self.node_names = node_names
        self.token_names: List[(str, bool)] = []
        self.visiting_for_control = False

    def visit(self, node: AstNode):
        if node.node_name == "forControl" or node.node_name == "enhancedForControl":
            self.visiting_for_control = True
        for i, node_name in enumerate(self.node_names[0]):
            if node.node_name == node_name:
                token_name = node.children[self.node_names[1][i]].token_name
                if token_name != "null":
                    self.token_names.append((token_name, self.visiting_for_control))
        super().visit(node)
        if node.node_name == "forControl" or node.node_name == "enhancedForControl":
            self.visiting_for_control = False
