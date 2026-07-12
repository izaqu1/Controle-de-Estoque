import banco
banco.criar_tabela()
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
    cadastrar_produto(
        nome = input("Nome: "),
        quantidade = int(input("Quantidade: ")),
        estoque_minimo = int(input("Estoque Mínimo: ")) 
    )
    banco.cadastrar(nome, quantidade, estoque_minimo)
    print("Produto cadastrado!")

elif opcao == "Consultar Produto":
    consultar_produto(
        produtos = banco.listar()
    )
    for p in produtos:
        print("-----------------------")
        print("ID:", p[0])
        print("Nome:", p[1])
        print("Quantidade:", p[2])
        print("Estoque Mínimo:", p[3])

elif opcao == "Adicionar Estoque":
    adicionar_estoque()

elif opcao == "Retirar Estoque":
    retirar_estoque()

elif opcao == "Listar Produtos":
    listar_produtos()

elif opcao == "Excluir Produto":
    excluir_produto()
    
elif opcao == "Sair":
    print("Saindo do sistema...")
    break