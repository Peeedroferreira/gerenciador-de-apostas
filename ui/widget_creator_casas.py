from tkinter import ttk
from ui.formularios import FormularioCasaAposta, FormularioDeposito, FormularioSaque

def create_widgets_casas(master, parent_frame, app):
    # Frame para os botões
    buttons_frame = ttk.Frame(parent_frame)
    buttons_frame.pack(side='top', fill='x', padx=5, pady=5)

    # Botão para Adicionar Casa de Aposta
    ttk.Button(buttons_frame, text="Adicionar Casa de Aposta",
               command=lambda: FormularioCasaAposta(master.root, app.db_manager.atualizar_lista_casas,
                                                    app.db_manager)).grid(
        row=0, column=0, padx=5, pady=5)

    # Botão para Depositar
    ttk.Button(buttons_frame, text="Depositar",
               command=lambda: FormularioDeposito(master.root, app.db_manager.atualizar_lista_casas,
                                                  app.db_manager)).grid(
        row=0, column=1, padx=5, pady=5)

    # Botão para Sacar
    ttk.Button(buttons_frame, text="Sacar",
               command=lambda: FormularioSaque(master.root, app.db_manager.atualizar_lista_casas, app.db_manager)).grid(
        row=0, column=2, padx=5, pady=5)

    # Configuração do Treeview
    app.tree = ttk.Treeview(parent_frame,
                            columns=("Casa de Aposta", "Saldo", "Total Apostado", "Lucro", "Prejuízo", "Comissão"),
                            show="headings")
    app.tree.pack(side='top', expand=True, fill='both', padx=10, pady=5)

    # Definindo os cabeçalhos
    app.tree.heading("Casa de Aposta", text="Casa de Aposta")
    app.tree.heading("Saldo", text="Saldo")
    app.tree.heading("Total Apostado", text="Total Apostado")
    app.tree.heading("Lucro", text="Lucro")
    app.tree.heading("Prejuízo", text="Prejuízo")
    app.tree.heading("Comissão", text="Comissão")

    # Buscar informações das casas de apostas
    casas_apostas = app.db_manager.listar_casas_apostas_com_total_apostado()

    # Inserir informações no Treeview
    for casa in casas_apostas:
        app.tree.insert('', 'end', values=casa)