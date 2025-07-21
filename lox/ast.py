"""
Construtor da Árvore Sintática Abstrata (AST) para SimpleLang.

Este módulo converte a árvore de parsing do Lark em uma AST mais estruturada
usando as classes de nós definidas em node.py.
"""

from lark import Tree, Token
from .node import *
from .errors import SimpleLangSyntaxError


class ASTBuilder:
    """
    Constrói a AST a partir da árvore de parsing do Lark.
    """
    
    def build(self, parse_tree):
        """
        Constrói a AST a partir da árvore de parsing.
        
        Args:
            parse_tree: Árvore de parsing do Lark
            
        Returns:
            list: Lista de statements que compõem o programa
        """
        if not isinstance(parse_tree, Tree) or parse_tree.data != 'program':
            raise SimpleLangSyntaxError("Árvore de parsing inválida")
        
        statements = []
        for child in parse_tree.children:
            stmt = self._build_statement(child)
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def _build_statement(self, tree):
        """Constrói um statement a partir de um nó da árvore."""
        if not isinstance(tree, Tree):
            return None
        
        method_name = f'_build_{tree.data}'
        method = getattr(self, method_name, None)
        if method:
            return method(tree)
        else:
            raise SimpleLangSyntaxError(f"Statement não implementado: {tree.data}")
    
    def _build_expression(self, tree):
        """Constrói uma expressão a partir de um nó da árvore."""
        if isinstance(tree, Token):
            return self._build_token(tree)
        
        if not isinstance(tree, Tree):
            return None
        
        method_name = f'_build_{tree.data}'
        method = getattr(self, method_name, None)
        if method:
            return method(tree)
        else:
            raise SimpleLangSyntaxError(f"Expressão não implementada: {tree.data}")
    
    def _build_token(self, token):
        """Constrói um literal a partir de um token."""
        if token.type == 'NUMBER':
            value = float(token.value) if '.' in token.value else int(token.value)
            return Literal(value, token)
        elif token.type == 'STRING':
            # Remove as aspas
            value = token.value[1:-1]
            return Literal(value, token)
        elif token.type == 'IDENTIFIER':
            return Variable(token.value, token)
        else:
            raise SimpleLangSyntaxError(f"Token não reconhecido: {token}")
    
    # --- Statements ---
    
    def _build_expression_stmt(self, tree):
        """Constrói um expression statement."""
        expr = self._build_expression(tree.children[0])
        return ExpressionStatement(expr, tree.meta)
    
    def _build_print_statement(self, tree):
        """Constrói um print statement."""
        expr = self._build_expression(tree.children[0])
        return PrintStatement(expr, tree.meta)
    
    def _build_var_declaration(self, tree):
        """Constrói uma declaração de variável."""
        name = tree.children[0].value  # IDENTIFIER
        initializer = None
        if len(tree.children) > 1:
            initializer = self._build_expression(tree.children[1])
        return VarDeclaration(name, initializer, tree.meta)
    
    def _build_block_statement(self, tree):
        """Constrói um bloco de statements."""
        statements = []
        for child in tree.children:
            stmt = self._build_statement(child)
            if stmt:
                statements.append(stmt)
        return BlockStatement(statements, tree.meta)
    
    def _build_if_statement(self, tree):
        """Constrói um if statement."""
        condition = self._build_expression(tree.children[0])
        then_branch = self._build_statement(tree.children[1])
        else_branch = None
        if len(tree.children) > 2:
            else_branch = self._build_statement(tree.children[2])
        return IfStatement(condition, then_branch, else_branch, tree.meta)
    
    def _build_while_statement(self, tree):
        """Constrói um while statement."""
        condition = self._build_expression(tree.children[0])
        body = self._build_statement(tree.children[1])
        return WhileStatement(condition, body, tree.meta)
    
    def _build_function_declaration(self, tree):
        """Constrói uma declaração de função."""
        name = tree.children[0].value  # IDENTIFIER
        parameters = []
        body_index = 1
        
        # Verifica se há parâmetros
        if len(tree.children) > 2 and isinstance(tree.children[1], Tree) and tree.children[1].data == 'parameters':
            params_tree = tree.children[1]
            for param in params_tree.children:
                parameters.append(param.value)
            body_index = 2
        
        body = self._build_statement(tree.children[body_index])
        return FunctionDeclaration(name, parameters, body, tree.meta)
    
    def _build_return_statement(self, tree):
        """Constrói um return statement."""
        value = None
        if tree.children:
            value = self._build_expression(tree.children[0])
        return ReturnStatement("return", value, tree.meta)
    
    # --- Expressões ---
    
    def _build_assignment(self, tree):
        """Constrói uma atribuição."""
        name = tree.children[0].value  # IDENTIFIER
        value = self._build_expression(tree.children[1])
        return Assignment(name, value, tree.meta)
    
    def _build_logical_or(self, tree):
        """Constrói uma expressão OR lógica."""
        return self._build_binary_expression(tree, "or")
    
    def _build_logical_and(self, tree):
        """Constrói uma expressão AND lógica."""
        return self._build_binary_expression(tree, "and")
    
    def _build_equality(self, tree):
        """Constrói uma expressão de igualdade."""
        return self._build_binary_expression(tree)
    
    def _build_comparison(self, tree):
        """Constrói uma expressão de comparação."""
        return self._build_binary_expression(tree)
    
    def _build_term(self, tree):
        """Constrói uma expressão de termo (+ -)."""
        return self._build_binary_expression(tree)
    
    def _build_factor(self, tree):
        """Constrói uma expressão de fator (* / %)."""
        return self._build_binary_expression(tree)
    
    def _build_binary_expression(self, tree, default_op=None):
        """Constrói uma expressão binária genérica."""
        if len(tree.children) == 1:
            return self._build_expression(tree.children[0])
        
        left = self._build_expression(tree.children[0])
        for i in range(1, len(tree.children), 2):
            operator = tree.children[i] if default_op is None else default_op
            right = self._build_expression(tree.children[i + 1])
            left = Binary(left, operator, right, tree.meta)
        
        return left
    
    def _build_unary(self, tree):
        """Constrói uma expressão unária."""
        if len(tree.children) == 1:
            return self._build_expression(tree.children[0])
        
        operator = tree.children[0]
        right = self._build_expression(tree.children[1])
        return Unary(operator, right, tree.meta)
    
    def _build_call(self, tree):
        """Constrói uma chamada de função."""
        callee = self._build_expression(tree.children[0])
        
        # Se há apenas um filho, não é uma chamada
        if len(tree.children) == 1:
            return callee
        
        # Processa argumentos se existirem
        arguments = []
        if len(tree.children) > 1 and isinstance(tree.children[1], Tree) and tree.children[1].data == 'arguments':
            args_tree = tree.children[1]
            for arg in args_tree.children:
                arguments.append(self._build_expression(arg))
        
        return Call(callee, tree.meta, arguments, tree.meta)
    
    def _build_grouping(self, tree):
        """Constrói uma expressão agrupada."""
        expr = self._build_expression(tree.children[0])
        return Grouping(expr, tree.meta)
    
    def _build_identifier(self, tree):
        """Constrói uma referência a variável."""
        return Variable(tree.children[0].value, tree.meta)
    
    def _build_number(self, tree):
        """Constrói um literal numérico."""
        value = tree.children[0].value
        num_value = float(value) if '.' in value else int(value)
        return Literal(num_value, tree.meta)
    
    def _build_string(self, tree):
        """Constrói um literal string."""
        value = tree.children[0].value[1:-1]  # Remove aspas
        return Literal(value, tree.meta)
    
    def _build_true(self, tree):
        """Constrói um literal true."""
        return Literal(True, tree.meta)
    
    def _build_false(self, tree):
        """Constrói um literal false."""
        return Literal(False, tree.meta)
    
    def _build_nil(self, tree):
        """Constrói um literal nil."""
        return Literal(None, tree.meta)


def build_ast(parse_tree):
    """
    Função utilitária para construir AST a partir de uma árvore de parsing.
    
    Args:
        parse_tree: Árvore de parsing do Lark
        
    Returns:
        list: Lista de statements da AST
    """
    builder = ASTBuilder()
    return builder.build(parse_tree)

