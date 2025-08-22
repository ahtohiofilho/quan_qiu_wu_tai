# server/initializer.py
"""
Módulo para inicializar ou reinicializar a infraestrutura AWS:
- Cria/recria a tabela DynamoDB 'GlobalArena' com PK/SK.
- Limpa os dados no S3 nos prefixos usados.
- Garante que o bucket S3 exista.

Pode ser executado como script: python server/inicializador.py
"""

from botocore.exceptions import ClientError
from server.integrations.aws_loader import AWSLoader


class InicializadorAWS:
    def __init__(self, aws_loader: AWSLoader):
        self.aws_loader = aws_loader
        self.dynamodb = self.aws_loader.get_client('dynamodb')
        self.s3 = self.aws_loader.get_client('s3')
        self.bucket_name = "global-arena-tiles"
        self.region = aws_loader.region_name

    def inicializar(self, confirmar: bool = True):
        """
        Inicializa ou reinicializa toda a infraestrutura.
        :param confirmar: Se True, pede confirmação antes de apagar dados.
        """
        if confirmar:
            resposta = input(
                "⚠️  Isso apagará todos os mundos e metadados no S3 e DynamoDB.\n"
                "Deseja continuar? (s/N): "
            )
            if resposta.lower() not in ['s', 'sim', 'y', 'yes']:
                print("❌ Operação cancelada.")
                return False

        print("🔄 Inicializando infraestrutura AWS...")

        try:
            # 1. Garantir que o bucket S3 existe
            self._criar_bucket_se_nao_existir()

            # 2. Limpar dados no S3
            prefixos = ["planetas/", "saves/"]
            for prefix in prefixos:
                self._limpar_prefixo_s3(prefix)

            # 3. Recriar tabela DynamoDB (única: GlobalArena)
            self._recriar_tabela_globalarena()

            print("✅ Infraestrutura AWS reinicializada com sucesso!")
            return True

        except Exception as e:
            print(f"❌ Erro ao inicializar infraestrutura: {e}")
            return False

    def _criar_bucket_se_nao_existir(self):
        """Cria o bucket S3 se ele não existir."""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"ℹ️  Bucket S3 '{self.bucket_name}' já existe.")
        except ClientError:
            print(f"📦 Criando bucket S3 '{self.bucket_name}'...")
            try:
                if self.region == "us-east-1":
                    self.s3.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                print(f"✅ Bucket '{self.bucket_name}' criado com sucesso.")
            except ClientError as e:
                print(f"❌ Falha ao criar bucket: {e}")
                raise

    def _limpar_prefixo_s3(self, prefix: str):
        """Remove todos os objetos com o prefixo dado no S3."""
        print(f"🧹 Limpando S3: s3://{self.bucket_name}/{prefix}")
        paginator = self.s3.get_paginator('list_objects_v2')
        apagados = 0

        try:
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
            for page in pages:
                if 'Contents' not in page:
                    continue
                keys = [{'Key': obj['Key']} for obj in page['Contents']]
                if keys:
                    self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': keys})
                    apagados += len(keys)
            print(f"✅ {apagados} objetos apagados no prefixo '{prefix}'.")
        except ClientError as e:
            print(f"❌ Erro ao limpar S3 no prefixo '{prefix}': {e}")

    def _recriar_tabela_globalarena(self):
        """Deleta e recria a tabela GlobalArena com PK/SK."""
        table_name = "GlobalArena"
        try:
            print(f"🔍 Verificando tabela '{table_name}'...")
            self.dynamodb.describe_table(TableName=table_name)
            print(f"🗑️  Tabela '{table_name}' encontrada. Deletando...")
            self.dynamodb.delete_table(TableName=table_name)

            # Aguardar exclusão
            waiter = self.dynamodb.get_waiter('table_not_exists')
            waiter.wait(TableName=table_name, WaiterConfig={'Delay': 2, 'MaxAttempts': 30})
            print(f"✅ Tabela '{table_name}' deletada.")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceNotFoundException':
                raise e
            print(f"ℹ️  Tabela '{table_name}' não existe. Será criada.")

        # Criar tabela com PK/SK
        print(f"🆕 Criando tabela '{table_name}' com PK/SK...")
        try:
            self.dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {'AttributeName': 'PK', 'AttributeType': 'S'},
                    {'AttributeName': 'SK', 'AttributeType': 'S'}
                ],
                KeySchema=[
                    {'AttributeName': 'PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'SK', 'KeyType': 'RANGE'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )

            # Aguardar ativação
            waiter = self.dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=table_name, WaiterConfig={'Delay': 2, 'MaxAttempts': 30})
            print(f"✅ Tabela '{table_name}' criada e ativa.")
        except ClientError as e:
            print(f"❌ Falha ao criar tabela '{table_name}': {e}")
            raise


# ========================== CLI ==========================
if __name__ == "__main__":
    """
    Execução direta do módulo:
    $ python server/inicializador.py
    """
    print("🔧 Inicializador AWS - Reinicialização de Infraestrutura\n")

    # Cria o loader AWS
    try:
        aws_loader = AWSLoader()
        print(f"✅ Conectado à AWS (região: {aws_loader.region_name})")
    except Exception as e:
        print(f"❌ Falha ao conectar à AWS: {e}")
        exit(1)

    # Inicializa
    inicializador = InicializadorAWS(aws_loader)
    inicializador.inicializar(confirmar=True)