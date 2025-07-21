"""
Testes de integração para SimpleLang.

Estes testes verificam o funcionamento completo do compilador,
desde o parsing até a execução, usando programas completos.
"""

import unittest
import sys
from io import StringIO
from pathlib import Path

# Adiciona o diretório pai ao path para importar o módulo lox
sys.path.insert(0, str(Path(__file__).parent.parent))

from lox.parser import Parser
from lox.transformer import transform_to_ast
from lox.runtime import Interpreter
from lox.errors import SimpleLangError


class TestSimpleLangIntegration(unittest.TestCase):
    """Testes de integração para programas completos em SimpleLang."""

    def setUp(self):
        self.parser = Parser()
        self.interpreter = Interpreter()

    def _run_program(self, code):
        """Executa um programa SimpleLang e retorna a saída."""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        try:
            tree = self.parser.parse(code)
            ast = transform_to_ast(tree)
            self.interpreter.interpret(ast)
            return captured_output.getvalue().strip()
        finally:
            sys.stdout = old_stdout

    def test_calculator_program(self):
        """Testa um programa calculadora simples."""
        code = """
        fun add(a, b) {
            return a + b;
        }
        
        fun multiply(a, b) {
            return a * b;
        }
        
        fun calculate(x, y) {
            var sum = add(x, y);
            var product = multiply(x, y);
            print "Soma: " + sum;
            print "Produto: " + product;
            return sum + product;
        }
        
        var result = calculate(3, 4);
        print "Resultado final: " + result;
        """
        output = self._run_program(code)
        expected = "Soma: 7\nProduto: 12\nResultado final: 19"
        self.assertEqual(output, expected)

    def test_fibonacci_iterative(self):
        """Testa implementação iterativa de Fibonacci."""
        code = """
        fun fibonacci(n) {
            if (n <= 1) {
                return n;
            }
            
            var a = 0;
            var b = 1;
            var i = 2;
            
            while (i <= n) {
                var temp = a + b;
                a = b;
                b = temp;
                i = i + 1;
            }
            
            return b;
        }
        
        var i = 0;
        while (i <= 5) {
            print "fib(" + i + ") = " + fibonacci(i);
            i = i + 1;
        }
        """
        output = self._run_program(code)
        expected = "fib(0) = 0\nfib(1) = 1\nfib(2) = 1\nfib(3) = 2\nfib(4) = 3\nfib(5) = 5"
        self.assertEqual(output, expected)

    def test_factorial_program(self):
        """Testa programa de cálculo de fatorial."""
        code = """
        fun factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        
        fun print_factorial(n) {
            var result = factorial(n);
            print n + "! = " + result;
        }
        
        print_factorial(0);
        print_factorial(1);
        print_factorial(3);
        print_factorial(5);
        """
        output = self._run_program(code)
        expected = "0! = 1\n1! = 1\n3! = 6\n5! = 120"
        self.assertEqual(output, expected)

    def test_scope_and_closures(self):
        """Testa escopo de variáveis e closures."""
        code = """
        var global = "global";
        
        fun outer() {
            var outer_var = "outer";
            
            fun inner() {
                var inner_var = "inner";
                print global;
                print outer_var;
                print inner_var;
            }
            
            inner();
            print "Back in outer";
        }
        
        outer();
        print "Back in global";
        """
        output = self._run_program(code)
        expected = "global\nouter\ninner\nBack in outer\nBack in global"
        self.assertEqual(output, expected)

    def test_control_flow_complex(self):
        """Testa estruturas de controle complexas."""
        code = """
        fun classify_number(n) {
            if (n > 0) {
                if (n % 2 == 0) {
                    print n + " é positivo e par";
                } else {
                    print n + " é positivo e ímpar";
                }
            } else {
                if (n == 0) {
                    print n + " é zero";
                } else {
                    if (n % 2 == 0) {
                        print n + " é negativo e par";
                    } else {
                        print n + " é negativo e ímpar";
                    }
                }
            }
        }
        
        var numbers = [5, -4, 0, 8, -3];
        var i = 0;
        while (i < 5) {
            if (i == 0) classify_number(5);
            if (i == 1) classify_number(-4);
            if (i == 2) classify_number(0);
            if (i == 3) classify_number(8);
            if (i == 4) classify_number(-3);
            i = i + 1;
        }
        """
        output = self._run_program(code)
        expected = "5 é positivo e ímpar\n-4 é negativo e par\n0 é zero\n8 é positivo e par\n-3 é negativo e ímpar"
        self.assertEqual(output, expected)

    def test_string_manipulation(self):
        """Testa manipulação de strings."""
        code = """
        fun greet(name, title) {
            return "Olá, " + title + " " + name + "!";
        }
        
        fun repeat_string(str, times) {
            var result = "";
            var i = 0;
            while (i < times) {
                result = result + str;
                i = i + 1;
            }
            return result;
        }
        
        print greet("Silva", "Dr.");
        print greet("Maria", "Sra.");
        print repeat_string("Ha", 3);
        print repeat_string("Echo ", 2);
        """
        output = self._run_program(code)
        expected = "Olá, Dr. Silva!\nOlá, Sra. Maria!\nHaHaHa\nEcho Echo "
        self.assertEqual(output, expected)

    def test_recursive_functions(self):
        """Testa funções recursivas complexas."""
        code = """
        fun gcd(a, b) {
            if (b == 0) {
                return a;
            }
            return gcd(b, a % b);
        }
        
        fun power(base, exp) {
            if (exp == 0) {
                return 1;
            }
            if (exp == 1) {
                return base;
            }
            if (exp % 2 == 0) {
                var half = power(base, exp / 2);
                return half * half;
            } else {
                return base * power(base, exp - 1);
            }
        }
        
        print "GCD(48, 18) = " + gcd(48, 18);
        print "GCD(100, 25) = " + gcd(100, 25);
        print "2^10 = " + power(2, 10);
        print "3^4 = " + power(3, 4);
        """
        output = self._run_program(code)
        expected = "GCD(48, 18) = 6\nGCD(100, 25) = 25\n2^10 = 1024\n3^4 = 81"
        self.assertEqual(output, expected)

    def test_boolean_logic_complex(self):
        """Testa lógica booleana complexa."""
        code = """
        fun is_valid_age(age) {
            return age >= 0 and age <= 150;
        }
        
        fun can_vote(age, citizen) {
            return is_valid_age(age) and age >= 18 and citizen;
        }
        
        fun can_drink(age, country) {
            var legal_age = 21;
            if (country == "BR") {
                legal_age = 18;
            }
            return is_valid_age(age) and age >= legal_age;
        }
        
        print "Idade 25 válida: " + is_valid_age(25);
        print "Idade -5 válida: " + is_valid_age(-5);
        print "Pode votar (20, true): " + can_vote(20, true);
        print "Pode votar (16, true): " + can_vote(16, true);
        print "Pode beber no BR (19): " + can_drink(19, "BR");
        print "Pode beber nos EUA (19): " + can_drink(19, "US");
        """
        output = self._run_program(code)
        expected = "Idade 25 válida: true\nIdade -5 válida: false\nPode votar (20, true): true\nPode votar (16, true): false\nPode beber no BR (19): true\nPode beber nos EUA (19): false"
        self.assertEqual(output, expected)


class TestSimpleLangFileExecution(unittest.TestCase):
    """Testa a execução de arquivos SimpleLang."""

    def setUp(self):
        self.examples_dir = Path(__file__).parent.parent / "examples"

    def test_hello_world_file(self):
        """Testa execução do arquivo hello_world.sl."""
        if (self.examples_dir / "hello_world.sl").exists():
            from lox.cli import run_file
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            try:
                run_file(self.examples_dir / "hello_world.sl")
                output = captured_output.getvalue().strip()
                self.assertEqual(output, "Hello, World!")
            finally:
                sys.stdout = old_stdout

    def test_if_else_file(self):
        """Testa execução do arquivo if_else.sl."""
        if (self.examples_dir / "if_else.sl").exists():
            from lox.cli import run_file
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            try:
                run_file(self.examples_dir / "if_else.sl")
                output = captured_output.getvalue().strip()
                self.assertEqual(output, "x é menor que y")
            finally:
                sys.stdout = old_stdout


if __name__ == "__main__":
    unittest.main(verbosity=2)

