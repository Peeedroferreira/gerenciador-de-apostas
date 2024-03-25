import tkinter as tk
from ui.interface import ApostasApp
from database.db_manager import DBManager


def main():
    db_manager = DBManager()
    db_manager.criar_tabelas()

    # Inicializa a janela principal do Tkinter
    root = tk.Tk()
    # Define um tamanho inicial para a janela, se desejar
    root.geometry("800x600")

    # Cria a aplicação passando a janela principal como argumento
    app = ApostasApp(root)

    # Inicia o loop principal do Tkinter
    root.mainloop()


if __name__ == '__main__':
    main()
