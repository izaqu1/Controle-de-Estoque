import questionary
from rich.console import Console
from rich.table import Table

console = Console()

def ler_nome():

    while True:

        nome = input("Nome do produto: ").strip()

        if nome == "":

            resposta = questionary.select(
                "Deseja cancelar o cadastro?",
                choices=["Sim", "Não"]
            ).ask()

            if resposta == "Sim":
                print("Cadastro cancelado.")
                return None

            continue

        return nome
    
def ler_categoria():

    while True:

        categoria = input("Categoria: ").strip()

        if categoria and not categoria[0].isdigit():
            return categoria

        print("A categoria não pode ficar vazia nem começar com número.")

def ler_quantidade():

    while True:

        quantidade = input("Quantidade: ")

        if quantidade.isdigit():
            return int(quantidade)

        print("Digite apenas números.")

def ler_quantidade_minima():

    while True:

        quantidade = input("Quantidade mínima: ")

        if quantidade.isdigit():
            return int(quantidade)

        print("Digite apenas números inteiros.")

def atualizar_nome(nome_atual):

    while True:

        nome = input(f"Novo nome (atual: {nome_atual}): ")

        if nome == "":
            return nome_atual

        nome = nome.strip()

        if nome:
            return nome

        print("O nome não pode ficar vazio.")

def atualizar_categoria(categoria_atual):

    while True:

        categoria = input(f"Nova categoria (atual: {categoria_atual}): ")

        if categoria == "":
            return categoria_atual

        categoria = categoria.strip()

        if categoria and not categoria[0].isdigit():
            return categoria

        print("A categoria não pode ficar vazia nem começar com número.")

def atualizar_quantidade(valor_atual):

    while True:

        quantidade = input(f"Nova quantidade (atual: {valor_atual}): ")

        if quantidade == "":
            return valor_atual

        if quantidade.isdigit():
            return int(quantidade)

        print("Digite apenas números.")

def atualizar_quantidade_minima(valor_atual):

    while True:

        quantidade = input(f"Nova quantidade mínima (atual: {valor_atual}): ")

        if quantidade == "":
            return valor_atual

        if quantidade.isdigit():
            return int(quantidade)

        print("Digite apenas números inteiros.")

from rich.table import Table

def mostrar_produtos(produtos):
    tabela = Table(title="Produtos")

    tabela.add_column("ID")
    tabela.add_column("Nome")
    tabela.add_column("Categoria")
    tabela.add_column("Quantidade")
    tabela.add_column("Qtd. Mínima")

    for p in produtos:
        tabela.add_row(
            str(p[0]),
            p[1],
            p[2],
            str(p[3]),
            str(p[4])
        )

    console.print(tabela)

def mostrar_movimentacoes(movimentacoes):
    tabela = Table(title="Movimentações")

    tabela.add_column("ID")
    tabela.add_column("Produto")
    tabela.add_column("Tipo")
    tabela.add_column("Quantidade")
    tabela.add_column("Data")

    for m in movimentacoes:
        tabela.add_row(
            str(m[0]),
            m[1],
            m[2],
            str(m[3]),
            m[4]
        )

    console.print(tabela)