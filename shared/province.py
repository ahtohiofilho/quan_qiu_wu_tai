from shared.naming import formar_nome

class Provincia:
    def __init__(self, civilizacao, coordenadas):
        self.civilizacao = civilizacao
        self.coordenadas = coordenadas
        self.nome = formar_nome(civilizacao.cultura)