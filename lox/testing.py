"""
Sistema de testes para SimpleLang.

Contém testes unitários para verificar o funcionamento correto
do parser, AST, interpretador e outras funcionalidades.
"""

import unittest
from io import StringIO
import sys

from .parser import Parser
from .transformer import transform_to_ast
from .runtime import Interpreter
from .errors import SimpleLangError, SimpleLangSyntaxError, SimpleLangRuntimeError


class TestSimpleLangParser(unittest.TestCase):
    """Testes para o parser SimpleLang."""
    
    def setUp(self):
        self.parser = Parser()
    
    def test_parse_simple_expression(self):
        """Testa parsing de expressão simples."""
        code = "print 42;"
        tree = self.parser.parse(code)
        self.assertIsNotNone(tree)
    
    def test_parse_variable_declaration(self):
        """Testa parsing de declaração de variável."""
        code = "var x = 10;"
        tree = self.parser.parse(code)
        self.assertIsNotNone(tree)
    
    def test_parse_function_declaration(self):
        """Testa parsing de declaração de função."""
        code = """
        fun greet(name) {
            print "Hello, " + name;
        }
        """
        tree = self.parser.parse(code)
        self.assertIsNotNone(tree)
    
    def test_parse_if_statement(self):
        """Testa parsing de statement if."""
        code = """
        if (x > 0) {
            print "positive";
        } else {
            print "not positive";
        }
        """
        tree = self.parser.parse(code)
        self.assertIsNotNone(tree)
    
    def test_parse_while_loop(self):
        """Testa parsing de loop while."""
        code = """
        while (i < 10) {
            print i;
            i = i + 1;
        }
        """
        tree = self.parser.parse(code)
        self.assertIsNotNone(tree)
    
    def test_parse_syntax_error(self):
        """Testa detecção de erro de sintaxe."""
        code = "var x = ;"  # Sintaxe inválida
        with self.assertRaises(SimpleLangSyntaxError):
            self.parser.parse(code)


class TestSimpleLangInterpreter(unittest.TestCase):
    """Testes para o interpretador SimpleLang."""
    
    def setUp(self):
        self.parser = Parser()
        self.interpreter = Interpreter()
    
    def _run_code(self, code):
        """Helper para executar código SimpleLang."""
        tree = self.parser.parse(code)
        ast = transform_to_ast(tree)
        self.interpreter.interpret(ast)
    
    def _capture_output(self, code):
        """Helper para capturar saída de print."""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        try:
            self._run_code(code)
            return captured_output.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    
    def test_variable_declaration_and_access(self):
        """Testa declaração e acesso a variáveis."""
        output = self._capture_output("""
        var x = 42;
        print x;
        """)
        self.assertEqual(output, "42")
    
    def test_arithmetic_operations(self):
        """Testa operações aritméticas."""
        output = self._capture_output("""
        print 2 + 3;
        print 10 - 4;
        print 3 * 7;
        print 15 / 3;
        print 17 % 5;
        """)
        expected = "5\n6\n21\n5\n2"
        self.assertEqual(output, expected)
    
    def test_string_operations(self):
        """Testa operações com strings."""
        output = self._capture_output("""
        var greeting = "Hello";
        var name = "World";
        print greeting + ", " + name + "!";
        """)
        self.assertEqual(output, "Hello, World!")
    
    def test_boolean_operations(self):
        """Testa operações booleanas."""
        output = self._capture_output("""
        print true and false;
        print true or false;
        print !true;
        print !false;
        """)
        expected = "false\ntrue\nfalse\ntrue"
        self.assertEqual(output, expected)
    
    def test_comparison_operations(self):
        """Testa operações de comparação."""
        output = self._capture_output("""
        print 5 > 3;
        print 2 < 1;
        print 4 >= 4;
        print 3 <= 2;
        print 5 == 5;
        print 3 != 4;
        """)
        expected = "true\nfalse\ntrue\nfalse\ntrue\ntrue"
        self.assertEqual(output, expected)
    
    def test_if_statement(self):
        """Testa statement if."""
        output = self._capture_output("""
        var x = 10;
        if (x > 5) {
            print "greater";
        } else {
            print "not greater";
        }
        """)
        self.assertEqual(output, "greater")
    
    def test_while_loop(self):
        """Testa loop while."""
        output = self._capture_output("""
        var i = 0;
        while (i < 3) {
            print i;
            i = i + 1;
        }
        """)
        expected = "0\n1\n2"
        self.assertEqual(output, expected)
    
    def test_function_declaration_and_call(self):
        """Testa declaração e chamada de função."""
        output = self._capture_output("""
        fun greet(name) {
            print "Hello, " + name + "!";
        }
        greet("Alice");
        greet("Bob");
        """)
        expected = "Hello, Alice!\nHello, Bob!"
        self.assertEqual(output, expected)
    
    def test_function_with_return(self):
        """Testa função com retorno."""
        output = self._capture_output("""
        fun add(a, b) {
            return a + b;
        }
        var result = add(3, 4);
        print result;
        """)
        self.assertEqual(output, "7")
    
    def test_recursive_function(self):
        """Testa função recursiva (fibonacci)."""
        output = self._capture_output("""
        fun fib(n) {
            if (n <= 1) {
                return n;
            }
            return fib(n - 1) + fib(n - 2);
        }
        print fib(5);
        """)
        self.assertEqual(output, "5")
    
    def test_scope(self):
        """Testa escopo de variáveis."""
        output = self._capture_output("""
        var global = "global";
        {
            var local = "local";
            print global;
            print local;
        }
        print global;
        """)
        expected = "global\nlocal\nglobal"
        self.assertEqual(output, expected)
    
    def test_division_by_zero(self):
        """Testa erro de divisão por zero."""
        with self.assertRaises(SimpleLangRuntimeError):
            self._run_code("print 5 / 0;")
    
    def test_undefined_variable(self):
        """Testa erro de variável não definida."""
        with self.assertRaises(SimpleLangError):
            self._run_code("print undefined_var;")


