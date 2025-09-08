# shared/world.py
import random
from uuid import uuid4
from shared.references import Referencias
from shared.planet import Planeta
from shared.civilization import Civilizacao
from shared.settlement import Assentamento
from shared.turn import Turno


class Mundo:
    """
    Representa o estado completo do mundo no jogo.
    Inclui:
    - Planeta (geografia, biomas, polígonos)
    - Civilizações e seus assentamentos
    - Sistema de turnos
    - Estado de renderização (físico ou político)
    """

    def __init__(self, fator=4, bioma='Meadow', id_mundo=None):
        self.id_mundo = id_mundo or str(uuid4())
        self.ref = Referencias()
        random.shuffle(self.ref.culturas)
        lista_de_cores = list(self.ref.civs_cores.keys())
        random.shuffle(lista_de_cores)

        # Criar o planeta com base no fator e bioma
        self.planeta = Planeta(fator=fator, bioma=bioma)

        # Lista de civilizações
        self.civs = []

        # Identificar os 12 pentágonos do poliedro de Goldberg
        self.pentagonos = self._identificar_pentagonos()

        # Criar civilizações com capitais corretas
        for i, capital in enumerate(self.planeta.capitais_players):
            nome = lista_de_cores[i % len(lista_de_cores)]
            civ = Civilizacao(self.ref, i, nome, True, capital, mundo=self)
            self.civs.append(civ)

        for i, capital in enumerate(self.planeta.capitais_neutros):
            indice = i + len(self.planeta.capitais_players)
            nome = lista_de_cores[indice % len(lista_de_cores)]
            civ = Civilizacao(self.ref, indice, nome, False, capital, mundo=self)
            self.civs.append(civ)

        # Criar assentamento inicial para cada civilização
        for civ in self.civs:
            eh_pentagono = civ.ponto_inicial in self.pentagonos
            assentamento_inicial = Assentamento(
                civilizacao=civ,
                coordenadas=civ.ponto_inicial,
                indice_parcela=Assentamento.PARCELA_CENTRAL,
                eh_pentagono=eh_pentagono
            )
            # 🔥 Atualiza a produtividade com base no mundo
            assentamento_inicial.atualizar_produtividade(self)
            civ.assentamentos.append(assentamento_inicial)

        # ✅ Inicializa o sistema de turnos
        self.turno = Turno()

        # ✅ Estado visual vinculado ao mundo
        self.modo_renderizacao = "fisico"  # Pode ser "fisico" ou "politico"

    def _identificar_pentagonos(self):
        """
        Retorna um conjunto com as coordenadas dos 12 pentágonos.
        Baseado na topologia do icosaedro subdividido: são os tiles com grau 5.
        """
        G = self.planeta.geografia
        pentagonos = {node for node in G.nodes if len(list(G.neighbors(node))) == 5}
        if len(pentagonos) != 12:
            # Fallback: usar os 12 menores graus (heurística)
            graus = sorted(G.nodes, key=lambda n: len(list(G.neighbors(n))))
            pentagonos = set(graus[:12])
        return pentagonos

    def get_populacao_global(self):
        """
        Retorna a população total do mundo.
        :return: (homens, mulheres, total)
        """
        homens = sum(a.homens for civ in self.civs for a in civ.assentamentos)
        mulheres = sum(a.mulheres for civ in self.civs for a in civ.assentamentos)
        total = homens + mulheres
        return homens, mulheres, total

    def __repr__(self):
        h, m, t = self.get_populacao_global()
        return (f"<Mundo(id={self.id_mundo}, turno={self.turno.numero}, "
                f"Civilizações={len(self.civs)}, População={t} → H={h}, M={m})>")