import ast


class AstNodeVisitorWithContext:
    """
    This class is pretty much a copy of ast.NodeVisitor but with local context and a few extras
    """

    def __init__(self, code):
        self.code_lines = code.split('\n')

    def visit(self, node, context={'locals': set()}):
        """Visit a node."""
        method = 'base_visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor:
            visitor(node, context.copy())
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, context.copy())

    def generic_visit(self, node, context):
        """Called if no explicit visitor function exists for a node."""
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, context)
            elif isinstance(value, ast.AST):
                self.visit(value, context)

    def _create_syntax_exception(self, error, node=None):
        if node is not None and hasattr(node, 'lineno'):
            return SyntaxError(error, ("__user_code__", node.lineno, node.col_offset, self.code_lines[node.lineno-1]))
        else:
            return SyntaxError(error, ("__user_code__", None, None, None))

    def base_visit_Assign(self, node, context):
        for target in node.targets:
            if isinstance(target, ast.Name):
                context['locals'].add(target.id)
            elif isinstance(target, ast.Attribute) and target.value.id == 'self':
                context['locals'].add(target.value.id)

    def base_visit_For(self, node, context):
        targets = [node.target] if not isinstance(node.target, ast.Tuple) else node.target.elts
        for e in targets:
            context['locals'].add(e.id)