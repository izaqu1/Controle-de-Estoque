
import sqlite3
import math
from pathlib import Path
from datetime import datetime


# Mantém o banco.db na mesma pasta deste arquivo, mesmo quando o programa
# é iniciado por um atalho ou por outro diretório.
CAMINHO_BANCO = Path(__file__).resolve().parent / "banco.db"


def _numero_valido(valor):
    """Confere se o valor é numérico, finito e não negativo."""
    if isinstance(valor, bool):
        return False
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return False
    return math.isfinite(numero) and numero >= 0


def _inteiro_nao_negativo(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0


def _inteiro_positivo(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _texto_obrigatorio(valor):
    return isinstance(valor, str) and bool(valor.strip())


def conectar():
    conexao = sqlite3.connect(str(CAMINHO_BANCO), timeout=10)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    #============================
    # Tabela original de produtos
    #============================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            quantidade_minima INTEGER NOT NULL
        )
    """)
    #=================================
    # Tabela original de movimentações
    #=================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_produto) REFERENCES produtos(id)
        )
    """)
    #=================================================================
    # Migração: acrescenta novos campos sem apagar produtos existentes
    #=================================================================
    colunas = [
        coluna[1] for coluna in cursor.execute(
            "PRAGMA table_info(produtos)"
        ).fetchall()
    ]

    if "codigo" not in colunas:
        cursor.execute("ALTER TABLE produtos ADD COLUMN codigo TEXT")

    if "marca" not in colunas:
        cursor.execute("ALTER TABLE produtos ADD COLUMN marca TEXT")

    if "preco" not in colunas:
        cursor.execute(
            "ALTER TABLE produtos ADD COLUMN preco REAL NOT NULL DEFAULT 0"
        )

    if "ativo" not in colunas:
        cursor.execute(
            "ALTER TABLE produtos ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1"
        )
    #=================
    # Tabela de caixas
    #=================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caixas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_abertura DATETIME NOT NULL,
            valor_inicial REAL NOT NULL,
            responsavel TEXT NOT NULL,
            data_fechamento DATETIME,
            valor_contado REAL,
            valor_esperado REAL,
            diferenca REAL,
            status TEXT NOT NULL DEFAULT 'Aberto'
        )
    """)
    #=================
    # Tabela de vendas
    #=================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATETIME NOT NULL,
            forma_pagamento TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Concluida',
            id_caixa INTEGER,
            FOREIGN KEY(id_caixa) REFERENCES caixas(id)
        )
    """)
    #======================
    #Produtos de cada venda
    #======================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER NOT NULL,
            id_produto INTEGER,
            codigo TEXT,
            nome TEXT NOT NULL,
            marca TEXT,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY(id_venda) REFERENCES vendas(id),
            FOREIGN KEY(id_produto) REFERENCES produtos(id)
        )
    """)

    cursor.execute(
        "UPDATE vendas SET forma_pagamento = 'CARTEIRA' WHERE forma_pagamento = 'Faturado'"
    )
    conexao.commit()
    conexao.close()


# ========
# PRODUTOS
# ========
def cadastrar(nome, categoria, quantidade, quantidade_minima,
              codigo=None, marca=None, preco=0):
    if not _texto_obrigatorio(nome) or not _texto_obrigatorio(categoria):
        return False
    if not _inteiro_nao_negativo(quantidade):
        return False
    if not _inteiro_nao_negativo(quantidade_minima):
        return False
    if not _numero_valido(preco):
        return False
    if codigo is not None and (not isinstance(codigo, str) or not codigo.strip()):
        return False

    nome = nome.strip()
    categoria = categoria.strip()
    codigo = codigo.strip() if codigo else None
    marca = marca.strip() if isinstance(marca, str) and marca.strip() else None

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        if codigo:
            cursor.execute("SELECT 1 FROM produtos WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                return False

        cursor.execute("""
            INSERT INTO produtos
            (nome, categoria, quantidade, quantidade_minima,
             codigo, marca, preco)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, categoria, quantidade, quantidade_minima,
              codigo, marca, float(preco)))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def listar():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos WHERE ativo = 1 ORDER BY id")
    produtos = cursor.fetchall()

    conexao.close()
    return produtos


