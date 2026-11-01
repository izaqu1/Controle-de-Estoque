import tkinter as tk
from tkinter import messagebox

from interface import SistemaEstoque


def iniciar_sistema():
    janela = tk.Tk()

    try:
        app = SistemaEstoque(janela)
        janela.mainloop()

    except Exception as erro:
        messagebox.showerror(
            "Erro ao iniciar o sistema",
            f"Não foi possível iniciar o sistema:\n\n{erro}"
        )
        janela.destroy()


if __name__ == "__main__":
    iniciar_sistema()