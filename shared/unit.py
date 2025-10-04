class Unidade:
    def __init__(self, nome, ataque, defesa, vida, alcance, movimento, custo, tipo):
        self.nome = nome            # Nome da unidade
        self.ataque = ataque        # A
        self.defesa = defesa        # D
        self.vida = vida            # V
        self.alcance = alcance      # R
        self.movimento = movimento  # M
        self.custo = custo
        self.tipo = tipo            # 'Terrestre', 'Aéreo', 'Marítimo'