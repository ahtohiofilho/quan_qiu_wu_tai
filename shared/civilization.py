# shared/civilization.py
import random
from shared.flags import bandeira
from shared.settlement import Assentamento


class Civilizacao:
    """
    Representa uma civilização no mundo.
    Possui nome, cultura, cor, bandeira, ponto inicial e uma lista de assentamentos.
    A produção total é a soma da produtividade de todos os assentamentos.
    """

    def __init__(self, ref, indice, nome, player=False, ponto_inicial=None, mundo=None, chamado_pelo_cliente=False):
        """
        :param ref: Instância de Referencias (culturas, cores, etc)
        :param indice: Índice para seleção de cultura e cor
        :param nome: Nome da civilização (ex: "Red", "Blue")
        :param player: Se é uma civilização controlada por jogador
        :param ponto_inicial: Coordenadas (q, r) do assentamento inicial
        :param mundo: Referência ao mundo (para consulta de pentágonos ou outros dados globais)
        :param chamado_pelo_cliente: Se True, bandeiras devem ser salvas em disco.
        """
        self.player = player
        self.nome = nome
        self.cultura = ref.culturas[indice % len(ref.culturas)]
        self.cor = ref.civs_cores[self.nome]
        self.modalidade_bandeira = random.randint(0, 82)

        # --- Modificação ---
        # Chama a função 'bandeira' passando o id_mundo se chamado_pelo_cliente for True
        if chamado_pelo_cliente and mundo and hasattr(mundo, 'id_mundo'):
            # Chamada modificada: passa o id_mundo do mundo criado
            from shared.flags import bandeira  # Importa localmente para evitar dependências circulares potenciais
            self.cores_bandeira = bandeira(self.nome, self.modalidade_bandeira, criar_arquivo=True,
                                           id_mundo=mundo.id_mundo)
        else:
            # Chamada original (não cria arquivo) ou quando chamado_pelo_cliente é False
            from shared.flags import bandeira  # Importa localmente
            self.cores_bandeira = bandeira(self.nome, self.modalidade_bandeira, criar_arquivo=False, id_mundo=None)
        # --- Fim da Modificação ---

        self.ponto_inicial = ponto_inicial
        self.assentamentos = []
        self.unidades = []
        self.eh_jogador_local = False
        self.mundo = mundo  # Para consulta de pentágonos ou outros dados globais

    def get_populacao_total(self):
        """Calcula a população total somando todos os assentamentos."""
        return sum(a.get_populacao_total() for a in self.assentamentos)

    def get_genero_counts(self):
        """Retorna o total de homens e mulheres na civilização."""
        homens = sum(a.homens for a in self.assentamentos)
        mulheres = sum(a.mulheres for a in self.assentamentos)
        return homens, mulheres

    def get_producao_total(self):
        """Retorna a produção total da civilização."""
        return sum(a.get_producao_real() for a in self.assentamentos)

    def __repr__(self):
        h, m = self.get_genero_counts()
        producao = self.get_producao_total()
        return (f"Civilização('{self.nome}', assentamentos={len(self.assentamentos)}, "
                f"Prod={producao:.1f}, H={h}, M={m}, Total={h + m})")