# server/manager.py
import json
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

    def upload_mundo(
        self,
        mundo: Mundo,
        bucket_name: str = "global-arena-tiles",
        s3_prefix: str = "planetas/"
    ) -> bool:
        """
        Serializa o mundo e envia diretamente para S3.
        Também salva metadados no DynamoDB.

        :param mundo: Instância de Mundo a ser enviada.
        :param bucket_name: Nome do bucket S3.
        :param s3_prefix: Prefixo (pasta virtual) no bucket.
        :return: True se sucesso, False caso contrário.
        """
        try:
            # --- 1. Serializar ---
            data = Serializador.to_serializable_dict(mundo)
            json_data = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
            s3_key = f"{s3_prefix}{mundo.id_mundo}.json"

            # --- 2. Upload para S3 ---
            s3_client = self.aws_loader.get_client('s3')
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=json_data,
                ContentType='application/json'
            )
            print(f"✅ Mundo enviado para S3: s3://{bucket_name}/{s3_key}")

            # --- 3. Salvar metadados no DynamoDB ---
            dynamodb = self.aws_loader.get_client('dynamodb')
            bioma_inicial = mundo.planeta.geografia.nodes[mundo.planeta.capitais_players[0]]['bioma']
            item = {
                'id_mundo': {'S': mundo.id_mundo},
                'fator': {'N': str(mundo.planeta.fator)},
                'bioma_inicial': {'S': bioma_inicial},
                'vagas': {'SS': []}  # Set vazio para IDs de usuários
            }
            dynamodb.put_item(TableName="planetas_metadata", Item=item)
            print(f"✅ Metadados salvos no DynamoDB: {mundo.id_mundo}")

            return True

        except Exception as e:
            print(f"❌ Falha ao salvar/upload mundo: {e}")
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
        s3_prefix: str = "planetas/"
    ) -> Tuple[bool, Optional[Mundo]]:
        """
        Cria um novo mundo com fator e bioma dados, faz upload para S3 + DynamoDB,
        e retorna sucesso e a instância do mundo.

        Útil para operações que precisam do objeto Mundo após o upload (ex: salvar localmente).

        :param fator: Nível de detalhe da grade geográfica.
        :param bioma: Bioma inicial para escolha de capitais.
        :param bucket_name: Nome do bucket S3.
        :param s3_prefix: Prefixo (pasta) no bucket.
        :return: (sucesso: bool, mundo: Mundo ou None)
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

            return sucesso, mundo

        except Exception as e:
            print(f"❌ Erro ao criar e upload mundo: {e}")
            return False, None

    def criar_mundo(self, fator: int, bioma: str) -> Mundo:
        """Cria e retorna um novo mundo."""
        return Mundo(fator=fator, bioma=bioma)