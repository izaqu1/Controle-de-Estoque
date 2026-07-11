banco.py

import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        quantidade INTEGER,
        preco REAL
    )
    """)

    conexao.commit()
    conexao.close()

def cadastrar(nome, quantidade, preco):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO produtos(nome, quantidade, preco) VALUES(?,?,?)",
        (nome, quantidade, preco)
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