"""
Parser para SimpleLang usando Lark.

Este módulo implementa o analisador léxico e sintático para a linguagem SimpleLang.
Utiliza a biblioteca Lark para parsing LALR baseado na gramática definida em grammar.lark.
"""

import os
from pathlib import Path
from lark import Lark, LarkError
from .errors import SimpleLangSyntaxError


class Parser:
    """
    Parser principal para SimpleLang.
    
    Carrega a gramática do arquivo grammar.lark e fornece métodos
    para fazer parsing de código fonte SimpleLang.
    """
    
    def __init__(self):
        """Inicializa o parser carregando a gramática."""
        self._load_grammar()
        self.parser = Lark(
            self.grammar,
            start='program',
            parser='lalr',
            propagate_positions=True,
            maybe_placeholders=False
        )
    
    def _load_grammar(self):
        """Carrega a gramática do arquivo grammar.lark."""
        grammar_path = Path(__file__).parent / 'grammar.lark'
        try:
            with open(grammar_path, 'r', encoding='utf-8') as f:
                self.grammar = f.read()
        except FileNotFoundError:
            raise SimpleLangSyntaxError(f"Arquivo de gramática não encontrado: {grammar_path}")
        except Exception as e:
            raise SimpleLangSyntaxError(f"Erro ao carregar gramática: {e}")
    
    def parse(self, source_code, filename="<string>"):
        """
        Faz o parsing do código fonte SimpleLang.
        
        Args:
            source_code (str): Código fonte a ser analisado
            filename (str): Nome do arquivo (para relatórios de erro)
            
        Returns:
            Tree: Árvore sintática gerada pelo Lark
            
        Raises:
            SimpleLangSyntaxError: Em caso de erro de sintaxe
        """
        try:
            return self.parser.parse(source_code)
        except LarkError as e:
            # Converte erros do Lark para nosso formato de erro
            raise SimpleLangSyntaxError(f"Erro de sintaxe em {filename}: {e}")
    
    def parse_file(self, filepath):
        """
        Faz o parsing de um arquivo SimpleLang.
        
        Args:
            filepath (str): Caminho para o arquivo
            
        Returns:
            Tree: Árvore sintática gerada pelo Lark
            
        Raises:
            SimpleLangSyntaxError: Em caso de erro de sintaxe ou arquivo não encontrado
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()
            return self.parse(source_code, filepath)
        except FileNotFoundError:
            raise SimpleLangSyntaxError(f"Arquivo não encontrado: {filepath}")
        except Exception as e:
            raise SimpleLangSyntaxError(f"Erro ao ler arquivo {filepath}: {e}")


def create_parser():
    """Factory function para criar uma instância do parser."""
    return Parser()

