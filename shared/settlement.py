# shared/settlement.py
from math import ceil
from shared.naming import formar_nome
from shared.economy import Economia


class Assentamento:
    """
    Representa um assentamento, unidade básica de ocupação no mundo.

    Cada assentamento ocupa uma parcela específica dentro de um tile:
    - Parcela central (índice 0)
    - Parcelas periféricas (1–5 em pentágonos, 1–6 em hexágonos)

    A produção real depende de:
    - Coeficiente do bioma (calculado por tile)
    - População (homens e mulheres)
    - Fator de gênero: homens = 4, mulheres = 2 (unidades de trabalho)
    """

    PARCELA_CENTRAL = 0

    def __init__(self, civilizacao, coordenadas, indice_parcela=None, eh_pentagono=False):
        """
        Inicializa um assentamento.

        :param civilizacao: Civilização dona do assentamento
        :param coordenadas: Coordenadas do tile (q, r) no grid hexagonal
        :param indice_parcela: Índice da parcela no tile (0 a 6, ou 0 a 5 se pentágono)
                               Se None, usa a parcela central (0)
        :param eh_pentagono: Se True, o tile é um pentágono (5 periféricos)
        """
        # --- DADOS BÁSICOS ---
        self.civilizacao = civilizacao
        self.coordenadas_tile = coordenadas
        self.eh_pentagono = eh_pentagono

        # Validar e definir índice da parcela
        max_parcelas = 5 if eh_pentagono else 6
        if indice_parcela is None:
            self.indice_parcela = self.PARCELA_CENTRAL
        else:
            if not (0 <= indice_parcela <= max_parcelas):
                raise ValueError(
                    f"Índice de parcela {indice_parcela} inválido para "
                    f"{'pentágono' if eh_pentagono else 'hexágono'} em {coordenadas}. "
                    f"Permitido: 0–{max_parcelas}"
                )
            self.indice_parcela = indice_parcela

        # Nome da cultura
        self.nome = formar_nome(civilizacao.cultura)

        # --- POPULAÇÃO INICIAL ---
        self.homens = 1
        self.mulheres = 1

        # --- PRODUTIVIDADE (GEOPRÓXIMA) ---
        self.coef_produtividade = 0.0  # Será calculado com base no bioma

        # --- ECONOMIA LOCAL ---
        self.estoque_alimentos = 0.0  # Alimentos armazenados localmente
        self.taxa_consumo = 1.0  # Demanda base: unidades por pessoa por turno
        self.fator_consumo_local = 1.0  # Multiplier: quanto % da demanda será consumido (0.0 a 1.5+)
        self.coef_nutricao = 1.0  # Calculado como sqrt(consumo_efetivo / demanda)
        self.producao_bruta = 0.0  # Cache: produção antes de ajuste por nutrição

        # --- PLACEHOLDERS FUTUROS (opcional) ---
        # self.armazenamento_maximo = 50.0  # Pode crescer com tecnologia
        # self.politica_local = "padrao"    # Ex: "racionamento", "abastecimento"

    def get_populacao_total(self):
        """Retorna a população total do assentamento."""
        return self.homens + self.mulheres

    def aumentar_populacao(self):
        """
        Aplica crescimento populacional:
        1. Mortalidade: 5% da população morre (arredondado para baixo: // 20)
        2. Nascimentos: 20% das mulheres geram filhos (arredondado para cima)
        3. Distribuição de gênero tende a equilibrar.
        """
        # --- 1. MORTALIDADE ---
        mortos_homens = self.homens // 20
        mortos_mulheres = self.mulheres // 20
        self.homens = max(0, self.homens - mortos_homens)
        self.mulheres = max(0, self.mulheres - mortos_mulheres)

        # Se extinto, não há crescimento
        if self.get_populacao_total() == 0:
            return

        # --- 2. NASCIMENTOS ---
        nascimentos = int(ceil(self.mulheres * 0.20))

        # --- 3. DISTRIBUIÇÃO DE GÊNERO ---
        if self.homens < self.mulheres:
            homens_novos = (nascimentos + 1) // 2
            mulheres_novas = nascimentos // 2
        elif self.mulheres < self.homens:
            mulheres_novas = (nascimentos + 1) // 2
            homens_novos = nascimentos // 2
        else:
            homens_novos = (nascimentos + 1) // 2
            mulheres_novas = nascimentos // 2

        self.homens += homens_novos
        self.mulheres += mulheres_novas

    def eh_parcela_central(self):
        """Verifica se o assentamento está na parcela central do tile."""
        return self.indice_parcela == self.PARCELA_CENTRAL

    def eh_parcela_periferica(self):
        """Verifica se o assentamento está em uma parcela periférica."""
        return self.indice_parcela >= 1

    def get_tipo_tile(self):
        """Retorna o tipo do tile: 'pentágono' ou 'hexágono'."""
        return "pentágono" if self.eh_pentagono else "hexágono"

    @staticmethod
    def calcular_produtividade_parcela(mundo, tile, indice_parcela, eh_pentagono=False):
        """
        Calcula o coeficiente de produção de uma parcela.
        - Central: produtividade do bioma do tile
        - Periférica: média entre bioma local e do vizinho na direção da parcela

        Usa a topologia real da geografia (grafo NetworkX) com direções explícitas.

        :param mundo: Instância de Mundo
        :param tile: Coordenadas (q, r) do tile
        :param indice_parcela: Índice da parcela (0 a 6)
        :param eh_pentagono: Se o tile é pentágono (opcional; detectado automaticamente)
        :return: float (0.0 a 6.0)
        """
        G = mundo.planeta.geografia
        prod_base = mundo.ref.produtividade_base

        # Bioma do tile atual
        try:
            bioma_local = G.nodes[tile]['bioma']
            prod_local = prod_base.get(bioma_local, 0.0)
        except KeyError:
            return 0.0

        # 1. Parcela central
        if indice_parcela == Assentamento.PARCELA_CENTRAL:
            return prod_local

        # 2. Detectar se é pentágono (se não foi passado)
        if eh_pentagono is False:
            grau = len(list(G.neighbors(tile)))
            eh_pentagono = (grau == 5)

        # 3. Obter vizinhos ordenados por direção
        vizinhos_com_direcao = []
        for vizinho in G.neighbors(tile):
            direcao = G[tile][vizinho].get('direcao')
            if direcao:
                vizinhos_com_direcao.append((direcao, vizinho))

        # Ordenar por direção alfabética (ex: N1, N2, ..., S1, S2, ...)
        vizinhos_com_direcao.sort(key=lambda x: x[0])
        vizinhos = [v for _, v in vizinhos_com_direcao]

        # 4. Verificar se o índice da parcela é válido
        max_parcelas = 5 if eh_pentagono else 6
        if indice_parcela > max_parcelas:
            return 0.0  # Inválido

        # Ajustar índice: parcelas periféricas 1–5/6 → índices 0–4/5 na lista
        idx_vizinho = (indice_parcela - 1) % len(vizinhos)  # Evita erro se houver menos vizinhos

        try:
            vizinho = vizinhos[idx_vizinho]
            bioma_vizinho = G.nodes[vizinho]['bioma']
            prod_vizinho = prod_base.get(bioma_vizinho, 0.0)
            return (prod_local + prod_vizinho) / 2.0
        except (IndexError, KeyError):
            return prod_local / 2.0  # Fallback seguro

    def atualizar_produtividade(self, mundo):
        """
        Atualiza o coeficiente de produtividade do assentamento com base no mundo atual.
        Chamado ao criar ou ao avançar turno.
        """
        self.coef_produtividade = self.calcular_produtividade_parcela(
            mundo,
            self.coordenadas_tile,
            self.indice_parcela,
            self.eh_pentagono
        )

    def get_producao_real(self):
        """
        Calcula a produção real do assentamento com base em:
        - Coeficiente de produtividade do bioma
        - População (homens e mulheres)
        - Coeficiente de nutrição local (afeta eficiência)
        - Coeficientes futuros (tecnologia, políticas)

        Fórmula:
            produção = coef_produtividade × coef_nutricao × trabalho_total
        """
        if self.coef_produtividade == 0.0:
            return 0.0

        # --- Trabalho ---
        trabalho_homens = self.homens * 4
        trabalho_mulheres = 0  # Padrão: mulheres são reprodutoras
        trabalho_total = trabalho_homens + trabalho_mulheres

        # --- Coeficientes econômicos locais ---
        # Já calculado no turno: self.coef_nutricao = sqrt((produção + estoque) / demanda)
        coef_nutricao = self.coef_nutricao

        # Futuro: pode vir de tecnologia, edifício ou política local
        coef_eficiencia_tecnica = 1.0

        # --- Cálculo final ---
        return self.coef_produtividade * coef_nutricao * coef_eficiencia_tecnica * trabalho_total

    def get_producao_bruta(self):
        """
        Produção sem ajustes (antes de aplicar nutrição ou eficiência).
        Usada para cálculo de consumo e exibição na UI.
        """
        if self.coef_produtividade == 0.0:
            return 0.0

        trabalho_homens = self.homens * 4
        trabalho_mulheres = 0
        trabalho_total = trabalho_homens + trabalho_mulheres

        return self.coef_produtividade * trabalho_total

    def __repr__(self):
        return (f"Assentamento({self.nome}, "
                f"Tile={self.coordenadas_tile}, "
                f"Parcela={self.indice_parcela}, "
                f"Tipo={self.get_tipo_tile()}, "
                f"Coef={self.coef_produtividade:.1f}, "
                f"Prod={self.get_producao_real():.1f} "
                f"(Bruta={self.producao_bruta:.1f}), "
                f"Nut={self.coef_nutricao:.2f}, "
                f"Estoque={self.estoque_alimentos:.1f}, "
                f"H={self.homens}, M={self.mulheres}, "
                f"Total={self.get_populacao_total()})")