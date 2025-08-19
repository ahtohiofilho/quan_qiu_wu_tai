# server/services/queue_service.py

class FilaService:
    def __init__(self):
        self.fila = []

    def adicionar_jogador(self, username: str) -> bool:
        if username in self.fila:
            return False
        self.fila.append(username)
        print(f"📥 Jogador '{username}' adicionado à fila. Total: {len(self.fila)}")
        self._tentar_formar_partida()
        return True

    def remover_jogador(self, username: str):
        if username in self.fila:
            self.fila.remove(username)
            print(f"📤 Jogador '{username}' removido da fila.")

    def _tentar_formar_partida(self):
        """Quando tiver 4+ jogadores, inicia uma partida."""
        if len(self.fila) >= 4:
            partida = [self.fila.pop(0) for _ in range(4)]
            print(f"🎉 Partida iniciada com: {partida}")
            # Aqui você pode disparar um evento, sinalizar via WebSocket, etc.