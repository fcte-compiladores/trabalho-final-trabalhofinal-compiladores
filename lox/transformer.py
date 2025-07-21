"""
Transformer para SimpleLang usando o padrão Transformer do Lark.

Este módulo implementa uma abordagem alternativa para construir a AST
usando o sistema de transformação integrado do Lark.
"""

from lark import Transformer, Token
from .node import *


class SimpleLangTransformer(Transformer):
    """
    Transformer que converte a árvore de parsing do Lark em AST.
    
    Cada método corresponde a uma regra da gramática e retorna
    o nó AST apropriado.
    """
    
    # --- Programa ---
    
    def program(self, statements):
        """Retorna lista de statements do programa."""
        return [stmt for stmt in statements if stmt is not None]
    
    # --- Statements ---
    
    def expression_stmt(self, items):
        """Expression statement."""
        return ExpressionStatement(items[0])
    
    def print_statement(self, items):
        """Print statement."""
        return PrintStatement(items[0])
    
    def var_declaration(self, items):
        """Declaração de variável."""
        name = items[0].value
        initializer = items[1] if len(items) > 1 else None
        return VarDeclaration(name, initializer)
    
    def function_declaration(self, items):
        """Declaração de função."""
        name = items[0].value
        parameters = []
        body_index = 1
        
        # Verifica se há parâmetros
        if len(items) > 2:
            parameters = items[1]
            body_index = 2
        
        body = items[body_index]
        return FunctionDeclaration(name, parameters, body)
    
    def parameters(self, items):
        """Lista de parâmetros de função."""
        return [param.value for param in items]
    
    def if_statement(self, items):
        """If statement."""
        condition = items[0]
        then_branch = items[1]
        else_branch = items[2] if len(items) > 2 else None
        return IfStatement(condition, then_branch, else_branch)
    
    def while_statement(self, items):
        """While statement."""
        condition = items[0]
        body = items[1]
        return WhileStatement(condition, body)
    
    def for_statement(self, items):
        """For statement - convertido para while."""
        # for (init; condition; increment) body
        # vira: { init; while (condition) { body; increment; } }
        init = items[0] if items[0] else None
        condition = items[1] if items[1] else Literal(True)
        increment = items[2] if items[2] else None
        body = items[3]
        
        # Constrói o corpo do while
        while_body_stmts = [body]
        if increment:
            while_body_stmts.append(ExpressionStatement(increment))
        while_body = BlockStatement(while_body_stmts)
        
        # Constrói o while
        while_stmt = WhileStatement(condition, while_body)
        
        # Constrói o bloco externo
        block_stmts = []
        if init:
            block_stmts.append(init)
        block_stmts.append(while_stmt)
        
        return BlockStatement(block_stmts)
    
    def return_statement(self, items):
        """Return statement."""
        value = items[0] if items else None
        return ReturnStatement("return", value)
    
    def block_statement(self, items):
        """Block statement."""
        return BlockStatement(items)
    
    # --- Expressões ---
    
    def assignment(self, items):
        """Atribuição."""
        if len(items) == 1:
            return items[0]
        name = items[0].value
        value = items[1]
        return Assignment(name, value)
    
    def logical_or(self, items):
        """OR lógico."""
        return self._build_binary_chain(items)
    
    def logical_and(self, items):
        """AND lógico."""
        return self._build_binary_chain(items)
    
    def equality(self, items):
        """Igualdade."""
        return self._build_binary_chain(items)
    
    def comparison(self, items):
        """Comparação."""
        return self._build_binary_chain(items)
    
    def term(self, items):
        """Termo (+ -)."""
        return self._build_binary_chain(items)
    
    def factor(self, items):
        """Fator (* / %)."""
        return self._build_binary_chain(items)
    
    def _build_binary_chain(self, items):
        """
        Constrói uma cadeia de expressões binárias.
        Espera que `items` seja uma lista de [expr, op, expr, op, expr, ...]
        ou apenas [expr].
        """
        if not items:
            return None
        
        # Se houver apenas um item, é uma expressão simples, não binária
        if len(items) == 1:
            return items[0]
        
        # Se houver mais de um item, assume-se que é uma cadeia de operações binárias
        # Ex: [expr1, op1, expr2, op2, expr3]
        left = items[0]
        i = 1
        while i < len(items):
            # Verifica se o próximo item é um operador (Token) e se há um operando à direita
            if isinstance(items[i], Token) and i + 1 < len(items):
                operator = items[i]
                right = items[i + 1]
                left = Binary(left, operator, right)
                i += 2
            else:
                # Se não for um operador ou não houver operando à direita, assume que é o fim da cadeia
                # Isso pode acontecer se a gramática permitir expressões como 'a + b' sem o 'c' subsequente
                break
        
        return left
    
    def unary(self, items):
        """Expressão unária."""
        if len(items) == 1:
            return items[0]
        operator = items[0]
        right = items[1]
        return Unary(operator, right)
    
    def call(self, items):
        """Chamada de função."""
        callee = items[0]
        
        # O último item pode ser a lista de argumentos ou None se não houver argumentos
        arguments = items[1] if len(items) > 1 else []
        
        # Certifica-se de que arguments é uma lista, mesmo que vazia
        if not isinstance(arguments, list):
            arguments = [arguments] if arguments is not None else []

        return Call(callee, None, arguments)
    
    def arguments(self, items):
        """Lista de argumentos."""
        return items
    
    def grouping(self, items):
        """Expressão agrupada."""
        return Grouping(items[0])
    
    # --- Literais ---
    
    def identifier(self, items):
        """Identificador (variável)."""
        return Variable(items[0].value)
    
    def number(self, items):
        """Literal numérico."""
        value = items[0].value
        num_value = float(value) if "." in value else int(value)
        return Literal(num_value)
    
    def string(self, items):
        """Literal string."""
        value = items[0].value[1:-1]  # Remove aspas
        return Literal(value)
    
    def true(self, items):
        """Literal true."""
        return Literal(True)
    
    def false(self, items):
        """Literal false."""
        return Literal(False)
    
    def nil(self, items):
        """Literal nil."""
        return Literal(None)


def transform_to_ast(parse_tree):
    """
    Transforma uma árvore de parsing em AST usando o transformer.
    
    Args:
        parse_tree: Árvore de parsing do Lark
        
    Returns:
        list: Lista de statements da AST
    """
    transformer = SimpleLangTransformer()
    return transformer.transform(parse_tree)


