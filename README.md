# SimpleLang - Um Interpretador para Linguagem Simples

## Integrantes

- Arthur Henrique Vieira - 231034064
- Gabriel Soares dos Anjos - 2310266625
- Mylena Trindade de Mendonca - 231035769
- Cibelly Lourenco Ferreira - 231026680

## Introdução

Este projeto consiste na implementação de um interpretador para **SimpleLang**, uma linguagem de programação simples, dinamicamente tipada, com sintaxe inspirada em linguagens como Python e JavaScript. O objetivo principal foi desenvolver um compilador/interpretador completo, abordando as principais fases de um processo de compilação: análise léxica, análise sintática, construção da Árvore Sintática Abstrata (AST), análise semântica e execução em tempo de execução (runtime).

SimpleLang foi projetada para ser didática, permitindo a exploração de conceitos fundamentais de linguagens de programação, como declaração de variáveis, estruturas de controle de fluxo (condicionais `if-else`, laços `while` e `for`), definição e chamada de funções (incluindo recursividade), e operações básicas com tipos de dados numéricos, booleanos e strings. A linguagem também incorpora um sistema de tratamento de erros robusto para auxiliar no desenvolvimento e depuração de programas.

## Instalação

Para instalar e rodar o interpretador SimpleLang, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <nome_do_diretorio_do_repositorio>
    ```

2.  **Instale as dependências:**

    O projeto utiliza a biblioteca `lark` para a análise léxica e sintática. Você pode instalá-la usando `pip`:

    ```bash
    pip install lark
    ```

3.  **Executando o Interpretador:**

    Você pode executar um arquivo SimpleLang diretamente ou iniciar o REPL (Read-Eval-Print Loop) da linguagem.

    *   **Executar um arquivo:**

        ```bash
        python -m lox <caminho_do_arquivo.sl>
        ```

        Exemplo:

        ```bash
        python -m lox examples/hello_world.sl
        ```

    *   **Iniciar o REPL:**

        ```bash
        python -m lox
        ```

        No REPL, você pode digitar comandos SimpleLang e ver o resultado imediatamente.

        ```
        >>> var x = 10;
        >>> print x + 5;
        15
        >>> fun greet(name) { print "Hello, " + name + "!"; }
        >>> greet("SimpleLang");
        Hello, SimpleLang!
        ```

## Exemplos

A pasta `examples/` (a ser criada) conterá diversos exemplos de programas escritos em SimpleLang, demonstrando as funcionalidades da linguagem. Abaixo, alguns exemplos notáveis:

### Hello World

```simplelang
print "Hello, World!";
```

### Fibonacci Recursivo

```simplelang
fun fib(n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}
print "Fibonacci(10): " + fib(10);
```

### Fatorial

```simplelang
fun factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
print "Fatorial de 5: " + factorial(5);
```

## Referências

Este projeto foi fortemente inspirado e baseado nos conceitos e na estrutura de compiladores e interpretadores, com particular atenção às seguintes referências:

-   **Crafting Interpreters** por Robert Nystrom [1]: Uma excelente e didática obra que aborda a construção de um interpretador completo do zero, utilizando a linguagem Lox como exemplo. Muitos dos padrões de design (como o padrão Visitor para a AST) e a organização geral do interpretador foram influenciados por este livro.
    -   [1] Nystrom, Robert. *Crafting Interpreters*. Disponível em: [https://craftinginterpreters.com/](https://craftinginterpreters.com/)

-   **Lark - um parser para Python** [2]: A biblioteca Lark foi utilizada para a geração do analisador léxico e sintático (parser) a partir da gramática da SimpleLang. Sua flexibilidade e facilidade de uso foram cruciais para a fase de parsing do projeto.
    -   [2] Lark. *Lark - a parsing library for Python*. Disponível em: [https://lark-parser.readthedocs.io/en/latest/](https://lark-parser.readthedocs.io/en/latest/)

## Estrutura do Código

O projeto está organizado na seguinte estrutura de diretórios e arquivos:

```
. (raiz do repositório)
├── lox/
│   ├── ast.py             # Definição das classes de nós da Árvore Sintática Abstrata (AST).
│   ├── cli.py             # Interface de linha de comando (CLI) para o interpretador.
│   ├── ctx.py             # Gerenciamento de contexto e escopo (variáveis, funções).
│   ├── errors.py          # Definição de classes de exceção para erros da SimpleLang.
│   ├── grammar.lark       # Gramática da SimpleLang definida em formato Lark.
│   ├── __init__.py        # Inicialização do pacote Python.
│   ├── __main__.py        # Ponto de entrada para execução via `python -m lox`.
│   ├── node.py            # Classes base para os nós da AST (Expressões e Statements).
│   ├── parser.py          # Analisador léxico e sintático, utiliza Lark para parsing.
│   ├── runtime.py         # Interpretador principal, percorre a AST e executa o código.
│   ├── testing.py         # Módulo de testes unitários para o interpretador.
│   └── transformer.py     # Converte a árvore de parsing do Lark em AST.
├── pyproject.toml         # Configurações do projeto Python (dependências, etc.).
├── pytest.ini             # Configurações para o Pytest (framework de testes).
├── README.md              # Este arquivo.
└── tests/                 # Diretório para testes adicionais (não implementado neste escopo).
```

### Etapas de Compilação e Onde São Realizadas

1.  **Análise Léxica e Sintática:** Realizada pelo módulo `parser.py`, que utiliza a gramática definida em `grammar.lark` e a biblioteca `lark`. O `parser.py` transforma o código fonte em uma árvore de parsing.
2.  **Construção da Árvore Sintática Abstrata (AST):** O módulo `transformer.py` atua como um transformador da árvore de parsing gerada pelo Lark, convertendo-a em uma estrutura de AST mais limpa e hierárquica, utilizando as classes de nós definidas em `node.py`.
3.  **Análise Semântica e Gerenciamento de Contexto:** O módulo `ctx.py` é responsável por gerenciar os ambientes (escopos) de variáveis e funções. Durante a execução (`runtime.py`), a resolução de nomes e a verificação de tipos (implícita, devido à tipagem dinâmica) são realizadas com base no contexto atual. Erros semânticos, como variáveis não declaradas ou aridade incorreta de funções, são detectados e reportados via `errors.py`.
4.  **Execução (Interpretação):** O `runtime.py` é o coração do interpretador. Ele percorre a AST (utilizando o padrão Visitor) e executa as operações correspondentes a cada nó. Isso inclui avaliação de expressões, execução de statements de controle de fluxo e chamadas de função.

## Bugs/Limitações/Problemas Conhecidos

-   **Tratamento de Erros de Runtime:** Embora exista um módulo `errors.py` para tratamento de erros, a granularidade das mensagens de erro de runtime pode ser melhorada para incluir informações mais precisas sobre a linha e coluna do erro em todos os casos.
-   **Otimização:** O interpretador atual não realiza otimizações de código. Para programas muito grandes ou complexos, o desempenho pode ser um fator limitante. Uma futura melhoria poderia incluir uma fase de otimização da AST ou a geração de bytecode.
-   **Tipagem:** SimpleLang é dinamicamente tipada. A adição de um sistema de tipos estático ou inferência de tipos poderia melhorar a detecção de erros em tempo de compilação e a robustez do código.
-   **Recursos da Linguagem:** A linguagem é intencionalmente simples. Recursos mais avançados, como classes, objetos, módulos, tratamento de exceções (além do `return`), e estruturas de dados mais complexas (listas, dicionários nativos), não estão implementados. A extensão da gramática e do interpretador para suportar esses recursos seria uma evolução natural.
-   **REPL:** O REPL atual tem uma limitação na forma como lida com expressões que não são statements completos. Embora tente inferir, pode haver casos onde a entrada não é interpretada corretamente sem um `;` final ou se for uma expressão complexa que não se encaixa nas regras de statement.
-   **Testes:** Embora exista um módulo `testing.py` com testes unitários básicos, a cobertura de testes pode ser expandida significativamente para garantir a robustez de todas as funcionalidades e cenários de erro.


