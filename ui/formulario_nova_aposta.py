import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class FormularioNovaAposta(tk.Toplevel):
    def __init__(self, master, atualizar_callback, db_manager):
        super().__init__(master)
        self.atualizar_callback = atualizar_callback
        self.db_manager = db_manager
        self.title("Adicionar Nova Aposta")
        self.geometry("1200x600")  # Ajuste o tamanho conforme necessário
        self.resizable(False, False)

        self.casa_entries = []
        self.numero_de_casas = self.perguntar_numero_casas()
        if self.numero_de_casas:
            self.create_widgets()
        else:
            self.destroy()  # Fecha a janela se o usuário cancelar ou fechar a pergunta inicial

    def perguntar_numero_casas(self):
        return simpledialog.askinteger("Número de Casas",
                                       "Quantas casas de apostas serão usadas?",
                                       minvalue=1, maxvalue=4, parent=self)

    def create_widgets(self):
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, borderwidth=0)
        scrollable_frame = ttk.Frame(canvas)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Obter a lista de casas de apostas do banco de dados
        casas_apostas = self.db_manager.listar_nomes_casas_apostas()

        # Campo para o título da aposta
        ttk.Label(scrollable_frame, text="Título da Aposta:").grid(row=0, column=0, sticky='w', pady=2, padx=5)
        self.titulo_aposta_entry = ttk.Entry(scrollable_frame)
        self.titulo_aposta_entry.grid(row=0, column=1, sticky='ew', pady=2, padx=5)

        # Campo para a conta usada
        ttk.Label(scrollable_frame, text="Conta Usada:").grid(row=0, column=2, sticky='w', pady=2, padx=5)
        self.conta_usada_entry = ttk.Entry(scrollable_frame)
        self.conta_usada_entry.grid(row=0, column=3, sticky='ew', pady=2, padx=5)

        # Campo para o bônus
        ttk.Label(scrollable_frame, text="Bônus:").grid(row=0, column=4, sticky='w', pady=2, padx=5)
        self.bonus_entry = ttk.Entry(scrollable_frame)
        self.bonus_entry.grid(row=0, column=5, sticky='ew', pady=2, padx=5)

        # Campos variáveis para cada casa de apostas
        for i in range(1, self.numero_de_casas + 1):
            ttk.Label(scrollable_frame, text=f"Casa {i} Nome:").grid(row=i, column=0, sticky='w', pady=2, padx=5)

            # Use um Combobox para o campo de nome da casa
            casa_nome_entry = ttk.Combobox(scrollable_frame, values=casas_apostas)
            casa_nome_entry.grid(row=i, column=1, sticky='ew', pady=2, padx=5)

            ttk.Label(scrollable_frame, text="Odd:").grid(row=i, column=2, sticky='w', pady=2, padx=5)
            odd_entry = ttk.Entry(scrollable_frame)
            odd_entry.grid(row=i, column=3, sticky='ew', pady=2, padx=5)

            ttk.Label(scrollable_frame, text="Valor Aposta:").grid(row=i, column=4, sticky='w', pady=2, padx=5)
            valor_aposta_entry = ttk.Entry(scrollable_frame)
            valor_aposta_entry.grid(row=i, column=5, sticky='ew', pady=2, padx=5)

            # Adiciona os campos de entrada a uma lista para posterior recuperação
            self.casa_entries.append((casa_nome_entry, odd_entry, valor_aposta_entry))

        ttk.Button(self, text="Adicionar Aposta", command=self.adicionar_aposta).pack(pady=10)
    def adicionar_aposta(self):
        titulo = self.titulo_aposta_entry.get()
        if not titulo:
            messagebox.showerror("Erro", "Título da Aposta é obrigatório.")
            return

        # Inicializa o dicionário de argumentos
        args = {
            'titulo': titulo,
            'bonus': self.bonus_entry.get().replace(',', '.'),  # Pega o bônus do campo de bônus
            'conta_usada': self.casa_entries[0][1].get(),  # Pega a conta usada da primeira casa de aposta
        }

        for i, casa_entry in enumerate(self.casa_entries, start=1):
            casa_nome = casa_entry[0].get()
            odd = casa_entry[1].get().replace(',', '.')  # Substitui vírgulas por pontos
            valor_aposta = casa_entry[2].get().replace(',', '.')  # Substitui vírgulas por pontos

            if not casa_nome or not odd or not valor_aposta:
                messagebox.showerror("Erro", f"Campos para Casa {i} são obrigatórios.")
                return

            # Adiciona as informações da casa ao dicionário de argumentos
            args[f'casa_nome_{i}'] = casa_nome
            try:
                args[f'odd_{i}'] = float(odd)
            except ValueError:
                messagebox.showerror("Erro", f"Não foi possível converter odd_{i} para float. Valor inválido: {odd}")
                return
            try:
                args[f'valor_apostado_casa_{i}'] = float(valor_aposta)
            except ValueError:
                messagebox.showerror("Erro",
                                     f"Não foi possível converter valor_apostado_casa_{i} para float. Valor inválido: {valor_aposta}")
                return

        # Chama o método inserir_nova_aposta do db_manager com os argumentos
        if self.db_manager.inserir_nova_aposta(**args):
            # Se a aposta foi adicionada com sucesso, exibe uma mensagem de confirmação
            messagebox.showinfo("Sucesso", "Aposta adicionada com sucesso ao banco de dados!")
        # Chama o callback para atualizar a lista de apostas
        self.atualizar_callback()
       