
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import banco


class SistemaEstoque:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("ELETRO VERA CRUZ")
        self.janela.geometry("1150x720")
        self.janela.minsize(950, 600)

        self.carrinho = []
        self.produto_selecionado_id = None

        banco.criar_tabela()

        self.criar_interface()
        self.atualizar_produtos()
        self.atualizar_vendas()
        self.atualizar_status_caixa()

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="ELETRO VERA CRUZ",
            font=("Arial", 20, "bold"),
            pady=15
        )
        titulo.pack()

        self.status_caixa = tk.Label(
            self.janela,
            text="Verificando caixa...",
            font=("Arial", 11, "bold")
        )
        self.status_caixa.pack(pady=5)

        # Estilos para deixar as abas mais fáceis de identificar e clicar.
        estilo = ttk.Style(self.janela)
        estilo.configure(
            "TNotebook.Tab",
            font=("Arial", 11, "bold"),
            padding=(18, 10)
        )
        estilo.configure(
            "Finalizar.TButton",
            font=("Arial", 13, "bold"),
            padding=(28, 14)
        )

        abas = ttk.Notebook(self.janela)
        abas.pack(fill="both", expand=True, padx=12, pady=12)

        self.aba_produtos = ttk.Frame(abas)
        self.aba_vendas = ttk.Frame(abas)
        self.aba_caixa = ttk.Frame(abas)
        self.aba_relatorios = ttk.Frame(abas)

        abas.add(self.aba_produtos, text="Produtos")
        abas.add(self.aba_vendas, text="Vendas")
        abas.add(self.aba_caixa, text="Caixa")
        abas.add(self.aba_relatorios, text="Relatórios")

        self.criar_aba_produtos()
        self.criar_aba_vendas()
        self.criar_aba_caixa()
        self.criar_aba_relatorios()
        

    # ========
    # PRODUTOS
    # ========

    def criar_aba_produtos(self):
        formulario = ttk.LabelFrame(
            self.aba_produtos,
            text="Cadastro e edição de produtos",
            padding=12
        )
        formulario.pack(fill="x", padx=12, pady=12)

        campos = [
            ("Código", "codigo"),
            ("Nome", "nome"),
            ("Categoria", "categoria"),
            ("Marca", "marca"),
            ("Quantidade", "quantidade"),
            ("Quantidade mínima", "minima"),
            ("Preço unitário", "preco")
        ]

        self.campos_produto = {}

        for i, (rotulo, chave) in enumerate(campos):
            linha = i // 4
            coluna = (i % 4) * 2

            ttk.Label(formulario, text=rotulo).grid(
                row=linha * 2,
                column=coluna,
                sticky="w",
                padx=5,
                pady=4
            )

            entrada = ttk.Entry(formulario, width=22)
            entrada.grid(
                row=linha * 2 + 1,
                column=coluna,
                padx=5,
                pady=4
            )

            self.campos_produto[chave] = entrada

        ttk.Button(
            formulario,
            text="Cadastrar produto",
            command=self.cadastrar_produto
        ).grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(
            formulario,
            text="Limpar campos",
            command=self.limpar_campos_produto
        ).grid(row=4, column=2, columnspan=2, pady=10)

        ttk.Button(
            formulario,
            text="Salvar edição",
            command=self.editar_produto
        ).grid(row=4, column=4, columnspan=2, pady=10)

        ttk.Button(
            formulario,
            text="Excluir selecionado",
            command=self.excluir_produto
        ).grid(row=4, column=6, columnspan=2, pady=10)

        tabela_frame = ttk.LabelFrame(
            self.aba_produtos,
            text="Produtos cadastrados",
            padding=10
        )
        tabela_frame.pack(fill="both", expand=True, padx=12, pady=8)

        colunas = (
            "id", "codigo", "nome", "categoria",
            "marca", "quantidade", "minima", "preco"
        )

        self.tabela_produtos = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )

        titulos = {
            "id": "ID",
            "codigo": "Código",
            "nome": "Nome",
            "categoria": "Categoria",
            "marca": "Marca",
            "quantidade": "Estoque",
            "minima": "Mínimo",
            "preco": "Preço"
        }

        larguras = {
            "id": 45,
            "codigo": 90,
            "nome": 170,
            "categoria": 110,
            "marca": 110,
            "quantidade": 75,
            "minima": 75,
            "preco": 90
        }

        for coluna in colunas:
            self.tabela_produtos.heading(
                coluna,
                text=titulos[coluna]
            )
            self.tabela_produtos.column(
                coluna,
                width=larguras[coluna],
                anchor="center"
            )

        self.tabela_produtos.pack(fill="both", expand=True)
        self.tabela_produtos.bind(
            "<<TreeviewSelect>>", self.selecionar_produto
        )

        ttk.Button(
            tabela_frame,
            text="Atualizar lista",
            command=self.atualizar_produtos
        ).pack(pady=8)

    def cadastrar_produto(self):
        try:
            codigo = self.campos_produto["codigo"].get().strip()
            nome = self.campos_produto["nome"].get().strip()
            categoria = self.campos_produto["categoria"].get().strip()
            marca = self.campos_produto["marca"].get().strip()

            quantidade = int(
                self.campos_produto["quantidade"].get()
            )
            minima = int(
                self.campos_produto["minima"].get()
            )
            preco = float(
                self.campos_produto["preco"].get().replace(",", ".")
            )

            if not nome or not categoria:
                messagebox.showwarning(
                    "Atenção",
                    "Preencha o nome e a categoria."
                )
                return

            if quantidade < 0 or minima < 0 or preco < 0:
                messagebox.showwarning(
                    "Atenção",
                    "Os valores não podem ser negativos."
                )
                return

            if codigo and banco.consultar_codigo(codigo):
                messagebox.showwarning(
                    "Atenção",
                    "Já existe um produto com esse código."
                )
                return

            sucesso = banco.cadastrar(
                nome,
                categoria,
                quantidade,
                minima,
                codigo or None,
                marca or None,
                preco
            )

            if sucesso:
                messagebox.showinfo(
                    "Sucesso",
                    "Produto cadastrado!"
                )
                self.limpar_campos_produto()
                self.atualizar_produtos()
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível cadastrar o produto."
                )

        except ValueError:
            messagebox.showerror(
                "Dados inválidos",
                "Confira as quantidades e o preço."
            )

    def limpar_campos_produto(self):
        for campo in self.campos_produto.values():
            campo.delete(0, tk.END)
        self.produto_selecionado_id = None

    def selecionar_produto(self, evento=None):
        selecionado = self.tabela_produtos.selection()
        if not selecionado:
            return

        valores = self.tabela_produtos.item(selecionado[0], "values")
        self.produto_selecionado_id = int(valores[0])
        produto = banco.consultar_id(self.produto_selecionado_id)
        if produto is None:
            return

        dados = {
            "codigo": produto[5] or "",
            "nome": produto[1] or "",
            "categoria": produto[2] or "",
            "marca": produto[6] or "",
            "quantidade": produto[3],
            "minima": produto[4],
            "preco": str(produto[7]).replace(".", ",")
        }
        for chave, valor in dados.items():
            campo = self.campos_produto[chave]
            campo.delete(0, tk.END)
            campo.insert(0, str(valor))

    def editar_produto(self):
        if self.produto_selecionado_id is None:
            messagebox.showwarning(
                "Atenção", "Selecione um produto na tabela para editar."
            )
            return
        try:
            codigo = self.campos_produto["codigo"].get().strip()
            nome = self.campos_produto["nome"].get().strip()
            categoria = self.campos_produto["categoria"].get().strip()
            marca = self.campos_produto["marca"].get().strip()
            quantidade = int(self.campos_produto["quantidade"].get())
            minima = int(self.campos_produto["minima"].get())
            preco = float(self.campos_produto["preco"].get().replace(",", "."))

            sucesso = banco.atualizar(
                self.produto_selecionado_id, nome, categoria,
                quantidade, minima, codigo or None, marca or None, preco
            )
            if not sucesso:
                messagebox.showerror(
                    "Não foi possível editar",
                    "Confira os dados. O código pode já estar em uso."
                )
                return
            messagebox.showinfo("Sucesso", "Produto atualizado.")
            self.limpar_campos_produto()
            self.atualizar_produtos()
        except ValueError:
            messagebox.showerror(
                "Dados inválidos", "Confira quantidades e preço."
            )

    def excluir_produto(self):
        if self.produto_selecionado_id is None:
            messagebox.showwarning(
                "Atenção", "Selecione um produto na tabela para excluir."
            )
            return
        selecionado = self.tabela_produtos.selection()
        nome = self.tabela_produtos.item(selecionado[0], "values")[2]
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja inativar o produto '{nome}'?\n\nEle deixará de aparecer para novas vendas, mas o histórico será mantido."
        )
        if not confirmar:
            return
        try:
            sucesso = banco.excluir(self.produto_selecionado_id)
            if sucesso:
                messagebox.showinfo("Sucesso", "Produto inativado. Ele não aparecerá em novos cadastros de venda, e o histórico foi preservado.")
                self.limpar_campos_produto()
                self.atualizar_produtos()
            else:
                messagebox.showerror(
                    "Não foi possível excluir",
                    "Não foi possível inativar este produto. Atualize a lista e tente novamente."
                )
        except Exception as erro:
            messagebox.showerror("Erro ao excluir", str(erro))

    def atualizar_produtos(self):
        for item in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(item)

        for p in banco.listar():
            self.tabela_produtos.insert(
                "",
                tk.END,
                values=(
                    p[0],
                    p[5] or "",
                    p[1],
                    p[2],
                    p[6] or "",
                    p[3],
                    p[4],
                    f"R$ {p[7]:.2f}"
                )
            )

        self.atualizar_selecao_venda()

    # ==================================================
    # VENDAS
    # ==================================================

    def criar_aba_vendas(self):
        area = ttk.Frame(self.aba_vendas, padding=10)
        area.pack(fill="both", expand=True)

        # A tela usa grid para manter os controles principais visíveis
        # mesmo quando a janela não está maximizada.
        area.columnconfigure(0, weight=1)
        area.rowconfigure(2, weight=1)

        ttk.Label(
            area,
            text="Nova venda",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        selecao = ttk.LabelFrame(
            area,
            text="Adicionar produto",
            padding=8
        )
        selecao.grid(row=1, column=0, sticky="ew", pady=(0, 7))
        selecao.columnconfigure(0, weight=1)

        ttk.Label(selecao, text="Produto").grid(
            row=0, column=0, padx=5, sticky="w"
        )
        self.produto_venda = ttk.Combobox(
            selecao,
            state="readonly",
            width=55
        )
        self.produto_venda.grid(
            row=1, column=0, padx=5, sticky="ew"
        )

        ttk.Label(selecao, text="Quantidade").grid(
            row=0, column=1, padx=5, sticky="w"
        )
        self.quantidade_venda = ttk.Entry(selecao, width=10)
        self.quantidade_venda.grid(row=1, column=1, padx=5)
        self.quantidade_venda.insert(0, "1")

        ttk.Button(
            selecao,
            text="Adicionar",
            command=self.adicionar_carrinho
        ).grid(row=1, column=2, padx=5)

        ttk.Button(
            selecao,
            text="Criar item avulso",
            command=self.criar_item_avulso
        ).grid(row=1, column=3, padx=5)

        carrinho_frame = ttk.LabelFrame(
            area,
            text="Itens da venda",
            padding=8
        )
        carrinho_frame.grid(
            row=2, column=0, sticky="nsew", pady=(0, 7)
        )
        carrinho_frame.columnconfigure(0, weight=1)
        carrinho_frame.rowconfigure(0, weight=1)

        colunas = (
            "codigo", "produto", "marca",
            "quantidade", "unitario", "subtotal"
        )
        self.tabela_carrinho = ttk.Treeview(
            carrinho_frame,
            columns=colunas,
            show="headings",
            height=7
        )
        titulos = [
            "Código", "Produto", "Marca",
            "Quantidade", "Valor unitário", "Subtotal"
        ]
        for coluna, titulo in zip(colunas, titulos):
            self.tabela_carrinho.heading(coluna, text=titulo)
            self.tabela_carrinho.column(
                coluna, width=115, anchor="center"
            )
        self.tabela_carrinho.grid(
            row=0, column=0, sticky="nsew"
        )

        botoes = ttk.Frame(area)
        botoes.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(
            botoes,
            text="Remover item selecionado",
            command=self.remover_item
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            botoes,
            text="Limpar venda",
            command=self.limpar_carrinho
        ).pack(side="left", padx=5)

        # Rodapé único: pagamento, total e finalização permanecem juntos
        # e visíveis em janelas menores, sem depender de tela cheia.
        rodape_venda = ttk.Frame(area, padding=(4, 7))
        rodape_venda.grid(row=4, column=0, sticky="ew")
        rodape_venda.columnconfigure(2, weight=1)

        ttk.Label(
            rodape_venda,
            text="Pagamento:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.forma_pagamento = ttk.Combobox(
            rodape_venda,
            state="readonly",
            values=["PIX", "Crédito", "Débito", "Dinheiro", "CARTEIRA"],
            width=14
        )
        self.forma_pagamento.grid(row=0, column=1, padx=(0, 12))
        self.forma_pagamento.set("Dinheiro")

        self.total_label = ttk.Label(
            rodape_venda,
            text="TOTAL: R$ 0,00",
            font=("Arial", 17, "bold")
        )
        self.total_label.grid(row=0, column=2, padx=8, sticky="e")

        ttk.Button(
            rodape_venda,
            text="FINALIZAR VENDA",
            style="Finalizar.TButton",
            command=self.finalizar_venda
        ).grid(row=0, column=3, padx=(10, 2), ipadx=10, ipady=3)

    def atualizar_selecao_venda(self):
        if not hasattr(self, "produto_venda"):
            return

        self.produtos_disponiveis = banco.listar()

        opcoes = []

        for p in self.produtos_disponiveis:
            codigo = p[5] or str(p[0])
            marca = p[6] or "Sem marca"

            opcoes.append(
                f"{codigo} - {p[1]} - {marca} "
                f"(Estoque: {p[3]})"
            )

        self.produto_venda["values"] = opcoes

        if opcoes:
            self.produto_venda.current(0)
        else:
            self.produto_venda.set("")
    
    def criar_item_avulso(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Adicionar item avulso")
        janela.geometry("420x330")
        janela.resizable(False, False)
        janela.transient(self.janela)
        janela.grab_set()

        campos = {}
        dados = [
            ("Código (opcional)", "codigo"),
            ("Nome do produto", "nome"),
            ("Marca (opcional)", "marca"),
            ("Quantidade", "quantidade"),
            ("Preço unitário", "preco")
        ]
        for linha, (rotulo, chave) in enumerate(dados):
            ttk.Label(janela, text=rotulo).grid(
                row=linha, column=0, padx=12, pady=9, sticky="w"
            )
            entrada = ttk.Entry(janela, width=25)
            entrada.grid(row=linha, column=1, padx=12, pady=9)
            campos[chave] = entrada
        campos["quantidade"].insert(0, "1")

        def adicionar():
            try:
                codigo = campos["codigo"].get().strip()
                nome = campos["nome"].get().strip()
                marca = campos["marca"].get().strip()
                quantidade = int(campos["quantidade"].get())
                preco = float(campos["preco"].get().replace(",", "."))
                if not nome or quantidade <= 0 or preco < 0:
                    raise ValueError
                self.carrinho.append({
                    "id_produto": None, "codigo": codigo or None,
                    "nome": nome, "marca": marca or None,
                    "quantidade": quantidade, "valor_unitario": preco
                })
                self.atualizar_carrinho()
                janela.destroy()
            except ValueError:
                messagebox.showerror(
                    "Dados inválidos",
                    "Informe um nome, quantidade positiva e preço válido.",
                    parent=janela
                )

        ttk.Button(
            janela, text="Adicionar à venda", command=adicionar
        ).grid(row=len(dados), column=0, columnspan=2, pady=15)

    def adicionar_carrinho(self):
        try:
            indice = self.produto_venda.current()

            if indice < 0:
                messagebox.showwarning(
                    "Atenção",
                    "Selecione um produto."
                )
                return

            quantidade = int(self.quantidade_venda.get())

            if quantidade <= 0:
                raise ValueError

            produto = self.produtos_disponiveis[indice]

            if quantidade > produto[3]:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    f"Disponível: {produto[3]}"
                )
                return

            # Permite adicionar o mesmo produto mais de uma vez,
            # desde que a soma não ultrapasse o estoque.
            item_existente = next(
                (
                    item for item in self.carrinho
                    if item["id_produto"] == produto[0]
                ),
                None
            )

            quantidade_total = quantidade

            if item_existente:
                quantidade_total += item_existente["quantidade"]

            if quantidade_total > produto[3]:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    f"Disponível: {produto[3]}"
                )
                return

            if item_existente:
                item_existente["quantidade"] = quantidade_total
                item_existente["subtotal"] = (
                    quantidade_total * item_existente["valor_unitario"]
                )
            else:
                self.carrinho.append({
                    "id_produto": produto[0],
                    "quantidade": quantidade,
                    "valor_unitario": produto[7]
                })

            self.atualizar_carrinho()
            self.quantidade_venda.delete(0, tk.END)
            self.quantidade_venda.insert(0, "1")

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite uma quantidade inteira válida."
            )

    def atualizar_carrinho(self):
        for item_id in self.tabela_carrinho.get_children():
            self.tabela_carrinho.delete(item_id)

        total = 0
        for item in self.carrinho:
            produto = banco.consultar_id(item["id_produto"]) if item.get("id_produto") is not None else None
            if item.get("id_produto") is not None and produto is None:
                continue
            codigo = (produto[5] or produto[0]) if produto else (item.get("codigo") or "")
            nome = produto[1] if produto else item.get("nome", "")
            marca = (produto[6] or "") if produto else (item.get("marca") or "")
            subtotal = item["quantidade"] * item["valor_unitario"]
            item["subtotal"] = subtotal
            total += subtotal
            self.tabela_carrinho.insert(
                "", tk.END,
                values=(codigo, nome, marca, item["quantidade"],
                        f"R$ {item['valor_unitario']:.2f}", f"R$ {subtotal:.2f}")
            )
        self.total_label.config(text=f"TOTAL: R$ {total:.2f}")

    def remover_item(self):
        selecionado = self.tabela_carrinho.selection()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um item para remover."
            )
            return

        indice = self.tabela_carrinho.index(selecionado[0])
        self.carrinho.pop(indice)

        self.atualizar_carrinho()

    def limpar_carrinho(self):
        self.carrinho.clear()
        self.atualizar_carrinho()

    def finalizar_venda(self):
        if not self.carrinho:
            messagebox.showwarning(
                "Atenção",
                "Adicione pelo menos um produto."
            )
            return

        forma = self.forma_pagamento.get()

        if not forma:
            messagebox.showwarning(
                "Atenção",
                "Selecione a forma de pagamento."
            )
            return

        if banco.caixa_aberto() is None:
            messagebox.showwarning(
                "Caixa fechado",
                "Abra o caixa antes de registrar uma venda."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar venda",
            f"{self.total_label.cget('text')}\n\n"
            f"Pagamento: {forma}\n\n"
            "Deseja finalizar?"
        )

        if not confirmar:
            return

        try:
            resultado = banco.registrar_venda(
                self.carrinho,
                forma
            )

            if not resultado:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível registrar a venda."
                )
                return

            messagebox.showinfo(
                "Venda concluída",
                f"Venda nº {resultado['id_venda']}\n"
                f"Total: R$ {resultado['total']:.2f}"
            )

            self.limpar_carrinho()
            self.atualizar_produtos()
            self.atualizar_vendas()
            self.atualizar_status_caixa()

        except Exception as erro:
            messagebox.showerror(
                "Erro na venda",
                str(erro)
            )

    # ==================================================
    # CAIXA
    # ==================================================

    def criar_aba_caixa(self):
        area = ttk.Frame(self.aba_caixa, padding=20)
        area.pack(fill="both", expand=True)

        ttk.Label(
            area,
            text="CONTROLE DE CAIXA",
            font=("Arial", 17, "bold")
        ).pack(pady=15)

        abertura = ttk.LabelFrame(
            area,
            text="Abertura de caixa",
            padding=15
        )
        abertura.pack(fill="x", pady=10)

        ttk.Label(
            abertura,
            text="Responsável:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.responsavel = ttk.Entry(
            abertura,
            width=30
        )
        self.responsavel.grid(row=0, column=1, padx=5)

        ttk.Label(
            abertura,
            text="Valor inicial em dinheiro:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.valor_inicial = ttk.Entry(
            abertura,
            width=30
        )
        self.valor_inicial.grid(row=1, column=1, padx=5)

        ttk.Button(
            abertura,
            text="Abrir caixa",
            command=self.abrir_caixa
        ).grid(row=2, column=0, columnspan=2, pady=10)

        fechamento = ttk.LabelFrame(
            area,
            text="Fechamento de caixa",
            padding=15
        )
        fechamento.pack(fill="x", pady=10)

        ttk.Label(
            fechamento,
            text="Dinheiro contado:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.valor_contado = ttk.Entry(
            fechamento,
            width=30
        )
        self.valor_contado.grid(row=0, column=1, padx=5)

        ttk.Button(
            fechamento,
            text="Fechar caixa",
            command=self.fechar_caixa
        ).grid(row=1, column=0, columnspan=2, pady=10)

        # Área de resultado com rolagem para que o fechamento completo
        # continue visível mesmo quando a janela estiver menor.
        quadro_resultado = ttk.LabelFrame(
            area,
            text="Resumo do fechamento",
            padding=8
        )
        quadro_resultado.pack(fill="both", expand=True, pady=(8, 0))

        self.resultado_caixa = tk.Text(
            quadro_resultado,
            height=9,
            font=("Arial", 11),
            wrap="word",
            relief="flat",
            borderwidth=0,
            state="disabled"
        )
        barra_resultado = ttk.Scrollbar(
            quadro_resultado,
            orient="vertical",
            command=self.resultado_caixa.yview
        )
        self.resultado_caixa.configure(yscrollcommand=barra_resultado.set)
        self.resultado_caixa.pack(side="left", fill="both", expand=True)
        barra_resultado.pack(side="right", fill="y")

    def abrir_caixa(self):
        try:
            responsavel = self.responsavel.get().strip()
            valor = float(
                self.valor_inicial.get().replace(",", ".")
            )

            if not responsavel:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o responsável."
                )
                return

            if valor < 0:
                raise ValueError

            sucesso = banco.abrir_caixa(valor, responsavel)

            if sucesso:
                messagebox.showinfo(
                    "Caixa",
                    "Caixa aberto com sucesso!"
                )
                self.atualizar_status_caixa()
            else:
                messagebox.showwarning(
                    "Atenção",
                    "Já existe um caixa aberto ou os dados são inválidos."
                )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Informe um valor inicial válido."
            )

    def fechar_caixa(self):
        try:
            valor = float(
                self.valor_contado.get().replace(",", ".")
            )

            if valor < 0:
                raise ValueError

            confirmar = messagebox.askyesno(
                "Fechar caixa",
                "Tem certeza que deseja fechar o caixa?"
            )

            if not confirmar:
                return

            resultado = banco.fechar_caixa(valor)

            if resultado is False:
                messagebox.showwarning(
                    "Atenção",
                    "Não existe caixa aberto."
                )
                return

            pagamentos = resultado.get("pagamentos", {})
            linhas_pagamento = []
            for forma in ("Dinheiro", "PIX", "Crédito", "Débito", "CARTEIRA"):
                dados = pagamentos.get(forma, {"total": 0, "quantidade": 0})
                linhas_pagamento.append(
                    f"{forma}: R$ {dados['total']:.2f} "
                    f"({dados['quantidade']} venda(s))"
                )

            texto_fechamento = (
                "FECHAMENTO DO CAIXA\n"
                f"Fundo inicial: R$ {resultado.get('valor_inicial', 0):.2f}\n"
                f"Vendas em dinheiro: R$ {resultado.get('vendas_dinheiro', 0):.2f}\n"
                f"Dinheiro esperado na gaveta: R$ {resultado['esperado']:.2f}\n"
                f"Dinheiro contado: R$ {resultado['contado']:.2f}\n"
                f"Diferença: R$ {resultado['diferenca']:.2f}\n\n"
                "RESUMO POR FORMA DE PAGAMENTO\n"
                + "\n".join(linhas_pagamento)
                + f"\n\nTotal de vendas: R$ {resultado.get('total_vendas', 0):.2f}"
            )
            self.resultado_caixa.config(state="normal")
            self.resultado_caixa.delete("1.0", tk.END)
            self.resultado_caixa.insert(tk.END, texto_fechamento)
            self.resultado_caixa.config(state="disabled")
            self.resultado_caixa.yview_moveto(0)

            messagebox.showinfo(
                "Caixa fechado",
                "Fechamento registrado com sucesso."
            )

            self.atualizar_status_caixa()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Informe um valor contado válido."
            )

    def atualizar_status_caixa(self):
        if not hasattr(self, "status_caixa"):
            return

        caixa = banco.caixa_aberto()

        if caixa:
            self.status_caixa.config(
                text=f"CAIXA ABERTO | Responsável: {caixa[3]}",
                foreground="green"
            )
        else:
            self.status_caixa.config(
                text="CAIXA FECHADO",
                foreground="red"
            )

    # ==================================================
    # RELATÓRIOS
    # ==================================================

    def criar_aba_relatorios(self):
        area = ttk.Frame(self.aba_relatorios, padding=15)
        area.pack(fill="both", expand=True)

        ttk.Label(
            area,
            text="RELATÓRIO DE VENDAS",
            font=("Arial", 17, "bold")
        ).pack(pady=10)

        filtros = ttk.Frame(area)
        filtros.pack(fill="x", pady=10)

        ttk.Label(
            filtros,
            text="Data inicial (AAAA-MM-DD):"
        ).pack(side="left", padx=5)

        self.data_inicio = ttk.Entry(
            filtros,
            width=14
        )
        self.data_inicio.pack(side="left", padx=5)
        self.data_inicio.insert(0, date.today().isoformat())

        ttk.Label(
            filtros,
            text="Data final:"
        ).pack(side="left", padx=5)

        self.data_fim = ttk.Entry(
            filtros,
            width=14
        )
        self.data_fim.pack(side="left", padx=5)
        self.data_fim.insert(0, date.today().isoformat())

        ttk.Button(
            filtros,
            text="Consultar",
            command=self.gerar_relatorio
        ).pack(side="left", padx=10)

        ttk.Button(
            filtros,
            text="Exportar PDF",
            command=self.exportar_pdf
        ).pack(side="left", padx=5)

        ttk.Button(
            filtros,
            text="Exportar Excel",
            command=self.exportar_excel
        ).pack(side="left", padx=5)

        self.resumo_relatorio = tk.Text(
            area,
            height=12,
            font=("Consolas", 11)
        )
        self.resumo_relatorio.pack(
            fill="both",
            expand=True,
            pady=10
        )

        historico = ttk.LabelFrame(
            area,
            text="Histórico de vendas",
            padding=8
        )
        historico.pack(fill="both", expand=True)

        colunas = (
            "id", "data", "pagamento", "total", "status"
        )

        self.tabela_vendas = ttk.Treeview(
            historico,
            columns=colunas,
            show="headings"
        )

        titulos = {
            "id": "Venda",
            "data": "Data",
            "pagamento": "Pagamento",
            "total": "Total",
            "status": "Status"
        }

        for coluna in colunas:
            self.tabela_vendas.heading(
                coluna,
                text=titulos[coluna]
            )
            self.tabela_vendas.column(
                coluna,
                width=150,
                anchor="center"
            )

        self.tabela_vendas.pack(fill="both", expand=True)

        ttk.Button(
            historico,
            text="Atualizar histórico",
            command=self.atualizar_vendas
        ).pack(pady=8)

    def atualizar_vendas(self):
        if not hasattr(self, "tabela_vendas"):
            return

        for item in self.tabela_vendas.get_children():
            self.tabela_vendas.delete(item)

        for venda in banco.listar_vendas():
            self.tabela_vendas.insert(
                "",
                tk.END,
                values=(
                    venda[0],
                    venda[1],
                    venda[2],
                    f"R$ {venda[3]:.2f}",
                    venda[4]
                )
            )

    def gerar_relatorio(self):
        inicio = self.data_inicio.get().strip()
        fim = self.data_fim.get().strip()

        try:
            data_inicio = date.fromisoformat(inicio)
            data_fim = date.fromisoformat(fim)

            if data_inicio > data_fim:
                raise ValueError

            relatorio = banco.relatorio_vendas(inicio, fim)

            texto = (
                f"PERÍODO: {inicio} até {fim}\n\n"
                f"Vendas concluídas: "
                f"{relatorio['vendas_concluidas']}\n"
                f"Vendas canceladas: "
                f"{relatorio['canceladas']}\n"
                f"Quantidade de itens vendidos: "
                f"{relatorio['quantidade_itens']}\n"
                f"Faturamento: "
                f"R$ {relatorio['faturamento']:.2f}\n"
                f"Ticket médio: "
                f"R$ {relatorio['ticket_medio']:.2f}\n\n"
                f"RESUMO POR FORMA DE PAGAMENTO\n"
            )

            for forma, total, quantidade in relatorio["pagamentos"]:
                texto += (
                    f"{forma}: {quantidade} venda(s) - "
                    f"R$ {total:.2f}\n"
                )

            texto += (
                "\nObservação: vendas faturadas são registradas "
                "como faturamento, mas não representam dinheiro "
                "recebido no caixa."
            )

            self.resumo_relatorio.delete("1.0", tk.END)
            self.resumo_relatorio.insert(tk.END, texto)

        except ValueError:
            messagebox.showerror(
                "Data inválida",
                "Informe datas válidas no formato AAAA-MM-DD "
                "e confira o período."
            )


    def _dados_para_exportacao(self):
        inicio = self.data_inicio.get().strip()
        fim = self.data_fim.get().strip()
        try:
            data_inicio = date.fromisoformat(inicio)
            data_fim = date.fromisoformat(fim)
            if data_inicio > data_fim:
                raise ValueError
            resumo = banco.relatorio_vendas(inicio, fim)
            vendas, itens = banco.vendas_periodo_exportacao(inicio, fim)
            return inicio, fim, resumo, vendas, itens
        except ValueError:
            messagebox.showerror(
                "Período inválido",
                "Informe datas válidas no formato AAAA-MM-DD e confira o período."
            )
            return None
        except Exception as erro:
            messagebox.showerror("Erro ao consultar dados", str(erro))
            return None

    def exportar_excel(self):
        dados = self._dados_para_exportacao()
        if dados is None:
            return
        inicio, fim, resumo, vendas, itens = dados

        caminho = filedialog.asksaveasfilename(
            title="Salvar relatório em Excel",
            defaultextension=".xlsx",
            filetypes=[("Arquivo Excel", "*.xlsx")],
            initialfile=f"relatorio_vendas_{inicio}_a_{fim}.xlsx"
        )
        if not caminho:
            return

        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment
            from openpyxl.utils import get_column_letter

            arquivo = Workbook()
            plan_resumo = arquivo.active
            plan_resumo.title = "Resumo"
            plan_resumo.append(["ELETRO VERA CRUZ - RELATÓRIO DE VENDAS"])
            plan_resumo.append(["Período", f"{inicio} até {fim}"])
            plan_resumo.append([])
            plan_resumo.append(["Indicador", "Resultado"])
            indicadores = [
                ("Vendas concluídas", resumo["vendas_concluidas"]),
                ("Vendas canceladas", resumo["canceladas"]),
                ("Quantidade de itens vendidos", resumo["quantidade_itens"]),
                ("Faturamento", resumo["faturamento"]),
                ("Ticket médio", resumo["ticket_medio"]),
            ]
            for linha in indicadores:
                plan_resumo.append(list(linha))
            plan_resumo.append([])
            plan_resumo.append(["Forma de pagamento", "Quantidade de vendas", "Total"])
            for forma, total, quantidade in resumo["pagamentos"]:
                plan_resumo.append([forma, quantidade, total])

            plan_vendas = arquivo.create_sheet("Vendas")
            plan_vendas.append(["Venda", "Data", "Pagamento", "Total", "Status"])
            for venda in vendas:
                plan_vendas.append(list(venda))

            plan_itens = arquivo.create_sheet("Itens")
            plan_itens.append([
                "Venda", "Data", "Pagamento", "Status", "Código", "Produto",
                "Marca", "Quantidade", "Valor unitário", "Subtotal"
            ])
            for item in itens:
                plan_itens.append(list(item))

            for plan in arquivo.worksheets:
                plan.freeze_panes = "A2"
                plan.auto_filter.ref = plan.dimensions
                for celula in plan[1]:
                    celula.font = Font(bold=True, color="FFFFFF")
                    celula.fill = PatternFill("solid", fgColor="244062")
                    celula.alignment = Alignment(horizontal="center")
                for coluna in plan.columns:
                    largura = max(
                        len(str(c.value)) if c.value is not None else 0
                        for c in coluna
                    )
                    plan.column_dimensions[get_column_letter(coluna[0].column)].width = min(largura + 3, 40)

            for linha in (8, 9):
                plan_resumo.cell(linha, 2).number_format = 'R$ #,##0.00'
            for linha in range(12, plan_resumo.max_row + 1):
                plan_resumo.cell(linha, 3).number_format = 'R$ #,##0.00'
            for linha in range(2, plan_vendas.max_row + 1):
                plan_vendas.cell(linha, 4).number_format = 'R$ #,##0.00'
            for linha in range(2, plan_itens.max_row + 1):
                plan_itens.cell(linha, 9).number_format = 'R$ #,##0.00'
                plan_itens.cell(linha, 10).number_format = 'R$ #,##0.00'

            arquivo.save(caminho)
            messagebox.showinfo("Exportação concluída", f"Relatório Excel salvo em:\n{caminho}")
        except ImportError:
            messagebox.showerror(
                "Dependência ausente",
                "Para exportar Excel, instale as bibliotecas com:\npip install -r requirements.txt"
            )
        except Exception as erro:
            messagebox.showerror("Erro ao exportar Excel", str(erro))

    def exportar_pdf(self):
        dados = self._dados_para_exportacao()
        if dados is None:
            return
        inicio, fim, resumo, vendas, itens = dados

        caminho = filedialog.asksaveasfilename(
            title="Salvar relatório em PDF",
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf")],
            initialfile=f"relatorio_vendas_{inicio}_a_{fim}.pdf"
        )
        if not caminho:
            return

        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import mm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

            documento = SimpleDocTemplate(
                caminho, pagesize=landscape(A4),
                rightMargin=12 * mm, leftMargin=12 * mm,
                topMargin=12 * mm, bottomMargin=12 * mm
            )
            estilos = getSampleStyleSheet()
            conteudo = [
                Paragraph("ELETRO VERA CRUZ", estilos["Title"]),
                Paragraph("Relatório de vendas", estilos["Heading2"]),
                Paragraph(f"Período: {inicio} até {fim}", estilos["Normal"]),
                Spacer(1, 6 * mm)
            ]

            dados_resumo = [
                ["Indicador", "Resultado"],
                ["Vendas concluídas", str(resumo["vendas_concluidas"])],
                ["Vendas canceladas", str(resumo["canceladas"])],
                ["Quantidade de itens", str(resumo["quantidade_itens"])],
                ["Faturamento", f"R$ {resumo['faturamento']:.2f}"],
                ["Ticket médio", f"R$ {resumo['ticket_medio']:.2f}"],
            ]
            tabela = Table(dados_resumo, colWidths=[65 * mm, 45 * mm])
            tabela.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#244062")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]))
            conteudo.extend([Paragraph("Resumo", estilos["Heading3"]), tabela, Spacer(1, 5 * mm)])

            pagamentos = [["Forma de pagamento", "Vendas", "Total"]]
            for forma, total, quantidade in resumo["pagamentos"]:
                pagamentos.append([forma, str(quantidade), f"R$ {total:.2f}"])
            tabela_pagamentos = Table(pagamentos, colWidths=[65 * mm, 35 * mm, 45 * mm])
            tabela_pagamentos.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#244062")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]))
            conteudo.extend([Paragraph("Formas de pagamento", estilos["Heading3"]), tabela_pagamentos, Spacer(1, 5 * mm)])

            tabela_vendas = [["Venda", "Data", "Pagamento", "Total", "Status"]]
            for venda in vendas:
                tabela_vendas.append([
                    str(venda[0]), str(venda[1]), str(venda[2]),
                    f"R$ {venda[3]:.2f}", str(venda[4])
                ])
            conteudo.append(Paragraph("Histórico de vendas", estilos["Heading3"]))
            tabela_historico = Table(tabela_vendas, repeatRows=1)
            tabela_historico.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#244062")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]))
            conteudo.append(tabela_historico)
            conteudo.append(Spacer(1, 5 * mm))
            conteudo.append(Paragraph(
                "Observação: o relatório considera vendas concluídas no faturamento; vendas canceladas são identificadas no histórico.",
                estilos["Italic"]
            ))
            documento.build(conteudo)
            messagebox.showinfo("Exportação concluída", f"Relatório PDF salvo em:\n{caminho}")
        except ImportError:
            messagebox.showerror(
                "Dependência ausente",
                "Para exportar PDF, instale as bibliotecas com:\npip install -r requirements.txt"
            )
        except Exception as erro:
            messagebox.showerror("Erro ao exportar PDF", str(erro))


if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaEstoque(janela)
    janela.mainloop()
