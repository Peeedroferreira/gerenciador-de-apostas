import tkinter as tk
from tkinter import messagebox, simpledialog
from database.db_manager import DBManager
from datetime import datetime


class FormularioCasaAposta(tk.Toplevel):
    def __init__(self, master, atualizar_callback, db_manager):
        super().__init__(master)
        self.atualizar_callback = atualizar_callback
        self.db_manager = db_manager
        self.title("Adicionar Casa de Aposta")
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self, text="Nome da Casa de Aposta:").pack(pady=(10, 0))
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack(pady=(0, 10))

        tk.Label(self, text="Saldo Inicial:").pack()
        self.saldo_entry = tk.Entry(self)
        self.saldo_entry.pack(pady=(0, 10))

        tk.Label(self, text="Comissão (%):").pack()
        self.comissao_entry = tk.Entry(self)
        self.comissao_entry.pack(pady=(0, 10))

        tk.Button(self, text="Adicionar", command=self.validar_e_adicionar_casa_aposta).pack()

    def validar_e_adicionar_casa_aposta(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome da casa de aposta é obrigatório.")
            return

        try:
            saldo = float(self.saldo_entry.get())
            comissao = float(self.comissao_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Saldo e comissão devem ser números válidos.")
            return

        self.adicionar_casa_aposta(nome, saldo, comissao)

    def adicionar_casa_aposta(self, nome, saldo, comissao):
        try:
            self.db_manager.inserir_casa_aposta(nome, saldo, comissao)
            messagebox.showinfo("Sucesso", "Casa de aposta adicionada com sucesso!")
            self.atualizar_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar a casa de aposta: {e}")

    def inserir_casa_aposta(self, nome, saldo, comissao):
        """Insere uma nova casa de aposta no banco de dados, incluindo a comissão."""
        cursor = self.conexao.cursor()
        comando_sql = '''
            INSERT INTO casas_apostas (nome, saldo, comissao)
            VALUES (?, ?, ?)
        '''
        try:
            cursor.execute(comando_sql, (nome, saldo, comissao))
            self.conexao.commit()
            print("Casa de aposta adicionada com sucesso.")
            self.apostas_app.atualizar_treeview()
        except Exception as e:
            print("Erro ao adicionar a casa de aposta:", e)
            self.conexao.rollback()
            self.db_manager.atualizar_treeview()

class FormularioDeposito(tk.Toplevel):
    def __init__(self, master, atualizar_callback, db_manager):
        super().__init__(master)
        self.atualizar_callback = atualizar_callback
        self.db_manager = db_manager
        self.title("Depósito em Casa de Aposta")

        # Obtém uma lista dos nomes das casas de apostas cadastradas
        casas_nomes = self.db_manager.listar_nomes_casas_apostas()

        tk.Label(self, text="Casa de Aposta:").pack(pady=(10, 0))
        self.casa_selecionada = tk.StringVar(self)
        if casas_nomes:  # Verifica se a lista não está vazia
            self.casa_selecionada.set(casas_nomes[0])  # Configura o valor padrão
        self.menu_casas = tk.OptionMenu(self, self.casa_selecionada, *casas_nomes)
        self.menu_casas.pack(pady=(0, 10))

        tk.Label(self, text="Valor do Depósito:").pack()
        self.valor_deposito_entry = tk.Entry(self)
        self.valor_deposito_entry.pack(pady=(0, 10))

        tk.Button(self, text="Depositar", command=self.efetuar_deposito).pack()

    def efetuar_deposito(self):
        casa_selecionada_nome = self.casa_selecionada.get()
        id_casa = self.db_manager.obter_id_por_nome_casa_aposta(casa_selecionada_nome)
        if id_casa is not None:
            valor_deposito = float(self.valor_deposito_entry.get())
            self.db_manager.depositar_em_casa_aposta(id_casa, valor_deposito)
            messagebox.showinfo("Sucesso", "Depósito realizado com sucesso!")
            self.atualizar_callback()
            self.db_manager.atualizar_treeview()
            self.destroy()
        else:
            messagebox.showerror("Erro", "Casa de aposta não encontrada.")

class FormularioSaque(tk.Toplevel):
    def __init__(self, master, atualizar_callback, db_manager):
        super().__init__(master)
        self.atualizar_callback = atualizar_callback
        self.db_manager = db_manager
        self.title("Saque de Casa de Aposta")

        # Obtém uma lista dos nomes das casas de apostas cadastradas
        casas_nomes = self.db_manager.listar_nomes_casas_apostas()

        tk.Label(self, text="Casa de Aposta:").pack(pady=(10, 0))
        self.casa_selecionada = tk.StringVar(self)
        if casas_nomes:  # Verifica se a lista não está vazia
            self.casa_selecionada.set(casas_nomes[0])  # Configura o valor padrão
        self.menu_casas = tk.OptionMenu(self, self.casa_selecionada, *casas_nomes)
        self.menu_casas.pack(pady=(0, 10))

        tk.Label(self, text="Valor do Saque:").pack()
        self.valor_saque_entry = tk.Entry(self)
        self.valor_saque_entry.pack(pady=(0, 10))

        tk.Button(self, text="Sacar", command=self.efetuar_saque).pack()

    def efetuar_saque(self):
        casa_selecionada_nome = self.casa_selecionada.get()
        id_casa = self.db_manager.obter_id_por_nome_casa_aposta(casa_selecionada_nome)
        if id_casa is not None:
            valor_saque = float(self.valor_saque_entry.get())
            if self.db_manager.sacar_de_casa_aposta(id_casa, valor_saque):
                messagebox.showinfo("Sucesso", "Saque realizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Saldo insuficiente para o saque.")
            self.atualizar_callback()
            self.db_manager.atualizar_treeview()
            self.destroy()
        else:
            messagebox.showerror("Erro", "Casa de aposta não encontrada.")