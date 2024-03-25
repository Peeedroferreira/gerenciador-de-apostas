from database.db_manager import DBManager


class BusinessLogic:
    def __init__(self):
        self.db_manager = DBManager()

    def calcular_e_atualizar_resultado_aposta(self, aposta_id):
        """Calcula o resultado de uma aposta específica e atualiza os saldos relevantes."""
        # Obter informações da aposta pelo ID
        aposta = self.db_manager.obter_aposta_por_id(aposta_id)

        # Supondo que 'aposta' é um dicionário com as informações necessárias
        valor_apostado = aposta['valor_aposta']
        odd = aposta['odd']
        resultado = aposta['resultado']
        bonus = aposta['bonus']
        casa_aposta_id = aposta['casa_aposta_id']

        if resultado == 'ganhou':
            lucro = valor_apostado * odd - valor_apostado + bonus
        else:
            lucro = -valor_apostado

        # Atualizar o saldo da casa de aposta
        self.atualizar_saldo_casa_aposta(casa_aposta_id, lucro)

        # Retorna o lucro (ou perda) final da aposta, incluindo o bônus
        return lucro

    def atualizar_saldo_casa_aposta(self, casa_aposta_id, valor):
        """Atualiza o saldo da casa de aposta após o resultado de uma aposta."""
        # Obter o saldo atual da casa de aposta
        casa_aposta = self.db_manager.obter_casa_aposta_por_id(casa_aposta_id)
        novo_saldo = casa_aposta['saldo'] + valor

        # Atualizar o saldo no banco de dados
        self.db_manager.atualizar_saldo_casa_aposta(casa_aposta_id, novo_saldo)

    def relatorio_lucros_perdas(self):
        """Gera um relatório do total de lucros e perdas, incluindo bônus."""
        apostas = self.db_manager.listar_apostas()
        total = sum(self.calcular_e_atualizar_resultado_aposta(aposta['id']) for aposta in apostas)
        return total
