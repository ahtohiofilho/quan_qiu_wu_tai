# shared/settlement.py
from math import ceil
from shared.naming import formar_nome


class Assentamento:
    """
    Representa um assentamento, unidade básica de ocupação no mundo.

    Originalmente associado diretamente a um tile (coordenadas),
    agora pode representar uma parcela específica dentro de um tile:
    - Parcela central (índice 0)
    - Parcelas periféricas (1–5 em pentágonos, 1–6 em hexágonos)

    Para compatibilidade, se não for especificado, assume-se parcela central de um hexágono.
    """

    PARCELA_CENTRAL = 0
    PARCELAS_PERIFERICAS_HEXA = [1, 2, 3, 4, 5, 6]
    PARCELAS_PERIFERICAS_PENTA = [1, 2, 3, 4, 5]

    def __init__(self, civilizacao, coordenadas, indice_parcela=None, eh_pentagono=False):
        """
        Inicializa um assentamento.

        :param civilizacao: Civilização dona do assentamento
        :param coordenadas: Coordenadas do tile (q, r) no grid hexagonal
        :param indice_parcela: Índice da parcela no tile (0 a 6, ou 0 a 5 se pentágono)
                               Se None, usa a parcela central (0)
        :param eh_pentagono: Se True, o tile é um pentágono (5 periféricos)
        """
        self.civilizacao = civilizacao
        self.coordenadas_tile = coordenadas
        self.eh_pentagono = eh_pentagono

        # Definir número máximo de parcelas
        max_parcelas = 5 if eh_pentagono else 6

        # Se não especificado, usar parcela central
        if indice_parcela is None:
            self.indice_parcela = self.PARCELA_CENTRAL
        else:
            if indice_parcela < 0 or indice_parcela > max_parcelas:
                raise ValueError(
                    f"Índice de parcela {indice_parcela} inválido para "
                    f"{'pentágono' if eh_pentagono else 'hexágono'} em {coordenadas}. "
                    f"Permitido: 0–{max_parcelas}"
                )
            self.indice_parcela = indice_parcela

        # Nome da cultura
        self.nome = formar_nome(civilizacao.cultura)

        # População inicial: 1 homem, 1 mulher
        self.homens = 1
        self.mulheres = 1

    def get_populacao_total(self):
        """Retorna a população total do assentamento."""
        return self.homens + self.mulheres

    def aumentar_populacao(self):
        """
        Aplica:
        1. Mortalidade: 5% da população morre (arredondado para baixo: // 20)
        2. Nascimentos: 20% das mulheres geram filhos (arredondado para cima)
        3. Distribuição de gênero tende a equilibrar.
        """
        # --- 1. MORTALIDADE (5% de cada gênero, arredondado para baixo) ---
        mortos_homens = self.homens // 20
        mortos_mulheres = self.mulheres // 20

        self.homens = self.homens - mortos_homens
        self.mulheres = self.mulheres - mortos_mulheres

        # Se o assentamento foi extinto, não há crescimento
        if self.get_populacao_total() == 0:
            return

        # --- 2. NASCIMENTOS: 20% das mulheres (arredondado para cima) ---
        total_mulheres = self.mulheres
        nascimentos = int(ceil(total_mulheres * 0.20))

        # --- 3. DISTRIBUIÇÃO DE GÊNERO (tende a equilibrar) ---
        if self.homens < self.mulheres:
            homens_novos = (nascimentos + 1) // 2
            mulheres_novas = nascimentos // 2
        elif self.mulheres < self.homens:
            mulheres_novas = (nascimentos + 1) // 2
            homens_novos = nascimentos // 2
        else:
            homens_novos = (nascimentos + 1) // 2
            mulheres_novas = nascimentos // 2

        self.homens += homens_novos
        self.mulheres += mulheres_novas

    def eh_parcela_central(self):
        """Verifica se o assentamento está na parcela central do tile."""
        return self.indice_parcela == self.PARCELA_CENTRAL

    def eh_parcela_periferica(self):
        """Verifica se o assentamento está em uma parcela periférica."""
        return self.indice_parcela >= 1

    def get_tipo_tile(self):
        """Retorna o tipo do tile: 'pentágono' ou 'hexágono'."""
        return "pentágono" if self.eh_pentagono else "hexágono"

    def __repr__(self):
        return (f"Assentamento({self.nome}, Tile={self.coordenadas_tile}, "
                f"Parcela={self.indice_parcela}, Tipo={self.get_tipo_tile()}, "
                f"H={self.homens}, M={self.mulheres}, Total={self.get_populacao_total()})")