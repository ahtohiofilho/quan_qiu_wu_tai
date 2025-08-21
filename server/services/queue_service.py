# server/services/queue_service.py
"""
Serviço de fila de espera para matchmaking online.
Gerencia a entrada de jogadores e formação de partidas quando há 4+ jogadores.
"""

import threading
from typing import Optional, Callable


class FilaService:
    """
    Serviço responsável por gerenciar a fila de jogadores online.
    Forma partidas automaticamente quando 4 jogadores estão na fila.
    """

    def __init__(self):
        self.fila = []
        self.lock = threading.Lock()
        self.partida_iniciada_callback: Optional[Callable[[list], None]] = None

    def adicionar_jogador(self, username: str) -> bool:
        with self.lock:
            if username in self.fila:
                print(f"⚠️ '{username}' já está na fila. Bloqueado.")
                return False
            self.fila.append(username)
            print(f"📥 Jogador '{username}' adicionado à fila. Total: {len(self.fila)}")
            self._tentar_formar_partida()
            return True

    def remover_jogador(self, username: str):
        """
        Remove um jogador da fila, se estiver presente.
        """
        with self.lock:
            if username in self.fila:
                self.fila.remove(username)
                print(f"📤 Jogador '{username}' removido da fila.")

    def _tentar_formar_partida(self):
        with self.lock:
            print(f"🔍 Verificando formação de partida. Fila atual: {self.fila} (total: {len(self.fila)})")  # ← Novo log
            if len(self.fila) >= 4:
                partida = [self.fila.pop(0) for _ in range(4)]
                print(f"🎉 Partida formada com: {partida}")
                if self.partida_iniciada_callback:
                    try:
                        self.partida_iniciada_callback(partida)
                    except Exception as e:
                        print(f"❌ Erro ao executar partida_iniciada_callback: {e}")
                else:
                    print("ℹ️ Nenhum callback configurado.")