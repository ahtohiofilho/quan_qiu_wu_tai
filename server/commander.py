# server/commander.py
import queue
import threading
import time
import uuid
from typing import Callable, Optional

class Comando:
    def __init__(
        self,
        nome: str,
        callback: Callable,
        args=None,
        kwargs=None,
        on_success: Callable = None,
        on_error: Callable = None
    ):
        self.id = str(uuid.uuid4())[:8]
        self.nome = nome
        self.callback = callback
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.on_success = on_success
        self.on_error = on_error
        self.timestamp = time.time()

    def __repr__(self):
        return f"<Comando(id={self.id}, nome='{self.nome}')>"

class ServidorDeComandos:
    def __init__(self):
        self.fila = queue.Queue()
        self.ativo = True
        self.thread = threading.Thread(target=self._loop, daemon=True)

    def iniciar(self):
        self.thread.start()
        print("✅ Servidor de comandos iniciado.")

    def enviar(self, comando: Comando):
        self.fila.put(comando)

    def _loop(self):
        while self.ativo:
            try:
                comando = self.fila.get(timeout=0.2)
                print(f"⚙️ Executando [{comando.id}]: {comando.nome}")
                try:
                    resultado = comando.callback(*comando.args, **comando.kwargs)
                    print(f"✅ [{comando.id}] {comando.nome} concluído.")
                    if comando.on_success:
                        comando.on_success(resultado)
                except Exception as e:
                    print(f"❌ [{comando.id}] Erro em '{comando.nome}': {e}")
                    if comando.on_error:
                        comando.on_error(e)
                finally:
                    self.fila.task_done()
            except queue.Empty:
                continue

    def parar(self, timeout: float = 2.0):
        self.ativo = False
        while not self.fila.empty():
            try:
                self.fila.get_nowait()
            except queue.Empty:
                break
        self.thread.join(timeout=timeout)
        if self.thread.is_alive():
            print("⚠️ Thread do servidor de comandos não encerrou a tempo.")
        else:
            print("🛑 Servidor de comandos parado.")