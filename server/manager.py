# server/manager.py
import json
import time
from pathlib import Path
from typing import Optional, Tuple

from server.serialization import Serializador
from server.aws_loader import AWSLoader
from shared.world import Mundo


class Gerenciador:
    """
    Gerencia operações de mundo: criação, serialização, upload S3 e salvamento de metadados no DynamoDB.
    Nada é salvo localmente.
    """

    def __init__(self, aws_loader: AWSLoader, save_dir: str = "saves"):
        self.aws_loader = aws_loader
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)  # Mantido para compatibilidade futura

    # server/manager.py

    def upload_mundo(self,
                     mundo: Mundo,
                     bucket_name: str = "global-arena-tiles",
                     s3_prefix: str = "planetas/",
                     dynamodb_table_name: str = "GlobalArena") -> bool:
        """
        Faz upload do mundo: dados pesados para S3, metadados leves para DynamoDB.
        Agora com rollback se falhar no DynamoDB.
        """
        try:
            pk = f"PLANET#{mundo.id_mundo}"
            sk = "METADATA"
            s3_key = f"{s3_prefix}{mundo.id_mundo}.json"

            # --- Verificar se já existe no DynamoDB ---
            dynamodb = self.aws_loader.get_client('dynamodb')
            response = dynamodb.get_item(
                TableName=dynamodb_table_name,
                Key={'PK': {'S': pk}, 'SK': {'S': sk}}
            )
            if 'Item' in response:
                print(f"❌ Mundo com ID {mundo.id_mundo} já existe no DynamoDB.")
                return False

            # --- Serializar e enviar para S3 ---
            dados_s3 = Serializador.to_serializable_dict(mundo)
            dados_json = json.dumps(dados_s3, ensure_ascii=False, indent=2)

            s3 = self.aws_loader.get_client('s3')
            s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=dados_json,
                ContentType='application/json'
            )
            print(f"✅ Upload para S3 concluído: s3://{bucket_name}/{s3_key}")

            # --- Salvar metadados no DynamoDB ---
            try:
                bioma_inicial = getattr(mundo.planeta, 'bioma_inicial', 'Desconhecido')
                vagas = getattr(mundo.planeta, 'numero_de_jogadores', 0)

                dynamodb.put_item(
                    TableName=dynamodb_table_name,
                    Item={
                        'PK': {'S': pk},
                        'SK': {'S': sk},
                        'entityType': {'S': 'Planet'},
                        'fator': {'N': str(mundo.planeta.fator)},
                        'bioma_inicial': {'S': bioma_inicial},
                        'vagas': {'N': str(vagas)},
                        'timestamp': {'N': str(int(time.time()))}
                    }
                )
                print(f"✅ Metadados do mundo {mundo.id_mundo} salvos no DynamoDB.")
                return True

            except Exception as e:
                print(f"❌ Falha ao salvar no DynamoDB: {e}")
                print(f"🧹 Removendo arquivo órfão do S3: s3://{bucket_name}/{s3_key}")
                try:
                    s3.delete_object(Bucket=bucket_name, Key=s3_key)
                    print("✅ Arquivo órfão removido com sucesso.")
                except Exception as del_e:
                    print(f"⚠️ Falha ao remover arquivo órfão do S3: {del_e}")
                return False

        except Exception as e:
            print(f"❌ Erro inesperado durante upload_mundo: {e}")
            return False

    def criar_e_upload_mundo(
        self,
        fator: int,
        bioma: str,
        bucket_name: str = "global-arena-tiles",
        s3_prefix: str = "planetas/"
    ) -> bool:
        """
        Cria um novo mundo com fator e bioma dados, e faz upload direto para S3 + DynamoDB.

        :param fator: Nível de detalhe da grade geográfica (ex: 4)
        :param bioma: Bioma inicial para escolha de capitais (ex: "Meadow")
        :param bucket_name: Nome do bucket S3
        :param s3_prefix: Prefixo (pasta) no bucket
        :return: True se sucesso, False caso contrário
        """
        try:
            print(f"🌍 Criando mundo com fator={fator}, bioma='{bioma}'...")
            mundo = Mundo(fator=fator, bioma=bioma)
            print(f"✅ Mundo criado: {mundo.id_mundo}")

            sucesso = self.upload_mundo(mundo, bucket_name=bucket_name, s3_prefix=s3_prefix)

            if sucesso:
                print(f"🎉 Mundo {mundo.id_mundo} enviado com sucesso para a nuvem!")
            else:
                print(f"❌ Falha no upload do mundo {mundo.id_mundo}")

            return sucesso

        except Exception as e:
            print(f"❌ Erro ao criar e upload mundo: {e}")
            return False

    def criar_e_upload_mundo_com_retorno(
            self,
            fator: int,
            bioma: str,
            bucket_name: str = "global-arena-tiles",
            s3_prefix: str = "planetas/",
            dynamodb_table_name: str = "GlobalArena"
    ) -> Tuple[bool, Optional[Mundo]]:
        """
        Cria um novo mundo com fator e bioma dados, faz upload para S3 + DynamoDB,
        e retorna sucesso e a instância do mundo.
        """
        try:
            print(f"🌍 Criando mundo com fator={fator}, bioma='{bioma}'...")
            mundo = Mundo(fator=fator, bioma=bioma)
            print(f"✅ Mundo criado: {mundo.id_mundo}")

            sucesso = self.upload_mundo(
                mundo,
                bucket_name=bucket_name,
                s3_prefix=s3_prefix,
                dynamodb_table_name=dynamodb_table_name
            )

            if sucesso:
                print(f"🎉 Mundo {mundo.id_mundo} enviado com sucesso para a nuvem!")
            else:
                print(f"❌ Falha no upload do mundo {mundo.id_mundo}")

            return sucesso, mundo

        except Exception as e:
            print(f"❌ Erro ao criar e upload mundo: {e}")
            import traceback
            traceback.print_exc()
            return False, None

    def criar_mundo(self, fator: int, bioma: str) -> Mundo:
        """Cria e retorna um novo mundo."""
        return Mundo(fator=fator, bioma=bioma)