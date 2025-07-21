"""
Sistema de tratamento de erros para SimpleLang.

Define as classes de exceção personalizadas para diferentes tipos de erros
que podem ocorrer durante a compilação e execução de programas SimpleLang.
"""


class SimpleLangError(Exception):
    """Classe base para todos os erros da SimpleLang."""
    
    def __init__(self, message, line=None, column=None, filename=None):
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename
        super().__init__(self.format_error())
    
    def format_error(self):
        """Formata a mensagem de erro com informações de localização."""
        location = ""
        if self.filename:
            location += f"Arquivo '{self.filename}'"
        if self.line is not None:
            if location:
                location += f", linha {self.line}"
            else:
                location += f"Linha {self.line}"
        if self.column is not None:
            location += f", coluna {self.column}"
        
        if location:
            return f"{location}: {self.message}"
        return self.message


class SimpleLangSyntaxError(SimpleLangError):
    """Erro de sintaxe durante o parsing."""
    pass


class SimpleLangNameError(SimpleLangError):
    """Erro de nome - variável ou função não declarada."""
    pass


class SimpleLangTypeError(SimpleLangError):
    """Erro de tipo - operação inválida para o tipo."""
    pass


class SimpleLangRuntimeError(SimpleLangError):
    """Erro durante a execução do programa."""
    pass


class SimpleLangReturnException(Exception):
    """
    Exceção especial para implementar o statement 'return'.
    Não é um erro, mas usa o mecanismo de exceção para controle de fluxo.
    """
    
    def __init__(self, value):
        self.value = value
        super().__init__()


class SimpleLangDivisionByZeroError(SimpleLangRuntimeError):
    """Erro específico para divisão por zero."""
    
    def __init__(self, line=None, column=None, filename=None):
        super().__init__("Divisão por zero", line, column, filename)


class SimpleLangUndefinedVariableError(SimpleLangNameError):
    """Erro específico para variável não definida."""
    
    def __init__(self, variable_name, line=None, column=None, filename=None):
        message = f"Variável '{variable_name}' não foi declarada"
        super().__init__(message, line, column, filename)


class SimpleLangUndefinedFunctionError(SimpleLangNameError):
    """Erro específico para função não definida."""
    
    def __init__(self, function_name, line=None, column=None, filename=None):
        message = f"Função '{function_name}' não foi declarada"
        super().__init__(message, line, column, filename)


class SimpleLangArityError(SimpleLangRuntimeError):
    """Erro de aridade - número incorreto de argumentos para função."""
    
    def __init__(self, function_name, expected, actual, line=None, column=None, filename=None):
        message = f"Função '{function_name}' espera {expected} argumentos, mas recebeu {actual}"
        super().__init__(message, line, column, filename)


def error_handler(func):
    """
    Decorator para capturar e formatar erros de forma consistente.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SimpleLangError:
            # Re-raise erros da SimpleLang sem modificação
            raise
        except Exception as e:
            # Converte outros erros para SimpleLangRuntimeError
            raise SimpleLangRuntimeError(f"Erro interno: {e}")
    return wrapper

