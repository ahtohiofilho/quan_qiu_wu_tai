# server/services/queue_service.py
import threading

class FilaService:
    def __init__(self):
        self.fila = []
        self.lock = threading.Lock()
        self.partida_iniciada_callback = None  # Para notificar quando uma partida é formada

    def adicionar_jogador(self, username: str) -> bool:
        with self.lock:
            if username in self.fila:
                return False
            self.fila.append(username)
            print(f"📥 Jogador '{username}' adicionado à fila. Total: {len(self.fila)}")
            self._tentar_formar_partida()
            return True

    def remover_jogador(self, username: str):
        with self.lock:
            if username in self.fila:
                self.fila.remove(username)
                print(f"📤 Jogador '{username}' removido da fila.")

    def _tentar_formar_partida(self):
        """Quando tiver 4+ jogadores, inicia uma partida."""
        if len(self.fila) >= 4:
            partida = [self.fila.pop(0) for _ in range(4)]
            print(f"🎉 Partida iniciada com: {partida}")
            if self.partida_iniciada_callback:
                self.partida_iniciada_callback(partida)