class TestSimpleLangExamples(unittest.TestCase):
    """Testes com exemplos mais complexos."""
    
    def setUp(self):
        self.parser = Parser()
        self.interpreter = Interpreter()
    
    def _capture_output(self, code):
        """Helper para capturar saída de print."""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        try:
            tree = self.parser.parse(code)
            ast = transform_to_ast(tree)
            self.interpreter.interpret(ast)
            return captured_output.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    
    def test_factorial(self):
        """Testa cálculo de fatorial."""
        code = """
        fun factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }
        print factorial(5);
        """
        output = self._capture_output(code)
        self.assertEqual(output, "120")
    
    def test_fibonacci_sequence(self):
        """Testa sequência de Fibonacci."""
        code = """
        fun fib(n) {
            if (n <= 1) {
                return n;
            }
            return fib(n - 1) + fib(n - 2);
        }
        
        var i = 0;
        while (i <= 6) {
            print fib(i);
            i = i + 1;
        }
        """
        output = self._capture_output(code)
        expected = "0\n1\n1\n2\n3\n5\n8"
        self.assertEqual(output, expected)


def run_tests():
    """Executa todos os testes."""
    unittest.main(module=__name__, verbosity=2)


if __name__ == "__main__":
    run_tests()




class TestSimpleLangAST(unittest.TestCase):
    """Testes para a construção da AST."""

    def setUp(self):
        self.parser = Parser()

    def _get_ast(self, code):
        tree = self.parser.parse(code)
        return transform_to_ast(tree)

    def test_binary_expression_ast(self):
        code = "print 1 + 2 * 3;"
        ast = self._get_ast(code)
        # Espera-se uma AST que represente (1 + (2 * 3))
        self.assertIsInstance(ast[0], ExpressionStatement)
        expr = ast[0].expression
        self.assertIsInstance(expr, Binary)
        self.assertEqual(expr.operator.value, "+")
        self.assertIsInstance(expr.left, Literal)
        self.assertEqual(expr.left.value, 1)
        self.assertIsInstance(expr.right, Binary)
        self.assertEqual(expr.right.operator.value, "*")
        self.assertIsInstance(expr.right.left, Literal)
        self.assertEqual(expr.right.left.value, 2)
        self.assertIsInstance(expr.right.right, Literal)
        self.assertEqual(expr.right.right.value, 3)

    def test_unary_expression_ast(self):
        code = "print -10;"
        ast = self._get_ast(code)
        self.assertIsInstance(ast[0], ExpressionStatement)
        expr = ast[0].expression
        self.assertIsInstance(expr, Unary)
        self.assertEqual(expr.operator.value, "-")
        self.assertIsInstance(expr.right, Literal)
        self.assertEqual(expr.right.value, 10)

    def test_assignment_ast(self):
        code = "var x = 10; x = 20;"
        ast = self._get_ast(code)
        self.assertIsInstance(ast[1], ExpressionStatement)
        assign_expr = ast[1].expression
        self.assertIsInstance(assign_expr, Assignment)
        self.assertEqual(assign_expr.name, "x")
        self.assertIsInstance(assign_expr.value, Literal)
        self.assertEqual(assign_expr.value.value, 20)

    def test_if_else_ast(self):
        code = "if (true) { print 1; } else { print 0; }"
        ast = self._get_ast(code)
        self.assertIsInstance(ast[0], IfStatement)
        self.assertIsInstance(ast[0].condition, Literal)
        self.assertEqual(ast[0].condition.value, True)
        self.assertIsInstance(ast[0].then_branch, BlockStatement)
        self.assertIsInstance(ast[0].else_branch, BlockStatement)

    def test_while_ast(self):
        code = "while (true) { print 1; }"
        ast = self._get_ast(code)
        self.assertIsInstance(ast[0], WhileStatement)
        self.assertIsInstance(ast[0].condition, Literal)
        self.assertEqual(ast[0].condition.value, True)
        self.assertIsInstance(ast[0].body, BlockStatement)

    def test_function_declaration_ast(self):
        code = "fun test(a, b) { return a + b; }"
        ast = self._get_ast(code)
        self.assertIsInstance(ast[0], FunctionDeclaration)
        self.assertEqual(ast[0].name, "test")
        self.assertEqual(ast[0].parameters, ["a", "b"])
        self.assertIsInstance(ast[0].body, BlockStatement)

    def test_call_ast(self):
        code = "test(1, 2);"
        ast = self._get_ast(code)
        self.assertIsInstance(ast[0], ExpressionStatement)
        call_expr = ast[0].expression
        self.assertIsInstance(call_expr, Call)
        self.assertIsInstance(call_expr.callee, Variable)
        self.assertEqual(call_expr.callee.name, "test")
        self.assertEqual(len(call_expr.arguments), 2)
        self.assertIsInstance(call_expr.arguments[0], Literal)
        self.assertEqual(call_expr.arguments[0].value, 1)
        self.assertIsInstance(call_expr.arguments[1], Literal)
        self.assertEqual(call_expr.arguments[1].value, 2)


