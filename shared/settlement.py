# shared/settlement.py
from shared.naming import formar_nome


class Assentamento:
    """
    Representa um assentamento (antigo 'província'), unidade básica de ocupação no mundo.
    Cada assentamento pertence a uma civilização e possui população, nome e localização.
    """

    def __init__(self, civilizacao, coordenadas):
        self.civilizacao = civilizacao
        self.coordenadas = coordenadas
        self.nome = formar_nome(civilizacao.cultura)

        # 👉 População inicial: 1 homem e 1 mulher por assentamento
        self.homens = 1
        self.mulheres = 1

    def get_populacao_total(self):
        """Retorna a população total do assentamento."""
        return self.homens + self.mulheres

    def aumentar_populacao(self):
        """
        Aplica crescimento populacional com base na população atual.
        Regra: taxa de crescimento base + bônus por população par.
        Distribuição de gênero tende a equilibrar.
        """
        populacao_atual = self.get_populacao_total()

        # Taxa base de crescimento
        taxa = 0.10
        # Bônus se população for par (estabilidade)
        if populacao_atual % 2 == 0:
            taxa += 0.05

        nascimentos = int(populacao_atual * taxa)
        if nascimentos < 1 and populacao_atual >= 2:
            nascimentos = 1  # Ao menos 1 nascimento se houver 2+ pessoas

        # Distribuição de gênero: tende a favorecer o gênero em menor número
        if self.homens < self.mulheres:
            homens_novos = (nascimentos + 1) // 2
            mulheres_novas = nascimentos // 2
        elif self.mulheres < self.homens:
            mulheres_novas = (nascimentos + 1) // 2
            homens_novos = nascimentos // 2
        else:
            mulheres_novas = (nascimentos + 1) // 2
            homens_novos = nascimentos // 2

        self.homens += homens_novos
        self.mulheres += mulheres_novas

    def __repr__(self):
        return (f"Assentamento({self.nome}, H={self.homens}, M={self.mulheres}, "
                f"Total={self.get_populacao_total()})")