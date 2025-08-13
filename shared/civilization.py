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