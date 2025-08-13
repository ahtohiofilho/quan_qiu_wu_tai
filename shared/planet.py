import random
from shared.polygons import dicionario_poligonos
from shared.geography import definir_geografia

class Planeta:
    def __init__(self, fator, bioma):
        self.fator = fator
        self.bioma_inicial = bioma
        self.geografia, self.capitais_players = definir_geografia(dicionario_poligonos(fator), fator, bioma) # capitais = [(int, int), ...]
        random.shuffle(self.capitais_players)
        self.numero_de_jogadores = len(self.capitais_players)
        biomas_invalidos = {"Ice", "Sea", "Ocean", "Coast", bioma}
        capitais_player_set = set(self.capitais_players)
        nodos_validos = [
            n for n in self.geografia.nodes()
            if self.geografia.nodes[n]["bioma"] not in biomas_invalidos and n not in capitais_player_set
        ]
        npn = 27 - len(self.capitais_players)  # Lembrar de evitar npn (países neutros) negativo
        self.capitais_neutros = random.sample(nodos_validos, npn)
        random.shuffle(self.capitais_neutros)
        self.civilizacoes = []