class TestSimpleLangErrors(unittest.TestCase):
    """Testes para o tratamento de erros."""

    def setUp(self):
        self.parser = Parser()
        self.interpreter = Interpreter()

    def _run_code_expect_error(self, code, error_type):
        with self.assertRaises(error_type):
            tree = self.parser.parse(code)
            ast = transform_to_ast(tree)
            self.interpreter.interpret(ast)

    def test_undefined_variable_error(self):
        code = "print undefined_var;"
        self._run_code_expect_error(code, SimpleLangRuntimeError)

    def test_division_by_zero_error(self):
        code = "print 10 / 0;"
        self._run_code_expect_error(code, SimpleLangDivisionByZeroError)

    def test_type_error_arithmetic(self):
        code = "print 10 + \"hello\";"
        self._run_code_expect_error(code, SimpleLangTypeError)

    def test_type_error_unary(self):
        code = "print -\"hello\";"
        self._run_code_expect_error(code, SimpleLangTypeError)

    def test_arity_error(self):
        code = "fun test(a) { print a; } test(1, 2);"
        self._run_code_expect_error(code, SimpleLangRuntimeError)

    def test_syntax_error_missing_semicolon(self):
        code = "print 10"
        with self.assertRaises(SimpleLangSyntaxError):
            self.parser.parse(code)

    def test_syntax_error_invalid_token(self):
        code = "var x = #;"
        with self.assertRaises(SimpleLangSyntaxError):
            self.parser.parse(code)


