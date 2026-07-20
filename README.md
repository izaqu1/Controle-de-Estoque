# Sistema de Controle de Estoque

## Descrição

O Sistema de Controle de Estoque é uma aplicação desenvolvida em Python para gerenciar produtos de forma simples e eficiente. O sistema permite cadastrar produtos, controlar entradas e saídas de estoque, atualizar informações, excluir produtos e gerar relatórios de inventário e movimentações.

Os dados são armazenados em um banco de dados SQLite, garantindo persistência das informações mesmo após o encerramento do programa.

---

## Funcionalidades

- Cadastro de produtos
- Atualização de produtos
- Exclusão de produtos com confirmação
- Entrada de estoque
- Saída de estoque
- Consulta de produtos por categoria
- Relatório completo do inventário
- Relatório de movimentações de estoque
- Registro automático das entradas e saídas
- Validação para impedir retirada maior que o estoque disponível
- Interface interativa utilizando Questionary
- Exibição de tabelas utilizando Rich

---

## Tecnologias Utilizadas

- Python 3
- SQLite3
- Questionary
- Rich

---

## Estrutura do Projeto

```
SistemaEstoque/
│
├── Main.py          # Arquivo principal
├── banco.py         # Operações do banco de dados
├── ajuda.py         # Funções auxiliares e interface
├── banco.db       # Banco de dados SQLite
└── README.md
```

---

# Banco de Dados

O sistema utiliza duas tabelas:

# Produtos

| Campo | Tipo |
|--------|------|
| id | INTEGER |
| nome | TEXT |
| categoria | TEXT |
| quantidade | INTEGER |
| quantidade_minima | INTEGER |

# Movimentações

| Campo | Tipo |
|--------|------|
| id | INTEGER |
| id_produto | INTEGER |
| tipo | TEXT |
| quantidade | INTEGER |
| data | DATETIME |

---

## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/Controle-de-Estoque
```

### 2. Acesse a pasta

```bash
cd SEU-REPOSITORIO
```

### 3. Instale as dependências

```bash
pip install (questionary e rich)
```
### 4. Execute o programa

```bash
python Main.py
```

---

## Menu do Sistema

O sistema possui as seguintes opções:

- Cadastrar Produto
- Entrada de Estoque
- Saída de Estoque
- Consultar Categoria
- Atualizar Produto
- Relatório de Inventário
- Relatório de Movimentações
- Excluir Produto
- Sair

---

## Validações Implementadas

- Não permite cadastrar produto sem nome.
- Não permite categoria vazia ou iniciada por número.
- Quantidade aceita apenas números inteiros.
- Não permite retirar mais itens do que existem em estoque.
- Confirmação antes de atualizar um produto.
- Confirmação antes de excluir um produto.
- Possibilidade de cancelar operações.

---

## Bibliotecas Utilizadas

### SQLite3
Responsável pelo armazenamento dos dados do sistema.

### Questionary
Utilizada para criar menus interativos no terminal.

### Rich

Responsável pela exibição de tabelas e melhor formatação da interface no terminal.

---

## Desenvolvido por

**Izaque**

Projeto desenvolvido para a disciplina de Arquitetura de Sistemas Ciberfísicos e Modelagem.
