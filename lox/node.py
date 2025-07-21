"""
Definição dos nós da Árvore Sintática Abstrata (AST) para SimpleLang.

Cada classe representa um tipo de nó na AST, facilitando a travessia e a interpretação.
"""

class Node:
    """Classe base para todos os nós da AST."""
    def __init__(self, token=None):
        self.token = token  # O token Lark associado a este nó, para informações de linha/coluna

    def accept(self, visitor):
        """Método para o padrão Visitor, a ser implementado por subclasses."""
        raise NotImplementedError

class Expression(Node):
    """Classe base para nós que representam expressões."""
    pass

class Statement(Node):
    """Classe base para nós que representam declarações (statements)."""
    pass

# --- Expressões ---

class Binary(Expression):
    """Expressão binária (ex: 1 + 2, a == b)."""
    def __init__(self, left, operator, right, token=None):
        super().__init__(token or operator)
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Grouping(Expression):
    """Expressão agrupada por parênteses (ex: (1 + 2))."""
    def __init__(self, expression, token=None):
        super().__init__(token)
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expression):
    """Literal (número, string, booleano, nil)."""
    def __init__(self, value, token=None):
        super().__init__(token)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Unary(Expression):
    """Expressão unária (ex: -1, !true)."""
    def __init__(self, operator, right, token=None):
        super().__init__(token or operator)
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Variable(Expression):
    """Referência a uma variável."""
    def __init__(self, name, token=None):
        super().__init__(token or name)
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Assignment(Expression):
    """Atribuição de valor a uma variável."""
    def __init__(self, name, value, token=None):
        super().__init__(token or name)
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment_expr(self)

class Call(Expression):
    """Chamada de função."""
    def __init__(self, callee, paren, arguments, token=None):
        super().__init__(token or paren)
        self.callee = callee
        self.paren = paren  # Token do parêntese de abertura para erros
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

# --- Statements ---

class ExpressionStatement(Statement):
    """Statement que consiste apenas em uma expressão (ex: 1 + 2;)."""
    def __init__(self, expression, token=None):
        super().__init__(token)
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class PrintStatement(Statement):
    """Statement de impressão (ex: print "hello";)."""
    def __init__(self, expression, token=None):
        super().__init__(token)
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class VarDeclaration(Statement):
    """Declaração de variável (ex: var x = 10;)."""
    def __init__(self, name, initializer, token=None):
        super().__init__(token or name)
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_declaration_stmt(self)

class BlockStatement(Statement):
    """Bloco de statements (ex: { statement1; statement2; })."""
    def __init__(self, statements, token=None):
        super().__init__(token)
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class IfStatement(Statement):
    """Statement condicional if/else."""
    def __init__(self, condition, then_branch, else_branch, token=None):
        super().__init__(token)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class WhileStatement(Statement):
    """Loop while."""
    def __init__(self, condition, body, token=None):
        super().__init__(token)
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class FunctionDeclaration(Statement):
    """Declaração de função."""
    def __init__(self, name, parameters, body, token=None):
        super().__init__(token or name)
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_declaration_stmt(self)

class ReturnStatement(Statement):
    """Statement de retorno de função."""
    def __init__(self, keyword, value, token=None):
        super().__init__(token or keyword)
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)

# --- Visitor Pattern ---

class Visitor:
    """Classe base para o padrão Visitor."""
    def visit_binary_expr(self, expr):
        raise NotImplementedError

    def visit_grouping_expr(self, expr):
        raise NotImplementedError

    def visit_literal_expr(self, expr):
        raise NotImplementedError

    def visit_unary_expr(self, expr):
        raise NotImplementedError

    def visit_variable_expr(self, expr):
        raise NotImplementedError

    def visit_assignment_expr(self, expr):
        raise NotImplementedError

    def visit_call_expr(self, expr):
        raise NotImplementedError

    def visit_expression_stmt(self, stmt):
        raise NotImplementedError

    def visit_print_stmt(self, stmt):
        raise NotImplementedError

    def visit_var_declaration_stmt(self, stmt):
        raise NotImplementedError

    def visit_block_stmt(self, stmt):
        raise NotImplementedError

    def visit_if_stmt(self, stmt):
        raise NotImplementedError

    def visit_while_stmt(self, stmt):
        raise NotImplementedError

    def visit_function_declaration_stmt(self, stmt):
        raise NotImplementedError

    def visit_return_stmt(self, stmt):
        raise NotImplementedError


