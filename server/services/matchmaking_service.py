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

    def remover_jogador(self, username: str) -> bool:
        """Remove um jogador da sala. Retorna True se encontrado."""
        if username in self.jogadores:
            self.jogadores.remove(username)
            print(f"🗑️ Jogador '{username}' removido da sala de espera.")
            return True
        return False


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
        """Callback interno chamado quando uma sala enche. Garante limpeza completa do estado."""
        print(f"🔵 [DEBUG] MatchmakingService._on_partida_cheia: Início com {len(jogadores)} jogadores")

        # 1. Encontrar a sala associada aos jogadores
        sala = None
        with self.lock:
            for s in self.salas:
                # Comparar listas de jogadores (ordem pode variar, mas conteúdo deve ser igual)
                if set(s.jogadores) == set(jogadores):
                    sala = s
                    break

        if not sala:
            print("🟡 [DEBUG] MatchmakingService._on_partida_cheia: Sala não encontrada. Ignorando.")
            return

        print(f"🟢 [DEBUG] MatchmakingService._on_partida_cheia: Sala encontrada com mundo {sala.mundo.id_mundo}")

        # 2. Se encontrou a sala e ela tem um mundo, consuma-o
        if sala.mundo:
            sucesso = self.world_pool.consumir_mundo(sala.mundo.id_mundo)
            if sucesso:
                print(f"✅ Mundo {sala.mundo.id_mundo} consumido após partida iniciar.")
            else:
                print(f"⚠️ Falha ao consumir mundo {sala.mundo.id_mundo}")

        # 3. Notificar o cliente que a partida começou
        if self.partida_iniciada_callback:
            print("🟢 [DEBUG] MatchmakingService._on_partida_cheia: Notificando cliente: partida iniciada")
            self.partida_iniciada_callback(jogadores)
        else:
            print("🟡 [DEBUG] MatchmakingService._on_partida_cheia: Nenhum callback registrado para partida iniciada")

        # 4. Remover a sala da lista de salas ativas
        with self.lock:
            antes = len(self.salas)
            # Remover pela referência da sala, não pela lista de jogadores
            if sala in self.salas:
                self.salas.remove(sala)
                print(f"🗑️ [DEBUG] MatchmakingService._on_partida_cheia: Sala com mundo {sala.mundo.id_mundo} removida")
            else:
                print("🟡 [DEBUG] MatchmakingService._on_partida_cheia: Sala já foi removida")
            depois = len(self.salas)
            print(f"🟢 [DEBUG] MatchmakingService._on_partida_cheia: Salas ativas: {antes} → {depois}")

        print("🟢 [DEBUG] MatchmakingService._on_partida_cheia: Execução concluída")

    def entrar_na_fila(self, username: str) -> str:
        """
        1. Obtém um mundo com vaga do MundoPoolService.
        2. Associa o jogador a esse mundo (cria ou entra em sala).
        3. Registra ocupação no pool.

        NOTA: O mundo NÃO é consumido aqui. Ele só será consumido em `_on_partida_cheia`,
        quando a sala encher. Isso permite que múltiplos jogadores entrem no mesmo mundo.
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
                print(f"👥 {username} adicionado à sala existente do mundo {mundo.id_mundo}")
            else:
                # Criar nova sala para esse mundo
                nova_sala = SalaDeEspera(mundo=mundo, callback=self._on_partida_cheia)
                self.salas.append(nova_sala)
                mensagem = nova_sala.adicionar_jogador(username)
                print(f"🆕 Sala criada para o mundo {mundo.id_mundo}. {username} entrou.")

            # 3. Registrar no pool que o jogador ocupou uma vaga
            if "Erro" not in mensagem:
                self.world_pool.registrar_jogador_no_mundo(username, mundo)
                print(f"✅ {username} registrado no mundo {mundo.id_mundo}")

            # ❌ REMOVIDO: consumo prematuro do mundo
            # O mundo será consumido apenas quando a sala encher, em `_on_partida_cheia`
            # Isso permite que outros jogadores entrem no mesmo mundo

            print(mensagem)
            return mensagem

    def sair_da_fila(self, username: str) -> bool:
        """Remove o jogador da fila de qualquer sala. Remove a sala se ficar vazia."""
        with self.lock:
            for sala in self.salas:
                if sala.remover_jogador(username):
                    print(f"📤 {username} removido da sala {sala.mundo.id_mundo}")

                    # ✅ Remover do pool de jogadores do mundo
                    if sala.mundo.id_mundo in self.world_pool.jogadores_por_mundo:
                        if username in self.world_pool.jogadores_por_mundo[sala.mundo.id_mundo]:
                            self.world_pool.jogadores_por_mundo[sala.mundo.id_mundo].remove(username)
                            print(f"🧹 {username} removido de jogadores_por_mundo[{sala.mundo.id_mundo}]")

                    # ✅ Remover a sala se ficar vazia
                    if len(sala.jogadores) == 0:
                        self.salas.remove(sala)
                        print(f"🗑️ Sala com mundo {sala.mundo.id_mundo} removida (vazia)")
                    return True
            return False