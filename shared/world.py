# shared/world.py
import random
from uuid import uuid4
from shared.references import Referencias
from shared.planet import Planeta
from shared.civilization import Civilizacao
from shared.province import Provincia


class Mundo:
    def __init__(self, fator=4, bioma='Meadow'):
        self.id_mundo = str(uuid4())
        ref = Referencias()
        random.shuffle(ref.culturas)
        lista_de_cores = list(ref.civs_cores.keys())
        random.shuffle(lista_de_cores)
        self.planeta = Planeta(fator=fator, bioma=bioma)
        self.civs = []

        # Criar civilizações com capitais corretas
        for i, capital in enumerate(self.planeta.capitais_players):
            nome = lista_de_cores[i % len(lista_de_cores)]
            civ = Civilizacao(ref, i, nome, True, capital)
            self.civs.append(civ)

        for i, capital in enumerate(self.planeta.capitais_neutros):
            indice = i + len(self.planeta.capitais_players)
            nome = lista_de_cores[indice % len(lista_de_cores)]
            civ = Civilizacao(ref, indice, nome, False, capital)
            self.civs.append(civ)

        # Atribuir província inicial usando o ponto_inicial de cada civ
        for civ in self.civs:
            provincia = Provincia(civ, civ.ponto_inicial)
            civ.provincias.append(provincia)