def consultar_id(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE id = ? AND ativo = 1",
        (id_produto,)
    )

    produto = cursor.fetchone()
    conexao.close()

    return produto


def consultar_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE LOWER(nome) = LOWER(?) AND ativo = 1",
        (nome,)
    )

    produtos = cursor.fetchall()
    conexao.close()

    return produtos


def consultar_codigo(codigo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE codigo = ? AND ativo = 1",
        (codigo,)
    )

    produto = cursor.fetchone()
    conexao.close()

    return produto


def excluir(id_produto):
    """Inativa o produto para preservar vendas e movimentações antigas."""
    if not _inteiro_positivo(id_produto):
        return False

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE produtos SET ativo = 0 WHERE id = ? AND ativo = 1",
            (id_produto,)
        )
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT categoria
        FROM produtos
        WHERE ativo = 1
        ORDER BY categoria
    """)

    categorias = cursor.fetchall()
    conexao.close()

    return categorias


def consultar_categoria(categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos WHERE LOWER(categoria) = LOWER(?) AND ativo = 1",
        (categoria,)
    )

    produtos = cursor.fetchall()
    conexao.close()

    return produtos


def atualizar(id_produto, nome, categoria, quantidade,
              quantidade_minima, codigo=None, marca=None, preco=0):
    if not _inteiro_positivo(id_produto):
        return False
    if not _texto_obrigatorio(nome) or not _texto_obrigatorio(categoria):
        return False
    if not _inteiro_nao_negativo(quantidade):
        return False
    if not _inteiro_nao_negativo(quantidade_minima):
        return False
    if not _numero_valido(preco):
        return False
    if codigo is not None and (not isinstance(codigo, str) or not codigo.strip()):
        return False

    codigo = codigo.strip() if codigo else None
    marca = marca.strip() if isinstance(marca, str) and marca.strip() else None
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        if codigo:
            cursor.execute(
                "SELECT 1 FROM produtos WHERE codigo = ? AND id <> ?",
                (codigo, id_produto)
            )
            if cursor.fetchone():
                return False

        cursor.execute("""
            UPDATE produtos
            SET nome = ?, categoria = ?, quantidade = ?,
                quantidade_minima = ?, codigo = ?, marca = ?, preco = ?
            WHERE id = ? AND ativo = 1
        """, (nome.strip(), categoria.strip(), quantidade,
              quantidade_minima, codigo, marca, float(preco), id_produto))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


# ========================
# MOVIMENTAÇÕES DE ESTOQUE
# ========================

def registrar_movimentacao(id_produto, tipo, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_produto, tipo, quantidade)
        VALUES (?, ?, ?)
    """, (id_produto, tipo, quantidade))

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
        LEFT JOIN produtos p ON p.id = m.id_produto
        ORDER BY m.data DESC
    """)

    movimentacoes = cursor.fetchall()
    conexao.close()

    return movimentacoes


def entrada_estoque(id_produto, quantidade):
    if not _inteiro_positivo(id_produto) or not _inteiro_positivo(quantidade):
        return False

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade + ?
            WHERE id = ?
        """, (quantidade, id_produto))

        if cursor.rowcount == 0:
            conexao.rollback()
            return False

        cursor.execute("""
            INSERT INTO movimentacoes
            (id_produto, tipo, quantidade)
            VALUES (?, 'Entrada', ?)
        """, (id_produto, quantidade))

        conexao.commit()
        return True

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def saida_estoque(id_produto, quantidade):
    if not _inteiro_positivo(id_produto) or not _inteiro_positivo(quantidade):
        return False

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade - ?
            WHERE id = ? AND quantidade >= ?
        """, (quantidade, id_produto, quantidade))

        if cursor.rowcount == 0:
            conexao.rollback()
            return False

        cursor.execute("""
            INSERT INTO movimentacoes
            (id_produto, tipo, quantidade)
            VALUES (?, 'Saída', ?)
        """, (id_produto, quantidade))

        conexao.commit()
        return True

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


# =====
# CAIXA
# =====

def caixa_aberto():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM caixas
        WHERE status = 'Aberto'
        ORDER BY id DESC
        LIMIT 1
    """)

    caixa = cursor.fetchone()
    conexao.close()

    return caixa


