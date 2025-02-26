"""Miscellenous tools using ast"""

import ast


def remove_docstrings(code: str) -> str:
    '''
    Remove docstrings from the given Python code.

    Args:
        code (str): A string containing Python code.

    Returns:
        str: The same code with docstrings removed.

    Examples:
        >>> code = \'\'\'
        ... def foo():
        ...     """This is a docstring."""
        ...     print("Hello")
        ...
        ... class Bar:
        ...     """Class docstring."""
        ...     def baz(self):
        ...         """Method docstring."""
        ...         pass
        ... \'\'\'
        >>> print(remove_docstrings(code))
        def foo():
            print('Hello')
        <BLANKLINE>
        class Bar:
        <BLANKLINE>
            def baz(self):
                pass
    '''

    class DocstringRemover(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Str)
            ):
                node.body = node.body[
                    1:
                ]  # Remove the first expression if it's a docstring
            return node

        def visit_ClassDef(self, node):
            self.generic_visit(node)
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Str)
            ):
                node.body = node.body[
                    1:
                ]  # Remove the first expression if it's a docstring
            return node

        def visit_Module(self, node):
            self.generic_visit(node)
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Str)
            ):
                node.body = node.body[
                    1:
                ]  # Remove the first expression if it's a docstring
            return node

    parsed_ast = ast.parse(code)
    transformer = DocstringRemover()
    cleaned_ast = transformer.visit(parsed_ast)
    return ast.unparse(cleaned_ast)
