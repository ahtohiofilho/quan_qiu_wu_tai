# server/services/world_pool.py
from typing import List, Optional, Dict
import threading
import time
from shared.world import Mundo
from server.manager import Gerenciador


class MundoPoolService:
    """
    Serviço ativo que mantém um número mínimo de mundos com vagas disponíveis.
    Reabastece automaticamente o pool quando necessário.
    """
    def __init__(
        self,
        gerenciador: Gerenciador,
        fator: int = 4,
        bioma: str = "Meadow",
        min_mundos: int = 3,        # ✅ Mínimo que queremos manter ativo
        max_mundos: int = 10,       # Limite total de mundos no sistema
        intervalo_verificacao: float = 5.0  # Tempo entre verificações (segundos)
    ):
        self.gerenciador = gerenciador
        self.fator = fator
        self.bioma = bioma
        self.min_mundos = min_mundos
        self.max_mundos = max_mundos
        self.intervalo_verificacao = intervalo_verificacao

        self.mundos_com_vaga: List[Mundo] = []  # Apenas mundos com pelo menos 1 vaga
        self.jogadores_por_mundo: Dict[str, List[str]] = {}  # id_mundo → [user1, ...]
        self.lock = threading.Lock()

        # Controle da thread de reabastecimento
        self._thread_reabastecimento = None
        self._parar_reabastecimento = threading.Event()

        # Inicializa o pool e inicia o serviço ativo
        self._inicializar_pool()
        self.iniciar_servico()

    def _inicializar_pool(self):
        """Cria os mundos iniciais para atingir min_mundos."""
        for _ in range(self.min_mundos):
            sucesso, mundo = self.gerenciador.criar_e_upload_mundo_com_retorno(
                fator=self.fator,
                bioma=self.bioma,
                bucket_name="global-arena-tiles",
                s3_prefix="planetas/"
            )
            if sucesso and mundo:
                with self.lock:
                    self.mundos_com_vaga.append(mundo)
                    self.jogadores_por_mundo[mundo.id_mundo] = []

    def iniciar_servico(self):
        """Inicia o loop de monitoramento e reabastecimento."""
        if self._thread_reabastecimento is None:
            self._parar_reabastecimento.clear()
            self._thread_reabastecimento = threading.Thread(target=self._loop_reabastecimento, daemon=True)
            self._thread_reabastecimento.start()
            print(f"✅ WorldPoolService: serviço ativo iniciado (min={self.min_mundos}, max={self.max_mundos})")

    def parar_servico(self):
        """Para o serviço de reabastecimento (para testes ou desligamento)."""
        if self._thread_reabastecimento is not None:
            self._parar_reabastecimento.set()
            self._thread_reabastecimento.join(timeout=2)
            print("🛑 WorldPoolService: serviço ativo parado.")

    def _loop_reabastecimento(self):
        """Loop contínuo que verifica e reabastece o pool."""
        while not self._parar_reabastecimento.is_set():
            self._parar_reabastecimento.wait(self.intervalo_verificacao)
            if self._parar_reabastecimento.is_set():
                break
            self._reabastecer()

    def _reabastecer(self):
        """Cria mundos até atingir min_mundos, respeitando max_mundos."""
        with self.lock:
            atual = len(self.mundos_com_vaga)
            if atual >= self.min_mundos:
                return  # Já temos o mínimo

            # Quantos mundos precisamos criar?
            a_criar = min(self.min_mundos - atual, self.max_mundos - len(self.mundos_com_vaga))
            for _ in range(a_criar):
                sucesso, mundo = self.gerenciador.criar_e_upload_mundo_com_retorno(
                    fator=self.fator,
                    bioma=self.bioma,
                    bucket_name="global-arena-tiles",
                    s3_prefix="planetas/"
                )
                if sucesso and mundo:
                    self.mundos_com_vaga.append(mundo)
                    self.jogadores_por_mundo[mundo.id_mundo] = []
                    print(f"🔄 Mundo {mundo.id_mundo} criado. Pool agora tem {len(self.mundos_com_vaga)} mundos com vaga.")
                else:
                    print("⚠️ Falha ao criar mundo durante reabastecimento.")
                    break

    def obter_mundo_com_vaga(self) -> Optional[Mundo]:
        """Retorna um mundo com vaga disponível, se houver."""
        with self.lock:
            for mundo in self.mundos_com_vaga:
                ocupadas = len(self.jogadores_por_mundo[mundo.id_mundo])
                if ocupadas < len(mundo.planeta.capitais_players):
                    return mundo
            return None

    def registrar_jogador_no_mundo(self, username: str, mundo: Mundo):
        """Registra um jogador em um mundo. Remove o mundo do pool se encher."""
        with self.lock:
            lista = self.jogadores_por_mundo[mundo.id_mundo]
            if username not in lista:
                lista.append(username)

            # Se o mundo encheu, remova do pool
            if len(lista) >= len(mundo.planeta.capitais_players):
                if mundo in self.mundos_com_vaga:
                    self.mundos_com_vaga.remove(mundo)
                    print(f"🗑️ Mundo {mundo.id_mundo} removido do pool (partida formada).")

    def quantidade_mundos_ativos(self) -> int:
        """Retorna quantos mundos ainda têm vagas disponíveis."""
        with self.lock:
            return len(self.mundos_com_vaga)

    def quantidade_vagas_totais(self) -> int:
        """Retorna o número total de vagas disponíveis no pool."""
        total = 0
        with self.lock:
            for mundo in self.mundos_com_vaga:
                ocupadas = len(self.jogadores_por_mundo[mundo.id_mundo])
                total += len(mundo.planeta.capitais_players) - ocupadas
        return total