def abrir_caixa(valor_inicial, responsavel):
    if not _numero_valido(valor_inicial) or not _texto_obrigatorio(responsavel):
        return False
    valor_inicial = float(valor_inicial)
    responsavel = responsavel.strip()

    if caixa_aberto():
        return False

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO caixas (data_abertura, valor_inicial, responsavel)
        VALUES (?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        valor_inicial,
        responsavel
    ))

    conexao.commit()
    conexao.close()

    return True


def calcular_dinheiro_esperado(id_caixa):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM vendas
        WHERE id_caixa = ?
          AND forma_pagamento = 'Dinheiro'
          AND status = 'Concluida'
    """, (id_caixa,))

    total_vendas_dinheiro = cursor.fetchone()[0]

    cursor.execute("""
        SELECT valor_inicial
        FROM caixas
        WHERE id = ?
    """, (id_caixa,))

    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    return resultado[0] + total_vendas_dinheiro


def fechar_caixa(valor_contado):
    if not _numero_valido(valor_contado):
        return False
    valor_contado = float(valor_contado)

    caixa = caixa_aberto()

    if caixa is None:
        return False

    id_caixa = caixa[0]
    esperado = calcular_dinheiro_esperado(id_caixa)
    diferenca = valor_contado - esperado

    conexao = conectar()
    cursor = conexao.cursor()

    # Soma as vendas concluídas deste caixa, separadas por pagamento.
    cursor.execute("""
        SELECT forma_pagamento, COALESCE(SUM(total), 0), COUNT(*)
        FROM vendas
        WHERE id_caixa = ? AND status = 'Concluida'
        GROUP BY forma_pagamento
    """, (id_caixa,))
    pagamentos_consultados = cursor.fetchall()

    formas = ["Dinheiro", "PIX", "Crédito", "Débito", "CARTEIRA"]
    pagamentos = {
        forma: {"total": 0.0, "quantidade": 0}
        for forma in formas
    }
    for forma, total, quantidade in pagamentos_consultados:
        chave = forma.upper() if forma.upper() == "PIX" else forma
        if chave in pagamentos:
            pagamentos[chave] = {
                "total": float(total or 0),
                "quantidade": int(quantidade or 0)
            }

    total_vendas = sum(item["total"] for item in pagamentos.values())
    dinheiro_vendas = pagamentos["Dinheiro"]["total"]

    cursor.execute("""
        UPDATE caixas
        SET data_fechamento = ?,
            valor_contado = ?,
            valor_esperado = ?,
            diferenca = ?,
            status = 'Fechado'
        WHERE id = ?
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        valor_contado,
        esperado,
        diferenca,
        id_caixa
    ))

    conexao.commit()
    conexao.close()

    return {
        "esperado": esperado,
        "contado": valor_contado,
        "diferenca": diferenca,
        "valor_inicial": float(caixa[2] or 0),
        "vendas_dinheiro": dinheiro_vendas,
        "pagamentos": pagamentos,
        "total_vendas": total_vendas
    }


# ======
# VENDAS
# ======

