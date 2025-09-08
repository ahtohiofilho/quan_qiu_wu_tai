# shared/civilization.py
import random
from shared.flags import bandeira
from shared.settlement import Assentamento


class Civilizacao:
    """
    Representa uma civilização no mundo.
    Possui nome, cultura, cor, bandeira, ponto inicial e uma lista de assentamentos.
    """

    def __init__(self, ref, indice, nome, player=False, ponto_inicial=None, mundo=None):
        """
        :param ref: Instância de Referencias (culturas, cores, etc)
        :param indice: Índice para seleção de cultura e cor
        :param nome: Nome da civilização (ex: "Red", "Blue")
        :param player: Se é uma civilização controlada por jogador
        :param ponto_inicial: Coordenadas (q, r) do assentamento inicial
        :param mundo: Referência ao mundo (para verificar se o tile é pentágono)
        """
        self.player = player
        self.nome = nome
        self.cultura = ref.culturas[indice % len(ref.culturas)]
        self.cor = ref.civs_cores[self.nome]
        self.modalidade_bandeira = random.randint(0, 82)
        self.cores_bandeira = bandeira(self.nome, self.modalidade_bandeira)
        self.ponto_inicial = ponto_inicial
        self.assentamentos = []
        self.unidades = []
        self.eh_jogador_local = False
        self.mundo = mundo  # Para consulta de pentágonos

    def get_populacao_total(self):
        """Calcula a população total somando todos os assentamentos."""
        return sum(a.get_populacao_total() for a in self.assentamentos)

    def get_genero_counts(self):
        """Retorna o total de homens e mulheres na civilização."""
        homens = sum(a.homens for a in self.assentamentos)
        mulheres = sum(a.mulheres for a in self.assentamentos)
        return homens, mulheres

    def __repr__(self):
        h, m = self.get_genero_counts()
        return (f"Civilização('{self.nome}', assentamentos={len(self.assentamentos)}, "
                f"H={h}, M={m}, Total={h + m})")