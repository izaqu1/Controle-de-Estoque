# ELETRO VERA CRUZ — Sistema de Controle de Estoque e Vendas

Sistema desktop desenvolvido em **Python**, com interface gráfica, para auxiliar no controle de produtos, movimentações de estoque, vendas e operações de caixa da loja Eletro Vera Cruz.

A aplicação foi desenvolvida como uma alternativa local de contingência, permitindo registrar e consultar informações essenciais quando o sistema principal da loja estiver indisponível.

## Funcionalidades

### 1. Gestão de produtos
- Cadastro de produtos com código, nome, categoria, marca, quantidade, quantidade mínima e preço.
- Consulta dos produtos cadastrados.
- Edição das informações dos produtos.
- Inativação de produtos, preservando o histórico de movimentações e vendas.
- Validação de dados e identificação de códigos duplicados.

### 2. Controle de estoque
- Registro de entradas e saídas de produtos.
- Atualização automática das quantidades em estoque.
- Registro das movimentações realizadas.
- Validação para impedir saídas superiores à quantidade disponível.
- Consulta do histórico de movimentações.

### 3. Registro de vendas
- Seleção de produtos cadastrados.
- Inclusão de itens avulsos em uma venda.
- Definição da quantidade de cada item.
- Cálculo automático dos subtotais e do valor total.
- Seleção da forma de pagamento: PIX, crédito, débito, dinheiro ou carteira.
- Atualização do estoque após a conclusão da venda.
- Armazenamento do histórico de vendas.

### 4. Controle de caixa
- Abertura de caixa com valor inicial e identificação do responsável.
- Consulta da situação atual do caixa.
- Cálculo do valor esperado em dinheiro.
- Fechamento de caixa com registro do valor contado e da diferença.
- Separação das vendas em dinheiro das demais formas de pagamento.

### 5. Relatórios
- Consulta de informações sobre vendas e movimentações.
- Geração de relatórios em PDF e Excel.
- Apoio à conferência das operações realizadas.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python 3 | Linguagem de programação |
| Tkinter | Construção da interface gráfica |
| SQLite3 | Armazenamento local dos dados |
| OpenPyXL | Geração de planilhas Excel |
| ReportLab | Geração de documentos PDF |

## Estrutura do projeto

```text
Controle-de-Estoque/
│
├── Main.py
├── interface.py
├── banco.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Descrição dos arquivos:**

- `Main.py`: arquivo principal responsável por iniciar a aplicação.
- `interface.py`: contém a interface gráfica e os recursos de interação com o usuário.
- `banco.py`: concentra as operações de banco de dados, incluindo cadastro, consultas, vendas, estoque e caixa.
- `requirements.txt`: lista as bibliotecas externas necessárias para o funcionamento do projeto.
- `.gitignore`: define arquivos que não devem ser enviados ao repositório.

O banco de dados SQLite (`banco.db`) é criado automaticamente na pasta do projeto durante a inicialização do sistema.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/izaqu1/Controle-de-Estoque.git
```

### 2. Acessar a pasta

```bash
cd Controle-de-Estoque
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

O Tkinter normalmente já acompanha a instalação do Python. Caso não esteja disponível, será necessário instalá-lo conforme o sistema operacional utilizado.

### 4. Iniciar a aplicação

```bash
python Main.py
```

## Armazenamento dos dados

O sistema utiliza o SQLite para armazenar localmente os dados de produtos, movimentações, vendas e caixas.

Por ser uma aplicação local, os registros permanecem disponíveis após o encerramento do programa, desde que o arquivo do banco de dados seja preservado.

**Importante:** o sistema funciona de forma independente e não realiza integração automática com o sistema principal da loja.

## Objetivo do projeto

O projeto tem como objetivo oferecer uma ferramenta de apoio à operação da loja em situações de indisponibilidade do sistema principal, permitindo manter registros de estoque, vendas e movimentações financeiras por meio de uma aplicação desktop.

## Desenvolvedor

**Izaque Alceu Cavalheiro Fernandes**

Projeto desenvolvido em Python.