def registrar_venda(itens, forma_pagamento):
    formas_validas = [
        "PIX", "Crédito", "Débito", "Dinheiro", "CARTEIRA"
    ]

    if forma_pagamento not in formas_validas or not itens:
        return False

    caixa = caixa_aberto()

    if caixa is None:
        return False

    id_caixa = caixa[0]
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        total = 0
        itens_processados = []

        # Valida e prepara todos os itens
        for item in itens:
            quantidade = item["quantidade"]
            preco = item["valor_unitario"]
            id_produto = item.get("id_produto")

            if not _inteiro_positivo(quantidade):
                raise ValueError("Quantidade inválida.")

            if not _numero_valido(preco):
                raise ValueError("Preço inválido.")
            preco = float(preco)

            # Produto cadastrado: verifica estoque
            if id_produto is not None:
                cursor.execute(
                    "SELECT * FROM produtos WHERE id = ? AND ativo = 1",
                    (id_produto,)
                )
                produto = cursor.fetchone()

                if produto is None:
                    raise ValueError("Produto não encontrado.")

                if produto[3] < quantidade:
                    raise ValueError(
                        f"Estoque insuficiente para {produto[1]}."
                    )

                codigo = produto[5]
                nome = produto[1]
                marca = produto[6]

            # Item avulso: não consulta nem altera estoque
            else:
                codigo = item.get("codigo")
                nome = item.get("nome", "")
                nome = nome.strip() if isinstance(nome, str) else ""
                marca = item.get("marca")
                marca = marca.strip() if isinstance(marca, str) and marca.strip() else None
                codigo = codigo.strip() if isinstance(codigo, str) and codigo.strip() else None

                if not nome:
                    raise ValueError(
                        "O nome do item avulso é obrigatório."
                    )

            subtotal = preco * quantidade
            total += subtotal

            itens_processados.append({
                "id_produto": id_produto,
                "codigo": codigo,
                "nome": nome,
                "marca": marca,
                "quantidade": quantidade,
                "preco": preco,
                "subtotal": subtotal
            })

        # Registra a venda
        cursor.execute("""
            INSERT INTO vendas
            (data, forma_pagamento, total, status, id_caixa)
            VALUES (?, ?, ?, 'Concluida', ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            forma_pagamento,
            total,
            id_caixa
        ))

        id_venda = cursor.lastrowid

        # Registra todos os itens
        for item in itens_processados:
            cursor.execute("""
                INSERT INTO itens_venda
                (id_venda, id_produto, codigo, nome, marca,
                 quantidade, valor_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_venda,
                item["id_produto"],
                item["codigo"],
                item["nome"],
                item["marca"],
                item["quantidade"],
                item["preco"],
                item["subtotal"]
            ))

            # Só dá baixa no estoque se for produto cadastrado
            if item["id_produto"] is not None:
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade = quantidade - ?
                    WHERE id = ? AND quantidade >= ?
                """, (
                    item["quantidade"],
                    item["id_produto"],
                    item["quantidade"]
                ))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"Não foi possível atualizar o estoque "
                        f"de {item['nome']}."
                    )

                cursor.execute("""
                    INSERT INTO movimentacoes
                    (id_produto, tipo, quantidade)
                    VALUES (?, 'Venda', ?)
                """, (
                    item["id_produto"],
                    item["quantidade"]
                ))

        conexao.commit()

        return {
            "id_venda": id_venda,
            "total": total
        }

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, data, forma_pagamento, total, status
        FROM vendas
        ORDER BY data DESC
    """)

    vendas = cursor.fetchall()
    conexao.close()

    return vendas


