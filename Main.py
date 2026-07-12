import banco
import questionary

banco.criar_tabela()

while True:

    opcao = questionary.select(
        "===== SISTEMA DE CONTROLE DE ESTOQUE =====",
        choices=[
            "Cadastrar Produto",
            "Consultar Produto",
            "Adicionar Estoque",
            
            "Retirar Estoque",
            "Listar Produtos",
            "Excluir Produto",
            "Sair"
        ]
    ).ask()

    if opcao == "Cadastrar Produto":
        nome = input("Nome: ")
        quantidade = int(input("Quantidade: "))
        estoque_minimo = int(input("Estoque Mínimo: "))

        banco.cadastrar(nome, quantidade, estoque_minimo)
        print("Produto cadastrado!")

    elif opcao == "Consultar Produto":

        tipo = questionary.select(
        "Consultar por:",
        choices=["ID", "Nome"]
        ).ask()

        if tipo == "ID":
            id_produto = int(input("Digite o ID: "))

            produto = banco.consultar_id(id_produto)

            if produto:
                print("-----------------------")
                print("ID:", produto[0])
                print("Nome:", produto[1])
                print("Quantidade:", produto[2])
                print("Estoque Mínimo:", produto[3])
            else:
                print("Produto não encontrado!")

        elif tipo == "Nome":
            nome = input("Digite o nome do produto: ")

            produtos = banco.consultar_nome(nome)

            if produtos:
                for p in produtos:
                    print("-----------------------")
                    print("ID:", p[0])
                    print("Nome:", p[1])
                    print("Quantidade:", p[2])
                    print("Estoque Mínimo:", p[3])
            else:
                print("Nenhum produto encontrado.")

    elif opcao == "Adicionar Estoque":
        print("Função ainda não implementada.")

    elif opcao == "Retirar Estoque":
        print("Função ainda não implementada.")

    elif opcao == "Listar Produtos":
        produtos = banco.listar()

        for p in produtos:
            print("-----------------------")
            print("ID:", p[0])
            print("Nome:", p[1])
            print("Quantidade:", p[2])
            print("Estoque Mínimo:", p[3])

    elif opcao == "Excluir Produto":
        print("Função ainda não implementada.")

    elif opcao == "Sair":
        print("Saindo do sistema...")
        break