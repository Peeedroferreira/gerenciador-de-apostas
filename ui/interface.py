from ui.widget_creator_casas import create_widgets_casas
from database.db_manager import DBManager
from tkinter import ttk
class ApostasApp:
    def __init__(self, root):
        self.root = root
        self.db_manager = DBManager()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Gerenciador de Apostas")

        # Tab Control
        tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Casas de Apostas')
        tab_control.add(self.tab2, text='Apostas')
        tab_control.pack(expand=1, fill="both")

        # Chama a função create_widgets_casas
        create_widgets_casas(self, self.tab1, self)

        # Botão para Atualizar Informações
        ttk.Button(self.root, text="Atualizar Informações", command=self.atualizar_tudo).pack(pady=10)


    def atualizar_tudo(self):
        # Aqui você precisa adicionar a lógica para atualizar as informações
        print("Informações atualizadas")

if __name__ == "__main__":
    root = tk.Tk()
    app = ApostasApp(root)
    root.geometry("600x400")  # Define um tamanho inicial para a janela
    root.mainloop()