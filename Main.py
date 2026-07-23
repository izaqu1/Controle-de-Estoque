import banco
import ajuda
import questionary
banco.criar_tabela()


# Menu principal do sistema (fica repetindo até o usuário escolher "Sair")
 
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

 # # Cadastro de um novo produto--------------------------------------------------------------------------
    if opcao == "Cadastrar Produto":
        nome = ajuda.ler_nome()
        
# Se o usuário cancelar, volta para o menu principal
        if nome is None:
            continue

# Solicita os demais dados do produto
        categoria = ajuda.ler_categoria()
        quantidade = ajuda.ler_quantidade()
        quantidade_minima = ajuda.ler_quantidade_minima()

# Salva o produto no banco de dados
        banco.cadastrar(nome, categoria, quantidade, quantidade_minima)
        print("Produto cadastrado com sucesso!")

 # Entrada de produtos no estoque--------------------------------------------------------------------------
    elif opcao == "Entrada de Estoque":

        # Busca todos os produtos cadastrados
        produtos = banco.listar()

# Verifica se existe algum produto cadastrado
        if not produtos:
            print("Não há produtos cadastrados.")
            continue

# Mostra os produtos em formato de tabela
        ajuda.mostrar_produtos(produtos)

# Cria uma lista de opções para o usuário escolher um produto
        choices = [
            questionary.Choice(
                title=f"ID: {p[0]} | {p[1]} | {p[2]} | {p[3]}",
                value=p[0]
            )
            for p in produtos
        ]

# Adiciona a opção Cancelar
        choices.append(questionary.Choice(
            title="Cancelar",
            value="Cancelar"
        ))

# Usuário escolhe qual produto receberá entrada no estoque
        id_produto = questionary.select(
            "Selecione o produto para entrada de estoque:",
            choices=choices
            ).ask()

# Cancela a operação se o usuário desejar
        if id_produto is "Cancelar":
            print("Entrada de estoque cancelada.")
            continue

# Pergunta a quantidade que será adicionada
        quantidade = ajuda.ler_quantidade()

# Atualiza o estoque no banco de dados
        banco.entrada_estoque(id_produto, quantidade)

        print("Entrada de estoque registrada com sucesso!")

 #Saída de produtos do estoque--------------------------------------------------------------------------
    elif opcao == "Saída de Estoque":
        # Busca todos os produtos
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

# Exibe os produtos
        ajuda.mostrar_produtos(produtos)

# Monta a lista para seleção
        choices = [
            questionary.Choice(
                title=f"ID: {p[0]} | {p[1]} | {p[2]} | {p[3]}",
                value=p[0]
            )
            for p in produtos
        ]

        choices.append(
            questionary.Choice(
                title="Cancelar",
                value='Cancelar'
            )
        )

# Usuário escolhe qual produto será retirado do estoque
        id_produto = questionary.select(
            "Selecione o produto para saída de estoque:",
            choices=choices
        ).ask()

        if id_produto is 'Cancelar':
            print("Saída de estoque cancelada.")
            continue

# Pergunta a quantidade que será retirada
        quantidade = ajuda.ler_quantidade()

# Realiza a saída do estoque
        sucesso = banco.saida_estoque(id_produto, quantidade)

# Verifica se a operação foi realizada com sucesso
        if sucesso:
            print("Saída de estoque registrada com sucesso!")

# Consulta novamente o produto para verificar a quantidade atual
            produto = banco.consultar_id(id_produto)

# Verifica se o estoque chegou ao mínimo
            if produto[3] <= produto[4]:
                print(f"ATENÇÃO! O produto '{produto[1]}' atingiu o estoque mínimo.")

        else:
            print("Erro: Quantidade insuficiente em estoque ou produto não encontrado.")
        
 #Consulta produtos de uma categoria específica--------------------------------------------------------------------------
    elif opcao == "Consultar Categoria":

# Busca todas as categorias cadastradas
        categorias = banco.listar_categorias()

        if not categorias:
            print("Nenhuma categoria cadastrada.")
            continue

# Usuário escolhe uma categoria
        categoria = questionary.select(
            "Selecione uma categoria:",
            choices=[c[0] for c in categorias]
        ).ask()

