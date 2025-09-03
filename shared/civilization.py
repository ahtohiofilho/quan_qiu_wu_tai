# shared/civilization.py
import random
from shared.flags import bandeira


class Civilizacao:
    def __init__(self, ref, indice, nome, player=False, ponto_inicial=None):
        self.player = player
        self.nome = nome
        self.cultura = ref.culturas[indice % len(ref.culturas)]
        self.cor = ref.civs_cores[self.nome]
        self.modalidade_bandeira = random.randint(0, 82)
        self.cores_bandeira = bandeira(self.nome, self.modalidade_bandeira)
        self.ponto_inicial = ponto_inicial
        self.provincias = []
        self.unidades = []
        self.eh_jogador_local = False

        # ❌ Removido: população agora é por província

    def get_populacao_total(self):
        """Calcula a população total somando todas as províncias."""
        return sum(p.get_populacao_total() for p in self.provincias)

    def get_genero_counts(self):
        """Retorna o total de homens e mulheres na civilização."""
        homens = sum(p.homens for p in self.provincias)
        mulheres = sum(p.mulheres for p in self.provincias)
        return homens, mulheres

    def __repr__(self):
        h, m = self.get_genero_counts()
        return (f"Civilização('{self.nome}', províncias={len(self.provincias)}, "
                f"H={h}, M={m}, Total={h + m})")