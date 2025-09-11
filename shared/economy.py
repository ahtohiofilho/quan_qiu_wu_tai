# shared/economy.py
import math

class Economia:
    """
    Módulo centralizado para cálculos econômicos de uma civilização.
    Responsabilidades:
    - Cálculo do coeficiente de nutrição
    - Gestão de produção, consumo e estoque
    - Aplicação de efeitos econômicos na produtividade
    """

    @staticmethod
    def calcular_producao_real(
            coef_produtividade: float,
            homens: int,
            mulheres: int,
            coef_nutricao: float = 1.0,
            coef_eficiencia_tecnica: float = 1.0,
            fator_mulheres: float = 0.0
    ) -> float:
        """
        Calcula a produção real com base em população, produtividade e coeficientes.
        """
        trabalho_homens = homens * 4
        trabalho_mulheres = mulheres * fator_mulheres
        trabalho_total = trabalho_homens + trabalho_mulheres

        return coef_produtividade * coef_nutricao * coef_eficiencia_tecnica * trabalho_total

    @staticmethod
    def calcular_coeficiente_nutricao(x: float) -> float:
        """
        Calcula o coeficiente de nutrição com base na razão oferta/demanda.
        Usa y = sqrt(x).
        """
        return math.sqrt(x)

    @staticmethod
    def calcular_demanda_alimentos(populacao: float, taxa_consumo: float) -> float:
        """Retorna a demanda total de alimentos."""
        return populacao * taxa_consumo

    @staticmethod
    def calcular_fluxo_alimentos(
        producao_bruta: float,
        estoque_atual: float,
        demanda: float
    ) -> dict:
        """
        Calcula consumo efetivo e novo estoque.
        Retorna um dicionário com os resultados.
        """
        disponivel = producao_bruta + estoque_atual
        consumo_efetivo = min(demanda, disponivel)
        novo_estoque = disponivel - consumo_efetivo
        razao_oferta_demanda = disponivel / demanda if demanda > 0 else 0.0

        return {
            "disponivel": disponivel,
            "demanda": demanda,
            "consumo": consumo_efetivo,
            "estoque_final": novo_estoque,
            "x": razao_oferta_demanda,
            "coef_nutricao": Economia.calcular_coeficiente_nutricao(razao_oferta_demanda)
        }