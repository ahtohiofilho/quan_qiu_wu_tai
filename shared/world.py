# shared/world.py
import random
from uuid import uuid4
from shared.references import Referencias
from shared.planet import Planeta
from shared.civilization import Civilizacao
from shared.settlement import Assentamento
from shared.turn import Turno


class Mundo:
    def __init__(self, fator=4, bioma='Meadow', id_mundo=None):
        self.id_mundo = id_mundo or str(uuid4())
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
            provincia = Assentamento(civ, civ.ponto_inicial)
            civ.provincias.append(provincia)

        # ✅ Inicializa o sistema de turnos
        self.turno = Turno()

        # ✅ Estado visual vinculado ao mundo (evita vazamento entre partidas)
        self.modo_renderizacao = "fisico"  # Pode ser "fisico" ou "politico"

    def get_populacao_global(self):
        """
        Retorna a população total do mundo.
        :return: (homens, mulheres, total)
        """
        homens = sum(p.homens for civ in self.civs for p in civ.provincias)
        mulheres = sum(p.mulheres for civ in self.civs for p in civ.provincias)
        total = homens + mulheres
        return homens, mulheres, total

    def __repr__(self):
        h, m, t = self.get_populacao_global()
        return (f"<Mundo(id={self.id_mundo}, turno={self.turno.numero}, "
                f"Civilizações={len(self.civs)}, População={t} → H={h}, M={m})>")