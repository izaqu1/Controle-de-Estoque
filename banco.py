import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        quantidade_minima INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produto INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(id_produto) REFERENCES produtos(id)
)
""")

    conexao.commit()
    conexao.close()

def cadastrar(nome, categoria, quantidade, quantidade_minima):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO produtos(nome, categoria, quantidade, quantidade_minima) VALUES(?,?,?,?)",
        (nome, categoria, quantidade, quantidade_minima)
    )

    conexao.commit()
    conexao.close()

def listar():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos")

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def consultar_id(id_produto):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id_produto,)
    )

    produto = cursor.fetchone()

    conexao.close()

    return produto

def consultar_nome(nome):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE LOWER(nome) = LOWER(?)",
        (nome,)
    )

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def excluir(id_produto):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id_produto,)
    )

    conexao.commit()
    conexao.close()

def listar_categorias():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT categoria
        FROM produtos
        ORDER BY categoria
    """)

    categorias = cursor.fetchall()

    conexao.close()

    return categorias

def consultar_categoria(categoria):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE LOWER(categoria) = LOWER(?)",
        (categoria,)
    )

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def atualizar(id_produto, nome, categoria, quantidade, quantidade_minima):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE produtos SET nome = ?, categoria = ?, quantidade = ?, quantidade_minima = ? WHERE id = ?",
        (nome, categoria, quantidade, quantidade_minima, id_produto)
    )

    conexao.commit()
    conexao.close()

def registrar_movimentacao(id_produto, tipo, quantidade):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO movimentacoes(id_produto, tipo, quantidade) VALUES(?,?,?)",
        (id_produto, tipo, quantidade)
    )

    conexao.commit()
    conexao.close()

def listar_movimentacoes():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            m.id,
            p.nome,
            m.tipo,
            m.quantidade,
            m.data
        FROM movimentacoes m
        JOIN produtos p
            ON p.id = m.id_produto
        ORDER BY m.data DESC
    """)

    movimentacoes = cursor.fetchall()

    conexao.close()

    return movimentacoes

def entrada_estoque(id_produto, quantidade):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade + ?
        WHERE id = ?
    """, (quantidade, id_produto))

    conexao.commit()
    conexao.close()

    registrar_movimentacao(id_produto, "Entrada", quantidade)

def saida_estoque(id_produto, quantidade):

    produto = consultar_id(id_produto)

    if produto is None:
        return False

    if quantidade > produto[3]:
        return False

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
    """, (quantidade, id_produto))

    conexao.commit()
    conexao.close()

    registrar_movimentacao(id_produto, "Saída", quantidade)

    return True