if __name__ == "__main__":
    unittest.main(verbosity=2)





class TestSimpleLangEdgeCases(unittest.TestCase):
    """Testes para casos extremos e comportamentos inesperados."""

    def setUp(self):
        self.parser = Parser()
        self.interpreter = Interpreter()

    def _capture_output(self, code):
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        try:
            tree = self.parser.parse(code)
            ast = transform_to_ast(tree)
            self.interpreter.interpret(ast)
            return captured_output.getvalue().strip()
        finally:
            sys.stdout = old_stdout

    def _run_code_expect_error(self, code, error_type):
        with self.assertRaises(error_type):
            tree = self.parser.parse(code)
            ast = transform_to_ast(tree)
            self.interpreter.interpret(ast)

    def test_empty_program(self):
        """Testa um programa vazio."""
        code = ""
        output = self._capture_output(code)
        self.assertEqual(output, "")

    def test_only_comments(self):
        """Testa um programa contendo apenas comentários."""
        code = "// Este é um comentário\n/* Este é outro comentário */\n"
        output = self._capture_output(code)
        self.assertEqual(output, "")

    def test_nested_blocks(self):
        """Testa blocos aninhados."""
        code = """
        var x = 1;
        {
            var x = 2;
            {
                var x = 3;
                print x;
            }
            print x;
        }
        print x;
        """
        output = self._capture_output(code)
        self.assertEqual(output, "3\n2\n1")

    def test_function_no_return(self):
        """Testa função sem statement de retorno explícito."""
        code = """
        fun do_nothing() {
            var x = 10;
        }
        print do_nothing();
        """
        output = self._capture_output(code)
        self.assertEqual(output, "nil")

    def test_variable_reassignment(self):
        """Testa reatribuição de variável."""
        code = """
        var x = 10;
        print x;
        x = 20;
        print x;
        """
        output = self._capture_output(code)
        self.assertEqual(output, "10\n20")

    def test_string_concatenation_with_numbers(self):
        """Testa concatenação de string com números."""
        code = "print \"The answer is: \" + 42;"
        output = self._capture_output(code)
        self.assertEqual(output, "The answer is: 42")

    def test_for_loop_no_init_condition_increment(self):
        """Testa for loop sem inicialização, condição ou incremento."""
        code = """
        var i = 0;
        for (; i < 2; ) {
            print i;
            i = i + 1;
        }
        """
        output = self._capture_output(code)
        self.assertEqual(output, "0\n1")

    def test_for_loop_infinite(self):
        """
        Testa for loop infinito (deve ser interrompido por timeout ou Ctrl+C).
        Este teste não pode ser executado diretamente em unittest sem um mecanismo de timeout.
        Será um teste manual ou via integração com timeout.
        """
        # code = "for (;;) { print \"loop\"; }"
        # self._run_code_expect_error(code, TimeoutError) # Exemplo, TimeoutError não é padrão
        pass

    def test_unary_minus_on_zero(self):
        """Testa operador unário de menos em zero."""
        code = "print -0;"
        output = self._capture_output(code)
        self.assertEqual(output, "0")

    def test_unary_not_on_numbers(self):
        """Testa operador unário de negação em números."""
        code = """
        print !0;
        print !1;
        print !100;
        """
        output = self._capture_output(code)
        self.assertEqual(output, "true\nfalse\nfalse")

    def test_nested_function_calls(self):
        """Testa chamadas de função aninhadas."""
        code = """
        fun add(a, b) { return a + b; }
        fun mult(a, b) { return a * b; }
        print add(mult(2, 3), add(4, 5)); // (2*3) + (4+5) = 6 + 9 = 15
        """
        output = self._capture_output(code)
        self.assertEqual(output, "15")

    def test_logical_operators_short_circuit(self):
        """Testa short-circuiting em operadores lógicos."""
        code = """
        var x = 0;
        fun side_effect() {
            x = x + 1;
            return true;
        }
        print false and side_effect(); // side_effect não deve ser chamado
        print x;
        print true or side_effect(); // side_effect não deve ser chamado
        print x;
        """
        output = self._capture_output(code)
        self.assertEqual(output, "false\n0\ntrue\n0")


if __name__ == "__main__":
    unittest.main(verbosity=2)


