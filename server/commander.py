# server/commander.py
import queue
import threading
import time
import uuid
import random
from typing import Callable, Optional
from server.signals import WorkerSignals
from server.manager import Gerenciador
from server.initializer import InicializadorAWS


class Comando:
    def __init__(
        self,
        nome: str,
        callback: Callable,
        args=None,
        kwargs=None,
        on_success: Callable = None,
        on_error: Callable = None,
        signals: Optional[WorkerSignals] = None  # ✅ Novo: sinais PyQt6
    ):
        self.id = str(uuid.uuid4())[:8]
        self.nome = nome
        self.callback = callback
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.on_success = on_success  # ⚠️ Evite UI aqui
        self.on_error = on_error      # ⚠️ Evite UI aqui
        self.signals = signals        # ✅ Use para UI segura
        self.timestamp = time.time()

    def __repr__(self):
        return f"<Comando(id={self.id}, nome='{self.nome}')>"


class Comandante:
    """
    Orquestrador de operações de domínio.
    Deve ser usado pela interface gráfica para disparar ações assíncronas.
    Nunca deve conter lógica de UI.
    """
    def __init__(self, gerenciador: Gerenciador, aws_loader):
        self.gerenciador = gerenciador
        self.aws_loader = aws_loader
        self.fila = queue.Queue()
        self.ativo = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        # 🔁 Estado da simulação
        self.simulacao_ativa = False
        self.thread_simulacao: Optional[threading.Thread] = None

    def iniciar(self):
        """Inicia a thread de processamento de comandos."""
        self.thread.start()
        print("✅ Comandante iniciado. Pronto para executar comandos.")

    def parar(self, timeout: float = 2.0):
        """Para o loop de comandos de forma segura."""
        self.ativo = False
        while not self.fila.empty():
            try:
                self.fila.get_nowait()
            except queue.Empty:
                break
        self.thread.join(timeout=timeout)
        if self.thread.is_alive():
            print("⚠️ Thread do Comandante não encerrou a tempo.")
        else:
            print("🛑 Comandante parado com sucesso.")

    def _loop(self):
        """Loop principal: executa comandos da fila."""
        while self.ativo:
            try:
                comando = self.fila.get(timeout=0.2)
                print(f"⚙️ Executando [{comando.id}]: {comando.nome}")
                try:
                    resultado = comando.callback(*comando.args, **comando.kwargs)
                    print(f"✅ [{comando.id}] {comando.nome} concluído.")

                    # ✅ Primeiro: emitir sinais (seguro para UI)
                    if comando.signals:
                        comando.signals.success.emit(resultado)
                        comando.signals.finished.emit()

                    # ⚠️ Segundo: callbacks (cuidado! estão na thread secundária)
                    if comando.on_success:
                        try:
                            comando.on_success(resultado)
                        except Exception as cb_e:
                            print(f"⚠️ Erro no callback on_success: {cb_e}")

                except Exception as e:
                    print(f"❌ [{comando.id}] Erro em '{comando.nome}': {e}")

                    # ✅ Sinais de erro
                    if comando.signals:
                        comando.signals.error.emit(str(e))
                        comando.signals.finished.emit()

                    # ⚠️ Callbacks de erro
                    if comando.on_error:
                        try:
                            comando.on_error(str(e))
                        except Exception as cb_e:
                            print(f"⚠️ Erro no callback on_error: {cb_e}")

                finally:
                    self.fila.task_done()

            except queue.Empty:
                continue

    def _enviar_comando(self, nome: str, callback: Callable, *args, **kwargs):
        """
        Método auxiliar para criar e enviar um comando.
        Aceita on_success, on_error e signals nos kwargs.
        """
        on_success = kwargs.pop('on_success', None)
        on_error = kwargs.pop('on_error', None)
        signals = kwargs.pop('signals', None)  # ✅ Extrai os sinais

        comando = Comando(
            nome=nome,
            callback=callback,
            args=args,
            kwargs=kwargs,
            on_success=on_success,
            on_error=on_error,
            signals=signals  # ✅ Passa os sinais
        )
        self.fila.put(comando)

    # ————————————————————————————
    # Comandos de Domínio
    # ————————————————————————————

    def criar_e_upload_mundo(
        self,
        fator: int,
        bioma: str,
        bucket_name: str = "global-arena-tiles",
        s3_prefix: str = "planetas/",
        dynamodb_table_name: str = "GlobalArena",
        on_success: Callable = None,
        on_error: Callable = None,
        signals: Optional[WorkerSignals] = None  # ✅ Novo parâmetro
    ):
        """Comando: cria e faz upload de um novo mundo."""
        def task():
            sucesso, mundo = self.gerenciador.criar_e_upload_mundo_com_retorno(
                fator=fator,
                bioma=bioma,
                bucket_name=bucket_name,
                s3_prefix=s3_prefix,
                dynamodb_table_name=dynamodb_table_name
            )
            return sucesso, mundo

        self._enviar_comando(
            nome=f"Criar e Upload Mundo (fator={fator}, bioma={bioma})",
            callback=task,
            on_success=on_success,
            on_error=on_error,
            signals=signals  # ✅ Passa os sinais
        )

    def reinicializar_infra(
        self,
        confirmar: bool = False,
        on_success: Callable = None,
        on_error: Callable = None,
        signals: Optional[WorkerSignals] = None  # ✅ Novo parâmetro
    ):
        """Comando: reinicializa a infra AWS (S3 + DynamoDB)."""
        def task():
            inicializador = InicializadorAWS(self.aws_loader)
            sucesso = inicializador.inicializar(confirmar=confirmar)
            return sucesso

        self._enviar_comando(
            nome="Reinicializar Infra AWS",
            callback=task,
            on_success=on_success,
            on_error=on_error,
            signals=signals  # ✅ Passa os sinais
        )

    def testar_conexao_aws(
        self,
        on_success: Callable = None,
        on_error: Callable = None,
        signals: Optional[WorkerSignals] = None  # ✅ Novo parâmetro
    ):
        """Comando: testa conexão com AWS (conta, S3, DynamoDB)."""
        def task():
            try:
                account = self.aws_loader.get_account_info()
                buckets = self.aws_loader.list_s3_buckets()
                tables = self.aws_loader.list_dynamodb_tables()
                return {
                    'success': True,
                    'account': account,
                    'buckets': buckets,
                    'tables': tables
                }
            except Exception as e:
                raise e

        self._enviar_comando(
            nome="Testar Conexão AWS",
            callback=task,
            on_success=on_success,
            on_error=on_error,
            signals=signals  # ✅ Passa os sinais
        )

    def iniciar_simulacao_players(self, signals: Optional[WorkerSignals] = None):
        """Inicia a simulação de players online."""
        def task():
            if self.simulacao_ativa:
                return

            self.simulacao_ativa = True
            contador = 0

            def entrar_na_fila(usuario):
                nonlocal contador
                try:
                    import requests
                    response = requests.post("http://localhost:5000/auth/login", json=usuario)
                    if response.status_code == 200:
                        token = response.json().get("token")
                        headers = {"Authorization": f"Bearer {token}"} if token else {}
                        # ✅ Corrigido: agora envia o username
                        requests.post(
                            "http://localhost:5000/jogo/entrar",
                            json={"modo": "online", "username": usuario["username"]},
                            headers=headers
                        )
                        contador += 1
                        if signals:
                            signals.success.emit(f"✅ {usuario['username']} entrou na fila ({contador})")
                except Exception as e:
                    # ✅ Adicione log para depurar erros
                    print(f"❌ Erro ao processar {usuario['username']}: {e}")
                    if signals:
                        signals.error.emit(f"❌ Falha com {usuario['username']}")

            USUARIOS_SIMULADOS = [{"username": f"player{i:03d}", "password": "senha123"} for i in range(1, 51)]

            while self.simulacao_ativa:
                usuario = random.choice(USUARIOS_SIMULADOS)
                thread = threading.Thread(target=entrar_na_fila, args=(usuario,), daemon=True)
                thread.start()
                time.sleep(random.uniform(1.0, 3.0))

            if signals:
                signals.success.emit("🛑 Simulação encerrada.")

        self._enviar_comando(
            nome="Simular Players Online",
            callback=task,
            on_success=lambda msg: signals.success.emit(msg) if signals else None,
            on_error=lambda err: signals.error.emit(err) if signals else None,
            signals=signals
        )

    def parar_simulacao_players(self):
        """Para a simulação de players."""
        self.simulacao_ativa = False