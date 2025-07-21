"""
Sistema de contexto e escopo para SimpleLang.

Este módulo implementa o gerenciamento de escopos, variáveis e funções
durante a análise semântica e execução de programas SimpleLang.
"""

from typing import Dict, Any, Optional, List
from .errors import SimpleLangUndefinedVariableError, SimpleLangUndefinedFunctionError


class Environment:
    """
    Representa um ambiente/escopo de execução.
    
    Cada ambiente mantém um mapeamento de nomes para valores
    e uma referência ao ambiente pai (escopo externo).
    """
    
    def __init__(self, enclosing: Optional["Environment"] = None):
        """
        Inicializa um novo ambiente.
        
        Args:
            enclosing: Ambiente pai (escopo externo)
        """
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing
    
    def define(self, name: str, value: Any) -> None:
        """
        Define uma nova variável no ambiente atual.
        
        Args:
            name: Nome da variável
            value: Valor da variável
        """
        self.values[name] = value
    
    def get(self, name: str) -> Any:
        """
        Obtém o valor de uma variável.
        
        Args:
            name: Nome da variável
            
        Returns:
            Valor da variável
            
        Raises:
            SimpleLangUndefinedVariableError: Se a variável não existe
        """
        if name in self.values:
            return self.values[name]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise SimpleLangUndefinedVariableError(name)
    
    def assign(self, name: str, value: Any) -> None:
        """
        Atribui um valor a uma variável existente.
        
        Args:
            name: Nome da variável
            value: Novo valor
            
        Raises:
            SimpleLangUndefinedVariableError: Se a variável não existe
        """
        if name in self.values:
            self.values[name] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise SimpleLangUndefinedVariableError(name)
    
    def contains(self, name: str) -> bool:
        """
        Verifica se uma variável existe no ambiente ou em seus pais.
        
        Args:
            name: Nome da variável
            
        Returns:
            True se a variável existe, False caso contrário
        """
        if name in self.values:
            return True
        
        if self.enclosing is not None:
            return self.enclosing.contains(name)
        
        return False


class SimpleLangCallable:
    """
    Interface para objetos que podem ser chamados (funções).
    """
    
    def call(self, interpreter, arguments: List[Any]) -> Any:
        """Chama o objeto com os argumentos fornecidos."""
        raise NotImplementedError
    
    def arity(self) -> int:
        """Retorna o número de argumentos esperados."""
        raise NotImplementedError


class SimpleLangFunction(SimpleLangCallable):
    """
    Representa uma função definida pelo usuário em SimpleLang.
    """
    
    def __init__(self, declaration, closure: Environment):
        """
        Inicializa uma função.
        
        Args:
            declaration: Nó AST da declaração da função
            closure: Ambiente onde a função foi declarada (closure)
        """
        self.declaration = declaration
        self.closure = closure
    
    def call(self, interpreter, arguments: List[Any]) -> Any:
        """
        Chama a função com os argumentos fornecidos.
        
        Args:
            interpreter: Instância do interpretador
            arguments: Lista de argumentos
            
        Returns:
            Valor retornado pela função
        """
        from .errors import SimpleLangArityError, SimpleLangReturnException
        
        # Verifica aridade
        if len(arguments) != len(self.declaration.parameters):
            raise SimpleLangArityError(
                self.declaration.name,
                len(self.declaration.parameters),
                len(arguments)
            )
        
        # Cria novo ambiente para a função
        # O ambiente da função deve ter o closure como seu ambiente pai
        environment = Environment(self.closure)
        
        # Vincula parâmetros aos argumentos
        for i, param in enumerate(self.declaration.parameters):
            environment.define(param, arguments[i])
        
        # Executa o corpo da função no novo ambiente
        try:
            interpreter.execute_block(self.declaration.body.statements, environment)
        except SimpleLangReturnException as return_value:
            return return_value.value
        
        # Se não houve return explícito, retorna nil
        return None
    
    def arity(self) -> int:
        """
        Retorna o número de parâmetros da função.
        """
        return len(self.declaration.parameters)
    
    def __str__(self) -> str:
        return f"<função {self.declaration.name}>"


class Context:
    """
    Contexto global do interpretador SimpleLang.
    
    Mantém o estado global, incluindo o ambiente global
    e funções built-in.
    """
    
    def __init__(self):
        """
        Inicializa o contexto com o ambiente global.
        """
        self.globals = Environment()
        self.environment = self.globals
        
        # Define funções built-in
        self._define_builtins()
    
    def _define_builtins(self):
        """
        Define funções built-in no ambiente global.
        """
        # Por enquanto, não temos funções built-in além de print
        # que é tratado como statement especial
        pass
    
    def push_environment(self, environment: Environment):
        """
        Empurra um novo ambiente na pilha.
        
        Args:
            environment: Novo ambiente a ser usado
        """
        self.environment = environment
    
    def pop_environment(self):
        """
        Remove o ambiente atual da pilha.
        """
        if self.environment.enclosing is not None:
            self.environment = self.environment.enclosing
    
    def define_variable(self, name: str, value: Any):
        """
        Define uma variável no ambiente atual.
        
        Args:
            name: Nome da variável
            value: Valor da variável
        """
        self.environment.define(name, value)
    
    def get_variable(self, name: str) -> Any:
        """
        Obtém o valor de uma variável.
        
        Args:
            name: Nome da variável
            
        Returns:
            Valor da variável
        """
        return self.environment.get(name)
    
    def assign_variable(self, name: str, value: Any):
        """
        Atribui um valor a uma variável existente.
        
        Args:
            name: Nome da variável
            value: Novo valor
        """
        self.environment.assign(name, value)
    
    def define_function(self, name: str, function: SimpleLangFunction):
        """
        Define uma função no ambiente atual.
        
        Args:
            name: Nome da função
            function: Objeto função
        """
        self.environment.define(name, function)
    
    def get_function(self, name: str) -> SimpleLangFunction:
        """
        Obtém uma função pelo nome.
        
        Args:
            name: Nome da função
            
        Returns:
            Objeto função
            
        Raises:
            SimpleLangUndefinedFunctionError: Se a função não existe
        """
        try:
            func = self.environment.get(name)
            if not isinstance(func, SimpleLangFunction):
                raise SimpleLangUndefinedFunctionError(name)
            return func
        except SimpleLangUndefinedVariableError:
            raise SimpleLangUndefinedFunctionError(name)


def create_global_context() -> Context:
    """
    Cria um contexto global padrão para SimpleLang.
    
    Returns:
        Contexto global inicializado
    """
    return Context()


