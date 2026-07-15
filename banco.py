import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        estoque_minimo INTEGER NOT NULL
    )
    """)

    conexao.commit()
    conexao.close()

def cadastrar(nome, categoria, quantidade, estoque_minimo):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO produtos(nome, categoria, quantidade, estoque_minimo) VALUES(?,?,?,?)",
        (nome, categoria, quantidade, estoque_minimo)
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
        "SELECT * FROM produtos WHERE categoria = ?",
        (categoria,)
    )

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def atualizar(id_produto, nome, categoria, quantidade, estoque_minimo):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE produtos SET nome = ?, categoria = ?, quantidade = ?, estoque_minimo = ? WHERE id = ?",
        (nome, categoria, quantidade, estoque_minimo, id_produto)
    )

    conexao.commit()
    conexao.close()