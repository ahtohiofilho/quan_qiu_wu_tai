import random
from shared.polygons import dicionario_poligonos
from shared.geography import definir_geografia

class Planeta:
    def __init__(self, fator, bioma):
        self.fator = fator
        self.bioma_inicial = bioma
        self.poligonos = dicionario_poligonos(fator)
        print(f"🌍 [DEBUG] Planeta criado: {len(self.poligonos)} polígonos")
        print(f"   Exemplo: chave={list(self.poligonos.keys())[0]}, shape={list(self.poligonos.values())[0].shape}")
        self.geografia, self.capitais_players = definir_geografia(self.poligonos, fator, bioma) # capitais = [(int, int), ...]
        if len(self.capitais_players) > 24:
            self.capitais_players = random.sample(self.capitais_players, 24)
        random.shuffle(self.capitais_players)
        self.numero_de_jogadores = len(self.capitais_players)
        biomas_invalidos = {"Ice", "Sea", "Ocean", "Coast", bioma}
        capitais_player_set = set(self.capitais_players)
        nodos_validos = [
            n for n in self.geografia.nodes()
            if self.geografia.nodes[n]["bioma"] not in biomas_invalidos and n not in capitais_player_set
        ]
        npn = 24 - len(self.capitais_players)  # Lembrar de evitar npn (países neutros) negativo
        npn = min(npn, len(nodos_validos))  # Garante que npn <= len(nodos_validos)
        print(f"🌍 [DEBUG] Planeta: {len(nodos_validos)} nodos válidos para capitais neutras, solicitados: {npn}")
        self.capitais_neutros = []
        if npn > 0:
            self.capitais_neutros = random.sample(nodos_validos, npn)
        random.shuffle(self.capitais_neutros)
        self.civilizacoes = []