# server/services/matchmaking_service.py
from typing import List, Optional, Callable
import threading
from shared.world import Mundo
from server.services.world_pool import MundoPoolService  # ✅ Injeção de dependência

class SalaDeEspera:
    def __init__(self, mundo: Mundo, callback: Callable[[List[str]], None]):
        self.mundo = mundo
        self.vagas = len(mundo.planeta.capitais_players)  # ✅ Vagas definidas pelo mundo
        self.jogadores = []
        self.lock = threading.Lock()
        self.callback = callback

    def adicionar_jogador(self, username: str) -> str:
        with self.lock:
            if username in self.jogadores:
                return f"Erro ao entrar na fila: {username} já está na sala."
            if len(self.jogadores) >= self.vagas:
                return "Erro ao entrar na fila: sala cheia."

            self.jogadores.append(username)

            if len(self.jogadores) == self.vagas:
                self.callback(self.jogadores.copy())

            return f"{username} entrou na sala {self.mundo.id_mundo} ({len(self.jogadores)}/{self.vagas})"

    def esta_cheia(self) -> bool:
        with self.lock:
            return len(self.jogadores) >= self.vagas

    def tamanho(self) -> int:
        with self.lock:
            return len(self.jogadores)


class MatchmakingService:
    """
    Matchmaking baseado em MUNDOS PRÉ-CRIADOS fornecidos pelo MundoPoolService.
    O MatchmakingService não cria mundos — apenas aloca jogadores.
    """
    def __init__(self, world_pool: MundoPoolService):
        self.world_pool = world_pool
        self.salas: List[SalaDeEspera] = []  # Salas ativas com vagas
        self.lock = threading.Lock()
        self.partida_iniciada_callback: Optional[Callable[[List[str]], None]] = None

    def _on_partida_cheia(self, jogadores: List[str]):
        """Callback interno chamado quando uma sala enche."""
        if self.partida_iniciada_callback:
            self.partida_iniciada_callback(jogadores)

    def entrar_na_fila(self, username: str) -> str:
        """
        1. Obtém um mundo com vaga do MundoPoolService.
        2. Associa o jogador a esse mundo (cria ou entra em sala).
        3. Registra ocupação no pool.
        """
        with self.lock:
            # 1. Obter um mundo com vaga disponível
            mundo = self.world_pool.obter_mundo_com_vaga()
            if not mundo:
                return f"Erro ao entrar na fila: nenhum mundo disponível para {username}."

            # 2. Verificar se já existe uma sala para esse mundo
            sala_existente = next((s for s in self.salas if s.mundo.id_mundo == mundo.id_mundo), None)

            if sala_existente:
                mensagem = sala_existente.adicionar_jogador(username)
            else:
                # Criar nova sala para esse mundo
                nova_sala = SalaDeEspera(mundo=mundo, callback=self._on_partida_cheia)
                self.salas.append(nova_sala)
                mensagem = nova_sala.adicionar_jogador(username)

            # 3. Registrar no pool que o jogador ocupou uma vaga
            if "Erro" not in mensagem:
                self.world_pool.registrar_jogador_no_mundo(username, mundo)

            print(mensagem)
            return mensagem