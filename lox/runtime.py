"""
Interpretador para SimpleLang.

Este módulo contém a lógica para percorrer a AST e executar o código SimpleLang.
"""

from .node import *
from .ctx import Context, SimpleLangFunction, SimpleLangCallable, Environment
from .errors import SimpleLangRuntimeError, SimpleLangDivisionByZeroError, SimpleLangReturnException, SimpleLangTypeError


class Interpreter(Visitor):
    """
    Interpretador principal para SimpleLang.
    
    Implementa o padrão Visitor para percorrer a AST e executar
    os statements e expressões.
    """
    
    def __init__(self):
        """Inicializa o interpretador com um contexto global."""
        self.context = Context()
    
    def interpret(self, statements):
        """
        Interpreta uma lista de statements.
        
        Args:
            statements (list): Lista de nós AST (statements)
        """
        for statement in statements:
            self.execute(statement)
    
    def execute(self, statement):
        """Executa um único statement."""
        statement.accept(self)
    
    def evaluate(self, expression):
        """Avalia uma única expressão."""
        return expression.accept(self)
    
    def execute_block(self, statements, environment):
        """
        Executa um bloco de statements em um novo ambiente.
        
        Args:
            statements (list): Lista de statements
            environment (Environment): O novo ambiente para o bloco
        """
        previous_environment = self.context.environment
        try:
            self.context.push_environment(environment)
            for statement in statements:
                self.execute(statement)
        finally:
            self.context.environment = previous_environment
    
    # --- Visitor Methods for Expressions ---
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        operator_value = expr.operator.value
        
        if operator_value == "+":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            elif isinstance(left, str) or isinstance(right, str):
                # Ensure both operands are stringified before concatenation
                return str(left) + str(right)
            else:
                raise SimpleLangTypeError(f"Operação inválida: {self._stringify(left)} {operator_value} {self._stringify(right)}")
        elif operator_value == "-":
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise SimpleLangTypeError(f"Operação inválida: {self._stringify(left)} {operator_value} {self._stringify(right)}")
            return left - right
        elif operator_value == "*":
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise SimpleLangTypeError(f"Operação inválida: {self._stringify(left)} {operator_value} {self._stringify(right)}")
            return left * right
        elif operator_value == "/":
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise SimpleLangTypeError(f"Operação inválida: {self._stringify(left)} {operator_value} {self._stringify(right)}")
            if right == 0:
                raise SimpleLangDivisionByZeroError()
            return left / right
        elif operator_value == "%" and isinstance(left, int) and isinstance(right, int):
            if right == 0:
                raise SimpleLangDivisionByZeroError()
            return left % right
        elif operator_value == "==":
            return left == right
        elif operator_value == "!=":
            return left != right
        elif operator_value == ">":
            return left > right
        elif operator_value == ">=":
            return left >= right
        elif operator_value == "<":
            return left < right
        elif operator_value == "<=":
            return left <= right
        elif operator_value == "and":
            return self._is_truthy(left) and self._is_truthy(right)
        elif operator_value == "or":
            return self._is_truthy(left) or self._is_truthy(right)
        
        raise SimpleLangRuntimeError(f"Operador binário desconhecido: {operator_value}")
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)
    
    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        
        operator_value = expr.operator.value
        
        if operator_value == "-":
            if not isinstance(right, (int, float)):
                raise SimpleLangTypeError(f"Operação inválida: {operator_value}{self._stringify(right)}")
            return -right
        elif operator_value == "!":
            return not self._is_truthy(right)
        
        raise SimpleLangRuntimeError(f"Operador unário desconhecido: {operator_value}")
    
    def visit_variable_expr(self, expr):
        return self.context.get_variable(expr.name)
    
    def visit_assignment_expr(self, expr):
        value = self.evaluate(expr.value)
        self.context.assign_variable(expr.name, value)
        return value
    
    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        
        if not isinstance(callee, SimpleLangCallable):
            raise SimpleLangRuntimeError(f"Não é possível chamar: {self._stringify(callee)}")
        
        return callee.call(self, arguments)
    
    # --- Visitor Methods for Statements ---
    
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
    
    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self._stringify(value))
    
    def visit_var_declaration_stmt(self, stmt):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.context.define_variable(stmt.name, value)
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.context.environment))
    
    def visit_if_stmt(self, stmt):
        if self._is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)
    
    def visit_while_stmt(self, stmt):
        while self._is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
    
    def visit_function_declaration_stmt(self, stmt):
        function = SimpleLangFunction(stmt, self.context.environment)
        self.context.define_function(stmt.name, function)
    
    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        raise SimpleLangReturnException(value)
    
    # --- Helper Methods ---
    
    def _is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        if isinstance(obj, (int, float)):
            return obj != 0
        if isinstance(obj, str):
            return len(obj) > 0
        return True
    
    def _stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, bool):
            return str(obj).lower()
        if isinstance(obj, float):
            if obj.is_integer():
                return str(int(obj))
            return str(obj)
        return str(obj)


