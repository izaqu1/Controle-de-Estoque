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

        consultar_por = questionary.select(
        "Consultar por:",
        choices=["ID", "Nome"]
        ).ask()

        if consultar_por == "ID":
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

        elif consultar_por == "Nome":
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
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        excluir = questionary.select(
        "Selecione o produto a ser excluído:",
            choices=[
                questionary.Choice(
                    title=f"ID: {p[0]} - Nome: {p[1]} - Quantidade: {p[2]} - Estoque Mínimo: {p[3]}",
                        
                    value=p[0]
            )
            for p in produtos
            ]
        ).ask()

        if excluir:
            confirmar = questionary.select(
                "Tem certeza que deseja excluir este produto?",
            choices=["Sim", "Não"]
            ).ask()

            if confirmar == "Sim":
                banco.excluir(excluir)
                print(" Produto excluído com sucesso!")
            else:
                print(" Exclusão cancelada.")

    elif opcao == "Sair":
        print("Saindo do sistema...")
        break