def consultar_itens_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT codigo, nome, marca, quantidade,
               valor_unitario, subtotal
        FROM itens_venda
        WHERE id_venda = ?
    """, (id_venda,))

    itens = cursor.fetchall()
    conexao.close()

    return itens


def cancelar_venda(id_venda):
    if not _inteiro_positivo(id_venda):
        return False

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT status
            FROM vendas
            WHERE id = ?
        """, (id_venda,))

        venda = cursor.fetchone()

        if venda is None or venda[0] != "Concluida":
            return False

        cursor.execute("""
            SELECT id_produto, quantidade
            FROM itens_venda
            WHERE id_venda = ?
        """, (id_venda,))

        itens = cursor.fetchall()

        for id_produto, quantidade in itens:
            if id_produto is not None:
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade = quantidade + ?
                    WHERE id = ?
                """, (quantidade, id_produto))

                cursor.execute("""
                    INSERT INTO movimentacoes
                    (id_produto, tipo, quantidade)
                    VALUES (?, 'Cancelamento de venda', ?)
                """, (id_produto, quantidade))

        cursor.execute("""
            UPDATE vendas
            SET status = 'Cancelada'
            WHERE id = ?
        """, (id_venda,))

        conexao.commit()
        return True

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


# ==========================================================
# RELATÓRIOS
# ==========================================================

def relatorio_vendas(data_inicio, data_fim):
    if not isinstance(data_inicio, str) or not isinstance(data_fim, str):
        raise ValueError("Informe as datas no formato AAAA-MM-DD.")
    try:
        inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
    except ValueError as erro:
        raise ValueError("Informe as datas no formato AAAA-MM-DD.") from erro
    if inicio > fim:
        raise ValueError("A data inicial não pode ser posterior à data final.")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(CASE
                WHEN status = 'Concluida' THEN total
                ELSE 0
            END), 0),
            COALESCE(SUM(CASE
                WHEN status = 'Cancelada' THEN 1
                ELSE 0
            END), 0)
        FROM vendas
        WHERE date(data) BETWEEN date(?) AND date(?)
    """, (data_inicio, data_fim))

    resumo = cursor.fetchone()

    cursor.execute("""
        SELECT forma_pagamento, SUM(total), COUNT(*)
        FROM vendas
        WHERE date(data) BETWEEN date(?) AND date(?)
          AND status = 'Concluida'
        GROUP BY forma_pagamento
    """, (data_inicio, data_fim))

    pagamentos = cursor.fetchall()

    cursor.execute("""
        SELECT COALESCE(SUM(quantidade), 0)
        FROM itens_venda i
        JOIN vendas v ON v.id = i.id_venda
        WHERE date(v.data) BETWEEN date(?) AND date(?)
          AND v.status = 'Concluida'
    """, (data_inicio, data_fim))

    quantidade_itens = cursor.fetchone()[0]

    conexao.close()

    quantidade_vendas = resumo[0] - resumo[2]
    faturamento = resumo[1]
    ticket_medio = (
        faturamento / quantidade_vendas
        if quantidade_vendas > 0 else 0
    )

    return {
        "total_registros": resumo[0],
        "vendas_concluidas": quantidade_vendas,
        "faturamento": faturamento,
        "canceladas": resumo[2],
        "quantidade_itens": quantidade_itens,
        "ticket_medio": ticket_medio,
        "pagamentos": pagamentos
    }



def vendas_periodo_exportacao(data_inicio, data_fim):
    """Retorna vendas e itens do período para exportação de relatórios."""
    # Reutiliza a validação de datas do relatório principal.
    relatorio_vendas(data_inicio, data_fim)

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, data, forma_pagamento, total, status
            FROM vendas
            WHERE date(data) BETWEEN date(?) AND date(?)
            ORDER BY data, id
        """, (data_inicio, data_fim))
        vendas = cursor.fetchall()

        cursor.execute("""
            SELECT v.id, v.data, v.forma_pagamento, v.status,
                   i.codigo, i.nome, i.marca, i.quantidade,
                   i.valor_unitario, i.subtotal
            FROM vendas v
            LEFT JOIN itens_venda i ON i.id_venda = v.id
            WHERE date(v.data) BETWEEN date(?) AND date(?)
            ORDER BY v.data, v.id, i.id
        """, (data_inicio, data_fim))
        itens = cursor.fetchall()

        return vendas, itens
    finally:
        conexao.close()
