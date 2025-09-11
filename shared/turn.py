# shared/turn.py
"""
Módulo: shared/turn.py
Responsável por gerenciar a lógica de cada turno do jogo.
Agora inclui:
1. Atualização da produtividade (geográfica)
2. Cálculo econômico por assentamento: produção, consumo, nutrição, estoque
3. Crescimento populacional
4. Registro de estatísticas

Futuramente: eventos, comércio, tecnologia, etc.
"""

import math


class Turno:
    def __init__(self):
        self.numero = 0  # Turno atual (0 = pré-jogo)
        self.historico = []  # Histórico de eventos por turno

    def avancar(self, mundo):
        """
        Avança um turno no mundo.
        Aplica:
        1. Atualização da produtividade dos assentamentos (bioma)
        2. Cálculo econômico local: produção, consumo, nutrição, estoque
        3. Crescimento populacional
        4. Registro de estatísticas

        :param mundo: Instância de Mundo
        """
        self.numero += 1
        total_nascimentos = 0

        # --- 1. ATUALIZAR PRODUTIVIDADE GEOGRÁFICA ---
        for civ in mundo.civs:
            for assentamento in civ.assentamentos:
                assentamento.atualizar_produtividade(mundo)

        # --- 2. CÁLCULO ECONÔMICO POR ASSENTAMENTO ---
        for civ in mundo.civs:
            for assentamento in civ.assentamentos:
                # Atualizar produção bruta (sem ajustes)
                producao_bruta = assentamento.get_producao_bruta()
                assentamento.producao_bruta = producao_bruta

                populacao = assentamento.get_populacao_total()

                # Se o assentamento está vazio, pula cálculos
                if populacao == 0:
                    assentamento.coef_nutricao = 1.0
                    continue

                # --- CÁLCULO DE NUTRIÇÃO BASEADO EM CONSUMO EFETIVO ---
                # x = consumo_efetivo / demanda, onde:
                # - demanda = população × taxa_consumo
                # - consumo_efetivo = min(planejado, disponível)
                # - coef_nutricao = sqrt(x), limitado entre 0.1 e 2.0

                demanda = populacao * assentamento.taxa_consumo
                consumo_planejado = demanda * assentamento.fator_consumo_local
                disponivel = producao_bruta + assentamento.estoque_alimentos
                consumo_efetivo = min(consumo_planejado, disponivel)
                x = consumo_efetivo / demanda if demanda > 0 else 0.0

                # Coeficiente de nutrição: y = sqrt(x)
                coef_nutricao = math.sqrt(x)
                assentamento.coef_nutricao = max(0.1, min(coef_nutricao, 2.0))  # [0.1, 2.0]

                # Atualizar estoque após consumo
                assentamento.estoque_alimentos = disponivel - consumo_efetivo

        # --- 3. CRESCIMENTO POPULACIONAL ---
        for civ in mundo.civs:
            for assentamento in civ.assentamentos:
                antes = assentamento.get_populacao_total()
                assentamento.aumentar_populacao()
                depois = assentamento.get_populacao_total()
                total_nascimentos += max(0, depois - antes)

        # --- 4. REGISTRAR NO HISTÓRICO ---
        populacao_total = mundo.get_populacao_global()[2]
        registro = {
            "turno": self.numero,
            "nascimentos": total_nascimentos,
            "populacao_total": populacao_total
        }
        self.historico.append(registro)

        # --- 5. LOG VISUAL ---
        print(f"\n--- Turno {self.numero} concluído ---")
        print(f"📊 +{total_nascimentos} nascimentos | População total: {populacao_total}")

    def resetar(self):
        """Reseta o contador de turnos (sem afetar o mundo)."""
        self.numero = 0
        self.historico.clear()
        print("🔁 Turnos resetados.")

    def get_ultimo_registro(self):
        """Retorna o último registro do histórico, ou None."""
        return self.historico[-1] if self.historico else None

    def __repr__(self):
        return f"<Turno {self.numero} | Histórico: {len(self.historico)} turnos>"