# Busca apenas os produtos da categoria escolhida
        produtos = banco.consultar_categoria(categoria)

        print(f"\nCategoria: {categoria}")

# Mostra os produtos encontrados
        ajuda.mostrar_produtos(produtos)
        
#Atualiza os dados de um produto--------------------------------------------------------------------------
    elif opcao == "Atualizar Produto":

        # Busca todos os produtos cadastrados
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

# Cria a lista para selecionar qual produto será atualizado
        choices = [
        questionary.Choice(
            title=f"ID: {p[0]} - {p[1]} - {p[2]} - {p[3]} - {p[4]}",
            value=p[0]
        )
        for p in produtos
    ]

        choices.append(questionary.Choice(title="Cancelar", value="Cancelar"))

        atualizar_produto = questionary.select(
            "Selecione o produto a ser atualizado:",
            choices=choices
        ).ask()

        if atualizar_produto is "Cancelar":
            print("Atualização cancelada.")
            continue

# Busca os dados atuais do produto
        produto = banco.consultar_id(atualizar_produto)

        if produto:
            print("Produto selecionado:")
            print("-----------------------")

            # Mostra o produto selecionado
            ajuda.mostrar_produtos([produto])

# Solicita os novos dados
            nome = ajuda.atualizar_nome(produto[1])
            categoria = ajuda.atualizar_categoria(produto[2])
            quantidade = ajuda.atualizar_quantidade(produto[3])
            quantidade_minima = ajuda.atualizar_quantidade_minima(produto[4])

# Confirma se o usuário realmente deseja atualizar
            confirmar = questionary.select(
                "Confirma a atualização deste produto?",
                choices=["Sim", "Não"]
            ).ask()

            if confirmar == "Sim":
                # Atualiza o produto no banco
                banco.atualizar(
                    atualizar_produto,
                    nome,
                    categoria,
                    quantidade,
                    quantidade_minima
                )
                print("Produto atualizado com sucesso!")
            sucesso = banco.saida_estoque(id_produto, quantidade)

            if sucesso:
                print("Saída de estoque registrada com sucesso!")

                produto = banco.consultar_id(id_produto)

                if produto[3] <= produto[4]:
                    print(f"ATENÇÃO! O produto '{produto[1]}' atingiu o estoque mínimo.")
            else:
                print("Atualização cancelada!")

        else:
            print("Produto não encontrado!")

#Exibe todos os produtos cadastrados--------------------------------------------------------------------------
    elif opcao == "Relatório de Inventário":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

#Exibe todas as movimentações de entrada e saída--------------------------------------------------------------------------
    elif opcao == "Relatório de Movimentações":
        movimentacoes = banco.listar_movimentacoes()

        if not movimentacoes:
            print("Não há movimentações registradas.")
            continue

        ajuda.mostrar_movimentacoes(movimentacoes)


#Exclui um produto do sistema--------------------------------------------------------------------------
    elif opcao == "Excluir Produto":
        produtos = banco.listar()

        if not produtos:
            print("Não há produtos cadastrados.")
            continue

        ajuda.mostrar_produtos(produtos)

# Cria a lista de produtos para exclusão
        choices = [
            questionary.Choice(
                title=f"ID: {p[0]} - {p[1]} - {p[2]} - {p[3]} - {p[4]}",
                value=p[0]
            )
            for p in produtos
        ]

        choices.append(questionary.Choice(title="Cancelar", value="Cancelar"))

# Usuário escolhe qual produto deseja excluir
        excluir = questionary.select(
            "Selecione o produto a ser excluído:",
            choices=choices
        ).ask()

        if excluir is "Cancelar":
            print("Exclusão cancelada.")
            continue

# Pede confirmação antes de excluir
        confirmar = questionary.select(
            "Tem certeza que deseja excluir este produto?",
            choices=["Sim", "Não"]
        ).ask()

        if confirmar == "Sim":
            # Remove o produto do banco de dados
            banco.excluir(excluir)
            print("Produto excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
#Encerra o programa--------------------------------------------------------------------------
    elif opcao == "Sair":
        print("Saindo do sistema...")
        break
