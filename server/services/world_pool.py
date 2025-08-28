# server/services/world_pool.py
from typing import List, Optional, Dict
import threading
from shared.world import Mundo
from server.core.manager import Gerenciador


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

    def total_jogadores_na_fila(self) -> int:
        """Retorna o número total de jogadores já alocados nos mundos do pool."""
        total = 0
        with self.lock:
            for jogadores in self.jogadores_por_mundo.values():
                total += len(jogadores)
        return total

    def quantidade_total(self) -> int:
        """Retorna o número total de mundos com vagas disponíveis no pool."""
        return self.quantidade_mundos_ativos()

    def _inicializar_pool(self):
        """Inicializa o pool com mundos existentes e cria novos apenas se necessário."""
        print("🔄 Inicializando pool de mundos...")

        # Etapa 1: Carregar mundos existentes com vagas
        self._carregar_mundos_existentes()

        # Etapa 2: Contar quantos ainda precisamos criar
        with self.lock:
            atual = len(self.mundos_com_vaga)
        print(f"📦 {atual} mundos com vagas já carregados.")

        # Etapa 3: Criar apenas o necessário para atingir min_mundos
        a_criar = max(0, self.min_mundos - atual)
        print(f"🏗️  Criando {a_criar} novos mundos para atingir o mínimo ({self.min_mundos})...")

        for _ in range(a_criar):
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
                print(f"✅ Mundo {mundo.id_mundo} adicionado ao pool inicial.")
            else:
                print("⚠️ Falha ao criar mundo durante inicialização.")

    def iniciar_servico(self):
        """Inicia o loop de monitoramento e reabastecimento."""
        if self._thread_reabastecimento is None:
            self._parar_reabastecimento.clear()
            self._thread_reabastecimento = threading.Thread(target=self._loop_reabastecimento, daemon=True)
            self._thread_reabastecimento.start()
            print(f"✅ MundoPoolService: serviço ativo iniciado (min={self.min_mundos}, max={self.max_mundos})")

    def parar_servico(self):
        """Para o serviço de reabastecimento (para testes ou desligamento)."""
        if self._thread_reabastecimento is not None:
            self._parar_reabastecimento.set()
            self._thread_reabastecimento.join(timeout=2)
            print("🛑 MundoPoolService: serviço ativo parado.")

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

    def quantidade_vagas(self) -> int:
        """Retorna o número total de vagas disponíveis em todos os mundos do pool."""
        total = 0
        with self.lock:
            for mundo in self.mundos_com_vaga:
                ocupadas = len(self.jogadores_por_mundo.get(mundo.id_mundo, []))
                total += len(mundo.planeta.capitais_players) - ocupadas
        return total

    def _carregar_mundos_existentes(self):
        """Carrega mundos com vagas DO DynamoDB para o pool, mas apenas se estiverem 'disponiveis'."""
        try:
            dynamodb = self.gerenciador.aws_loader.get_client('dynamodb')
            response = dynamodb.scan(
                TableName=self.gerenciador.dynamodb_table_name,
                # ✅ Filtra por PK começando com PLANET#, com vagas > 0 E status = 'disponivel'
                FilterExpression="begins_with(PK, :pk_prefix) AND vagas > :zero AND #status = :ativo",
                ExpressionAttributeNames={
                    '#status': 'status'  # ✅ Protege contra palavras reservadas
                },
                ExpressionAttributeValues={
                    ':pk_prefix': {'S': 'PLANET#'},
                    ':zero': {'N': '0'},
                    ':ativo': {'S': 'disponivel'}  # ✅ Apenas mundos disponíveis
                }
            )

            with self.lock:
                for item in response.get('Items', []):
                    id_mundo = item['PK']['S'].split('#')[1]
                    vagas = int(item['vagas']['N'])
                    # ✅ Verifica novamente (embora o scan já tenha filtrado)
                    if vagas > 0:
                        # ✅ Evita duplicação
                        if not any(m.id_mundo == id_mundo for m in self.mundos_com_vaga):
                            mundo_stub = Mundo(fator=self.fator, bioma=self.bioma)
                            mundo_stub.id_mundo = id_mundo
                            self.mundos_com_vaga.append(mundo_stub)
                            self.jogadores_por_mundo[id_mundo] = []
                            print(f"🔁 Mundo carregado do DynamoDB: {id_mundo} ({vagas} vagas)")
        except Exception as e:
            print(f"⚠️ Falha ao carregar mundos existentes: {e}")
            import traceback
            traceback.print_exc()

    def consumir_mundo(self, id_mundo: str) -> Optional[Mundo]:
        """Remove um mundo do pool e marca como 'consumido' no DynamoDB."""
        with self.lock:
            # 1. Remover do pool local
            mundo = None
            for m in self.mundos_com_vaga:
                if m.id_mundo == id_mundo:
                    self.mundos_com_vaga.remove(m)
                    mundo = m
                    break
            if not mundo:
                print(f"⚠️ Mundo {id_mundo} não encontrado no pool para consumo.")
                return None

            print(f"🌍 Mundo {id_mundo} removido do pool (consumido).")

            # 2. Atualizar status no DynamoDB
            try:
                self.dynamodb.update_item(
                    TableName=self.dynamodb_table_name,
                    Key={
                        'PK': {'S': f'PLANET#{id_mundo}'},
                        'SK': {'S': 'METADATA'}
                    },
                    UpdateExpression="SET #status = :consumido",
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={':consumido': {'S': 'consumido'}}
                )
                print(f"✅ DynamoDB atualizado: mundo {id_mundo} marcado como 'consumido'.")
            except Exception as e:
                print(f"❌ Falha ao atualizar status do mundo {id_mundo} no DynamoDB: {e}")

            return mundo