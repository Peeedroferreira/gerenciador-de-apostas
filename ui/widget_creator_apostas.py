from database.db_manager import DBManager
from tkinter import ttk
from ui.formulario_nova_aposta import FormularioNovaAposta
import locale

def formatar_moeda(valor):
    return locale.currency(valor, symbol=True, grouping=True)

def create_widgets_apostas(master, tab, app):
    buttons_frame.pack(side='top', fill='x', padx=5, pady=5)

    # Botão para Nova Aposta
    ttk.Button(buttons_frame, text="Nova Aposta",
               command=lambda: FormularioNovaAposta(app, app.db_manager.listar_apostas_casas, app.db_manager)).grid(
        row=0, column=0, padx=5, pady=5)

    # Configuração do Treeview
    app.tree = ttk.Treeview(tab,
    columns = ("Casa de Aposta", "Valor Apostado", "Possível Retorno", "Resultado"),
    show = "headings")
    app.tree.pack(side='top', expand=True, fill='both', padx=10, pady=5)

    # Definindo os cabeçalhos
    app.tree.heading("Casa de Aposta", text="Casa de Aposta")
    app.tree.heading("Valor Apostado", text="Valor Apostado")
    app.tree.heading("Possível Retorno", text="Possível Retorno")
    app.tree.heading("Resultado", text="Resultado")

    # Configuração da largura das colunas (ajuste conforme necessário)
    app.tree.column("Casa de Aposta", width=150)
    app.tree.column("Valor Apostado", width=100)
    app.tree.column("Possível Retorno", width=100)
    app.tree.column("Resultado", width=100)

    apostas = app.db_manager.listar_apostas_casas()