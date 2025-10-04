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

    def calcular_multiplicador(self, alvo):
        """
        Calcula o multiplicador de dano contra outra unidade.
        Pode ser ajustado com base em parâmetros como velocidade, alcance, tipo, etc.
        """
        mult = 1.0
        mult += (self.alcance - alvo.alcance) * 0.05
        mult += (self.movimento - alvo.movimento) * 0.03
        mult += (self.ataque - alvo.defesa) * 0.02

        # Ajuste por tipo
        if self.tipo == 'Aéreo' and alvo.tipo == 'Terrestre':
            mult *= 1.2
        elif self.tipo == 'Terrestre' and alvo.tipo == 'Aéreo':
            mult *= 0.8
        elif self.tipo == 'Submarino' and alvo.tipo == 'Superfície':
            mult *= 1.3