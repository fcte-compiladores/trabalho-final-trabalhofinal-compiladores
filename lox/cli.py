"""
Interface de linha de comando (CLI) para o interpretador SimpleLang.

Permite executar arquivos SimpleLang ou entrar em modo interativo.
"""

import argparse
import sys
from pathlib import Path

from .parser import Parser
from .transformer import transform_to_ast
from .runtime import Interpreter
from .errors import SimpleLangError, SimpleLangSyntaxError

def run_file(filepath: Path):
    """
    Executa um arquivo SimpleLang.
    
    Args:
        filepath: Caminho para o arquivo SimpleLang.
    """
    parser = Parser()
    interpreter = Interpreter()
    
    try:
        source_code = filepath.read_text(encoding="utf-8")
        tree = parser.parse(source_code, str(filepath))
        ast = transform_to_ast(tree)
        interpreter.interpret(ast)
    except SimpleLangError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(65) # EXIT_DATAERR
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        sys.exit(70) # EXIT_SOFTWARE

def run_prompt():
    """
    Inicia o modo interativo (REPL) do SimpleLang.
    """
    parser = Parser()
    interpreter = Interpreter()
    
    print("SimpleLang REPL (Ctrl+C para sair)")
    while True:
        try:
            code = input(">>> ")
            if not code.strip():
                continue
            
            # Permite declarações e expressões no REPL
            # Tenta como statement, se falhar, tenta como expressão
            try:
                tree = parser.parse(code + ";") # Adiciona ; para forçar statement
                ast = transform_to_ast(tree)
                interpreter.interpret(ast)
            except SimpleLangSyntaxError:
                # Tenta como expressão se falhar como statement
                try:
                    # Para expressões, precisamos de uma regra de entrada diferente
                    # ou adaptar a gramática para REPL
                    # Por simplicidade, vamos apenas tentar avaliar a expressão
                    # Isso pode ser melhorado com uma gramática específica para REPL
                    tree = parser.parser.parse(code, start='expression')
                    expr_ast = SimpleLangTransformer().transform(tree)
                    result = interpreter.evaluate(expr_ast)
                    if result is not None:
                        print(interpreter._stringify(result))
                except Exception as le:
                    print(f"Erro de sintaxe: {le}", file=sys.stderr)
            except SimpleLangError as e:
                print(f"Erro: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Erro inesperado: {e}", file=sys.stderr)
        except EOFError:
            print("Saindo...")
            break
        except KeyboardInterrupt:
            print("\nSaindo...")
            break

def main():
    parser = argparse.ArgumentParser(description="Interpretador SimpleLang")
    parser.add_argument("file", nargs="?", help="Caminho para o arquivo SimpleLang")
    
    args = parser.parse_args()
    
    if args.file:
        run_file(Path(args.file))
    else:
        run_prompt()

if __name__ == "__main__":
    main()

