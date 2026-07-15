import banco
import questionary

banco.criar_tabela()

while True:

    opcao = questionary.select(
        "===== SISTEMA DE CONTROLE DE ESTOQUE =====",
        choices=[
            "Cadastrar Produto",
            "Consultar Categoria",
            "Atualizar Produto",
            "Listar Produtos",
            "Excluir Produto",
            "Sair"
        ]
    ).ask()

 #--------------------------------------------------------------------------
    if opcao == "Cadastrar Produto":
        cancelou = False

        while True:
            nome = input("Nome do produto: ").strip()

            if nome == "":
                resposta = questionary.select(
                     "Deseja cancelar o cadastro?",
                     choices=["Sim", "Não"]
                ).ask()

                if resposta == "Sim":
                    print("Cadastro cancelado.")
                    cancelou = True
                    break
                else:
                    continue

                break

        if cancelou:
            continue

        while True:
            categoria = input("Categoria: ").strip()

            if categoria:
                break
            else:
                print("Erro: não é permitido deixar campos em branco. Digite novamente.")
        while True:
            quantidade = input("Quantidade: ")

            if quantidade.isdigit():
                quantidade = int(quantidade)
                break
            else:
                print("Erro: não é permitido utilizar letras ou caracteres especiais. Digite apenas números inteiros.")

        while True:
            quantidade_minima = input("quantidade Mínima: ")

            if quantidade_minima.isdigit():
                quantidade_minima = int(quantidade_minima)
                break
            else:
                print("Erro: não é permitido utilizar letras ou caracteres especiais. Digite apenas números inteiros.")

        banco.cadastrar(nome, categoria, quantidade, quantidade_minima)
        print("Produto cadastrado!")
 
 #--------------------------------------------------------------------------
    elif opcao == "Consultar Categoria":

        categorias = banco.listar_categorias()

        if not categorias:
            print("Nenhuma categoria cadastrada.")
            continue

        categoria = questionary.select(
            "Selecione uma categoria:",
            choices=[c[0] for c in categorias]
        ).ask()

        produtos = banco.consultar_categoria(categoria)

        print(f"\nCategoria: {categoria}")

        for p in produtos:
            print(f"ID: {p[0]} - Nome: {p[1]} - Quantidade: {p[3]} - Quantidade Mínima: {p[4]}")

#--------------------------------------------------------------------------
    elif opcao == "Atualizar Produto":
        atualizar_produto = questionary.select(
            "Selecione o produto a ser atualizado:",
            choices=[
                questionary.Choice(
                    title=f"ID: {p[0]} - Nome: {p[1]} - Categoria: {p[2]} - Quantidade: {p[3]} - Quantidade Mínima: {p[4]}",
                    value=p[0]
                )
                for p in banco.listar()
            ]
        ).ask()

        if atualizar_produto:
            produto = banco.consultar_id(atualizar_produto)

            if produto:
                print("Produto selecionado:")
                print("-----------------------")
                print("ID:", produto[0])
                print("Nome:", produto[1])
                print("Categoria:", produto[2])
                print("Quantidade:", produto[3])
                print("Quantidade Mínima:", produto[4])

                nome = input(f"Novo nome (atual: {produto[1]}): ") or produto[1]
            while True:
                categoria = input(f"Nova categoria (atual: {produto[2]}): ") or produto[2]
                if categoria and not categoria[0].isdigit():
                    break
                else:
                    print("A categoria do produto não pode ser vazio nem começar com um numero. Por favor, insira uma categoria válida.")

            while True:
                quantidade = input(f"Nova quantidade (atual: {produto[3]}): ")
                if quantidade:
                    try:
                        quantidade = int(quantidade)
                        break
                    except ValueError:
                        print("A quantidade do produto deve ser um número inteiro. Por favor, insira um valor válido.")
                else:
                    quantidade = produto[3]
                    break
            while True:
                quantidade_minima = input(f"Nova quantidade mínima (atual: {produto[4]}): ")

                if quantidade_minima == "":
                    quantidade_minima = produto[4]
                    break

                elif quantidade_minima.isdigit():
                    quantidade_minima = int(quantidade_minima)
                    break

                else:
                    print("Digite apenas números.")

            banco.atualizar(atualizar_produto, nome, categoria, quantidade, quantidade_minima)
            print("Produto atualizado com sucesso!")
        else:
            print("Produto não encontrado.")

#--------------------------------------------------------------------------
    elif opcao == "Listar Produtos":
        produtos = banco.listar()

        for p in produtos:
           print(f"ID: {p[0]} - Nome: {p[1]} - Categoria: {p[2]} - Quantidade: {p[3]} - Quantidade Mínima: {p[4]}")

#--------------------------------------------------------------------------
    elif opcao == "Excluir Produto":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        excluir = questionary.select(
        "Selecione o produto a ser excluído:",
            choices=[
                questionary.Choice(
                    title=f"ID: {p[0]} - Nome: {p[1]} - Categoria: {p[2]} - Quantidade: {p[3]} - Quantidade Mínima: {p[4]}",
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


#--------------------------------------------------------------------------
    elif opcao == "Sair":
        print("Saindo do sistema...")
        break