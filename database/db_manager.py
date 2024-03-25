import sqlite3

class DBManager:
    def __init__(self):
        self.db_name = 'apostas.db'
        self.conexao = self.conectar_db()

    def conectar_db(self):
        """Cria uma conexão com o banco de dados SQLite."""
        return sqlite3.connect(self.db_name)

    def criar_tabelas(self):
        tabelas = [
            '''CREATE TABLE IF NOT EXISTS casas_apostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                saldo REAL DEFAULT 0,
                lucro REAL DEFAULT 0,
                prejuizo REAL DEFAULT 0,
                comissao REAL DEFAULT 0)''',
            '''CREATE TABLE IF NOT EXISTS apostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                conta_usada TEXT,
                bonus_id INTEGER,
                status TEXT,
                data_publicacao TEXT,
                prazo_bonus TEXT,
                valor_apostado_total REAL,
                prejuizo_somado REAL,
                lucro_final REAL,
                foto TEXT,
                FOREIGN KEY (bonus_id) REFERENCES bonus(id))''',
            '''CREATE TABLE IF NOT EXISTS apostas_casas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aposta_id INTEGER,
                titulo_aposta TEXT,
                bonus INTEGER,
                casa_nome TEXT,
                casa_nome_1 TEXT,
                casa_nome_2 TEXT,
                casa_nome_3 TEXT,
                casa_nome_4 TEXT,
                conta_usada TEXT,
                odd_1 REAL,
                odd_2 REAL,
                odd_3 REAL,
                odd_4 REAL,
                valor_apostado_casa_1 REAL, -- Alterado de valor_apostado_total para valor_apostado_casa_1
                valor_apostado_casa_2 REAL, -- Nova coluna para valor apostado na casa 2
                valor_apostado_casa_3 REAL, -- Alterado de valor_apostado_total para valor_apostado_casa_1
                valor_apostado_casa_4 REAL, -- Alterado de valor_apostado_total para valor_apostado_casa_1
                valor_apostado_total REAL,
                status TEXT,
                FOREIGN KEY (aposta_id) REFERENCES apostas(id))''',
            '''CREATE TABLE IF NOT EXISTS historico_depositos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                casa_aposta_id INTEGER,
                valor REAL,
                data_deposito TEXT,
                FOREIGN KEY (casa_aposta_id) REFERENCES casas_apostas(id))''',
            '''CREATE TABLE IF NOT EXISTS historico_saques (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                casa_aposta_id INTEGER,
                valor REAL,
                data_saque TEXT,
                FOREIGN KEY (casa_aposta_id) REFERENCES casas_apostas(id))''',
            '''CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                valor REAL,
                data_transacao TEXT,
                casa_aposta_id INTEGER,
                FOREIGN KEY (casa_aposta_id) REFERENCES casas_apostas(id))''',
            '''CREATE TABLE IF NOT EXISTS bonus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT,
                valor REAL,
                data_validade TEXT)'''
        ]
        for tabela in tabelas:
            cursor = self.conexao.cursor()
            cursor.execute(tabela)
        self.conexao.commit()

    def __del__(self):
        """Fecha a conexão com o banco de dados quando a instância é destruída."""
        self.conexao.close()

    def inserir_casa_aposta(self, nome, saldo, comissao):
        """Insere uma nova casa de apostas no banco de dados."""
        cursor = self.conexao.cursor()
        comando_sql = 'INSERT INTO casas_apostas (nome, saldo, comissao) VALUES (?, ?, ?)'
        cursor.execute(comando_sql, (nome, saldo, comissao))
        self.conexao.commit()

    def listar_casas_apostas_com_total_apostado(self):
        """Retorna informações das casas de apostas incluindo o total apostado."""
        cursor = self.conexao.cursor()
        comando_sql = """
        SELECT ca.nome, ca.saldo, SUM(ac.valor_apostado_total) AS total_apostado, ca.lucro, ca.prejuizo, ca.comissao
        FROM casas_apostas ca
        LEFT JOIN apostas_casas ac ON ca.nome = ac.casa_nome
        GROUP BY ca.nome, ca.saldo, ca.lucro, ca.prejuizo, ca.comissao
        ORDER BY ca.nome
        """
        cursor.execute(comando_sql)
        return cursor.fetchall()

    def inserir_aposta(self, casa_aposta_id, data_aposta, od, valor_aposta, resultado, bonus=0):
        """Insere uma nova aposta no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute(
            'INSERT INTO apostas (casa_aposta_id, data_aposta, od, valor_aposta, resultado, bonus) VALUES (?, ?, ?, ?, ?, ?)',
            (casa_aposta_id, data_aposta, od, valor_aposta, resultado, bonus))
        self.conexao.commit()

    def listar_apostas(self):
        """Retorna todas as apostas cadastradas no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM apostas')
        return cursor.fetchall()

    def listar_apostas_casas(self):
        """Retorna todas as apostas da tabela 'apostas_casas' no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM apostas_casas')
        return cursor.fetchall()
    def obter_aposta_por_id(self, aposta_id):
        """Retorna uma aposta específica pelo seu ID."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM apostas WHERE id = ?', (aposta_id,))
        return cursor.fetchone()

    def atualizar_saldo_casa_aposta(self, casa_aposta_id, novo_saldo):
        """Atualiza o saldo da casa de aposta com base no ID fornecido."""
        cursor = self.conexao.cursor()
        cursor.execute('UPDATE casas_apostas SET saldo = ? WHERE id = ?', (novo_saldo, casa_aposta_id))
        self.conexao.commit()

        # Funções para transações

    def inserir_transacao(self, tipo, valor, data_transacao, casa_aposta_id):
        """Insere uma nova transação no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO transacoes (tipo, valor, data_transacao, casa_aposta_id) VALUES (?, ?, ?, ?)',
                       (tipo, valor, data_transacao, casa_aposta_id))
        self.conexao.commit()

    def listar_transacoes(self):
        """Retorna todas as transações cadastradas no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM transacoes')
        return cursor.fetchall()

        # Funções para histórico de depósitos

    def listar_nomes_casas_apostas(self):
        """Retorna uma lista dos nomes das casas de apostas cadastradas no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT nome FROM casas_apostas')
        return [nome[0] for nome in cursor.fetchall()]

    def obter_id_por_nome_casa_aposta(self, nome_casa_aposta):
        """Retorna o ID de uma casa de aposta baseado no nome."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT id FROM casas_apostas WHERE nome = ?', (nome_casa_aposta,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    def depositar_em_casa_aposta(self, casa_aposta_id, valor_deposito):
        """Atualiza o saldo de uma casa de aposta com o valor do depósito."""
        cursor = self.conexao.cursor()
        # Primeiro, obtém o saldo atual
        cursor.execute('SELECT saldo FROM casas_apostas WHERE id = ?', (casa_aposta_id,))
        saldo_atual = cursor.fetchone()[0]

        # Atualiza o saldo com o valor do depósito
        novo_saldo = saldo_atual + valor_deposito
        cursor.execute('UPDATE casas_apostas SET saldo = ? WHERE id = ?', (novo_saldo, casa_aposta_id))
        self.conexao.commit()

    def sacar_de_casa_aposta(self, casa_aposta_id, valor_saque):
        """Atualiza o saldo de uma casa de aposta subtraindo o valor do saque."""
        cursor = self.conexao.cursor()
        # Primeiro, obtém o saldo atual
        cursor.execute('SELECT saldo FROM casas_apostas WHERE id = ?', (casa_aposta_id,))
        saldo_atual = cursor.fetchone()[0]

        # Verifica se o saldo é suficiente para o saque
        if saldo_atual >= valor_saque:
            # Atualiza o saldo subtraindo o valor do saque
            novo_saldo = saldo_atual - valor_saque
            cursor.execute('UPDATE casas_apostas SET saldo = ? WHERE id = ?', (novo_saldo, casa_aposta_id))
            self.conexao.commit()
            return True
        else:
            print("Saldo insuficiente para o saque.")
            return False

    def inserir_bonus(self, descricao, valor, data_validade):
        """Insere um novo bônus no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO bonus (descricao, valor, data_validade) VALUES (?, ?, ?)',
                       (descricao, valor, data_validade))
        self.conexao.commit()

    def listar_bonus(self):
        """Retorna todos os bônus cadastrados no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM bonus')
        return cursor.fetchall()

    def atualizar_treeview(self):
        # Limpa todos os itens existentes no Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Preenche o Treeview com os dados atualizados do banco de dados
        casas_apostas = self.db_manager.listar_casas_apostas_com_total_apostado()
        for casa in casas_apostas:
            self.tree.insert('', 'end', values=casa)

    def inserir_nova_aposta(self, titulo, bonus, conta_usada, bonus_id=None, status=None, data_publicacao=None,
                            prazo_bonus=None,
                            valor_apostado_total=None, prejuizo_somado=None, lucro_final=None, foto=None,
                            casa_nome_1=None, casa_nome_2=None, casa_nome_3=None, casa_nome_4=None,
                            odd_1=None, odd_2=None, odd_3=None, odd_4=None,
                            valor_apostado_casa_1=None, valor_apostado_casa_2=None,
                            valor_apostado_casa_3=None, valor_apostado_casa_4=None):
        """Insere uma nova aposta no banco de dados."""
        cursor = self.conexao.cursor()

        # Comando SQL para inserir na tabela 'apostas'
        comando_sql_apostas = '''
            INSERT INTO apostas
            (titulo, conta_usada, bonus_id, status, data_publicacao, prazo_bonus,
            valor_apostado_total, prejuizo_somado, lucro_final, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Valores para inserir na tabela 'apostas'
        valores_apostas = (
            titulo, conta_usada, bonus_id, status, data_publicacao, prazo_bonus,
            valor_apostado_total, prejuizo_somado, lucro_final, foto
        )

        # Comando SQL para inserir na tabela 'apostas_casas'
        comando_sql_apostas_casas = '''
            INSERT INTO apostas_casas
            (aposta_id, titulo_aposta, bonus, casa_nome_1, casa_nome_2, casa_nome_3, casa_nome_4,
            conta_usada, odd_1, odd_2, odd_3, odd_4,
            valor_apostado_casa_1, valor_apostado_casa_2,
            valor_apostado_casa_3, valor_apostado_casa_4, valor_apostado_total, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Valores para inserir na tabela 'apostas_casas'
        valores_apostas_casas = (
            None, titulo, bonus, casa_nome_1, casa_nome_2, casa_nome_3, casa_nome_4,
            conta_usada,
            odd_1, odd_2, odd_3, odd_4,
            valor_apostado_casa_1, valor_apostado_casa_2,
            valor_apostado_casa_3, valor_apostado_casa_4, valor_apostado_total, status
        )

        # Executando os comandos SQL
        try:
            # Inserir na tabela 'apostas' e obter o id da nova aposta inserida
            cursor.execute(comando_sql_apostas, valores_apostas)
            nova_aposta_id = cursor.lastrowid

            # Atualizar valores para inserir na tabela 'apostas_casas' com o novo id da aposta
            valores_apostas_casas = (
                nova_aposta_id, *valores_apostas_casas[1:]
            )

            # Inserir na tabela 'apostas_casas'
            cursor.execute(comando_sql_apostas_casas, valores_apostas_casas)

            # Commit das transações
            self.conexao.commit()
            print("Aposta e detalhes das casas adicionados com sucesso.")
            return True
        except Exception as e:
            print("Erro ao adicionar a aposta e detalhes das casas:", e)
            self.conexao.rollback()
            return False

    def atualizar_lista_casas(self):
        """Updates the list of betting houses."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM casas_apostas')
        return cursor.fetchall()

    def listar_apostas_casas(self):
        """Retorna todas as apostas da tabela 'apostas_casas' no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM apostas_casas')
        return cursor.fetchall()


    def __del__(self):
        """Fecha a conexão com o banco de dados quando a instância é destruída."""
        self.conexao.close()
