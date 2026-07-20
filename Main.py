import banco
import ajuda
import questionary
banco.criar_tabela()

while True:

    opcao = questionary.select(
        "===== SISTEMA DE CONTROLE DE ESTOQUE =====",
        choices=[
            "Cadastrar Produto",
            "Entrada de Estoque",
            "Saída de Estoque",
            "Consultar Categoria",
            "Atualizar Produto",
            "Relatório de Inventário",
            "Relatório de Movimentações",
            "Excluir Produto",
            "Sair"
        ]
    ).ask()

 #--------------------------------------------------------------------------
    if opcao == "Cadastrar Produto":
        nome = ajuda.ler_nome()

        if nome is None:
            continue

        categoria = ajuda.ler_categoria()
        quantidade = ajuda.ler_quantidade()
        quantidade_minima = ajuda.ler_quantidade_minima()

        banco.cadastrar(nome, categoria, quantidade, quantidade_minima)
        print("Produto cadastrado com sucesso!")

 #--------------------------------------------------------------------------
    elif opcao == "Entrada de Estoque":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

        choices = [
            questionary.Choice(
                title=f"ID: {p[0]} | {p[1]} | Categoria: {p[2]} | Estoque: {p[3]}",
                value=p[0]
            )
            for p in produtos
        ]

        choices.append(questionary.Choice(
            title="Cancelar",
            value="entrada-estoque"
        ))

        id_produto = questionary.select(
            "Selecione o produto para entrada de estoque:",
            choices=choices
            ).ask()

        if id_produto is "entrada-estoque":
            print("Entrada de estoque cancelada.")
            continue

        quantidade = ajuda.ler_quantidade()

        banco.entrada_estoque(id_produto, quantidade)

        print("Entrada de estoque registrada com sucesso!")

 #--------------------------------------------------------------------------
    elif opcao == "Saída de Estoque":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

        choices = [
            questionary.Choice(
                title=f"ID: {p[0]} | {p[1]} | Categoria: {p[2]} | Estoque: {p[3]}",
                value=p[0]
            )
            for p in produtos
        ]

        choices.append(
            questionary.Choice(
                title="Cancelar",
                value='saida-estoque'
            )
        )

        id_produto = questionary.select(
            "Selecione o produto para saída de estoque:",
            choices=choices
        ).ask()

        if id_produto is 'saida-estoque':
            print("Saída de estoque cancelada.")
            continue

        quantidade = ajuda.ler_quantidade()

        sucesso = banco.saida_estoque(id_produto, quantidade)

        if sucesso:
            print("Saída de estoque registrada com sucesso!")
        else:
            print("Erro: Quantidade insuficiente em estoque ou produto não encontrado.")
 
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

        ajuda.mostrar_produtos(produtos)
        
#--------------------------------------------------------------------------
    elif opcao == "Atualizar Produto":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        choices = [
        questionary.Choice(
            title=f"ID: {p[0]} - Nome: {p[1]} - Categoria: {p[2]} - Quantidade: {p[3]} - Quantidade Mínima: {p[4]}",
            value=p[0]
        )
        for p in produtos
    ]

        choices.append(questionary.Choice(title="Cancelar", value=None))

        atualizar_produto = questionary.select(
            "Selecione o produto a ser atualizado:",
            choices=choices
        ).ask()

        if atualizar_produto is None:
                print("Atualização cancelada.")
                continue

        produto = banco.consultar_id(atualizar_produto)

        if produto:
            print("Produto selecionado:")
            print("-----------------------")
            ajuda.mostrar_produtos([produto])

            nome = ajuda.atualizar_nome(produto[1])
            categoria = ajuda.atualizar_categoria(produto[2])
            quantidade = ajuda.atualizar_quantidade(produto[3])
            quantidade_minima = ajuda.atualizar_quantidade_minima(produto[4])

            confirmar = questionary.select(
                "Confirma a atualização deste produto?",
                choices=["Sim", "Não"]
            ).ask()

            if confirmar == "Sim":
                banco.atualizar(
                    atualizar_produto,
                    nome,
                    categoria,
                    quantidade,
                    quantidade_minima
                )
                print("Produto atualizado com sucesso!")
            else:
                print("Atualização cancelada.")

        else:
            print("Produto não encontrado.")

#--------------------------------------------------------------------------
    elif opcao == "Relatório de Inventário":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

#--------------------------------------------------------------------------
    elif opcao == "Relatório de Movimentações":
        movimentacoes = banco.listar_movimentacoes()

        if not movimentacoes:
            print("Não há movimentações registradas.")
            continue

        ajuda.mostrar_movimentacoes(movimentacoes)

#--------------------------------------------------------------------------
    elif opcao == "Excluir Produto":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

        choices = [
            questionary.Choice(
                title=f"ID: {p[0]} - Nome: {p[1]} - Categoria: {p[2]} - Quantidade: {p[3]} - Quantidade Mínima: {p[4]}",
                value=p[0]
            )
            for p in produtos
        ]

        choices.append(questionary.Choice(title="Cancelar", value=None))

        excluir = questionary.select(
            "Selecione o produto a ser excluído:",
            choices=choices
        ).ask()

        if excluir is None:
            print("Exclusão cancelada.")
            continue

        confirmar = questionary.select(
            "Tem certeza que deseja excluir este produto?",
            choices=["Sim", "Não"]
        ).ask()

        if confirmar == "Sim":
            banco.excluir(excluir)
            print("Produto excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
#--------------------------------------------------------------------------
    elif opcao == "Sair":
        print("Saindo do sistema...")
        break