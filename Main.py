import questionary

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
    cadastrar_produto()

elif opcao == "Consultar Produto":
    consultar_produto()

elif opcao == "Adicionar Estoque":
    adicionar_estoque()

elif opcao == "Retirar Estoque":
    retirar_estoque()

elif opcao == "Listar Produtos":
    listar_produtos()

elif opcao == "Excluir Produto":
    excluir_produto()