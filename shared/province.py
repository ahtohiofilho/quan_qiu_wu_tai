# shared/province.py
from shared.naming import formar_nome


class Provincia:
    def __init__(self, civilizacao, coordenadas):
        self.civilizacao = civilizacao
        self.coordenadas = coordenadas
        self.nome = formar_nome(civilizacao.cultura)

        # 👉 População inicial: 1 homem e 1 mulher por província
        self.homens = 1
        self.mulheres = 1

    def get_populacao_total(self):
        """Retorna a população total da província."""
        return self.homens + self.mulheres

    def aumentar_populacao(self):
        """
        Aumenta a população da província com base no número de mulheres.
        Regra: nascimentos = número de mulheres na província.
        Distribuição:
        - O gênero menos numeroso recebe o extra em caso de ímpar.
        - Se iguais, mulheres têm preferência.
        """
        nascimentos = self.mulheres
        if nascimentos == 0:
            return

        if self.homens < self.mulheres:
            # Homens são minoria → recebem a maioria
            homens_novos = (nascimentos + 1) // 2
            mulheres_novas = nascimentos // 2
        elif self.mulheres < self.homens:
            # Mulheres são minoria → recebem a maioria
            mulheres_novas = (nascimentos + 1) // 2
            homens_novos = nascimentos // 2
        else:
            # Quantidades iguais → mulheres levam o extra
            mulheres_novas = (nascimentos + 1) // 2
            homens_novos = nascimentos // 2

        self.homens += homens_novos
        self.mulheres += mulheres_novas

    def __repr__(self):
        return (f"Provincia({self.nome}, H={self.homens}, M={self.mulheres}, "
                f"Total={self.get_populacao_total()})")