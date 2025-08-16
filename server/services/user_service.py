# server/services/user_service.py
import boto3
from botocore.exceptions import ClientError


class UserService:
    def __init__(self, dynamodb_client, table_name):
        self.dynamodb = dynamodb_client
        self.table_name = table_name

    def _format_user_key(self, username: str) -> dict:
        """Formata a chave primária do usuário no DynamoDB."""
        return {
            'PK': {'S': f'USER#{username}'},
            'SK': {'S': 'PROFILE'}
        }

    def get_user(self, username: str) -> dict:
        """Busca um usuário pelo username."""
        if not self.dynamodb:
            print("⚠️ Cliente DynamoDB não disponível no UserService.")
            return None
        try:
            response = self.dynamodb.get_item(
                TableName=self.table_name,
                Key=self._format_user_key(username)
            )
            return response.get('Item')
        except ClientError as e:
            print(f"❌ Erro do DynamoDB ao buscar usuário '{username}': {e.response['Error']['Message']}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado ao buscar usuário '{username}': {e}")
            return None

    def create_user_item(self, username: str, **attributes) -> bool:
        """
        Cria um novo item de usuário no DynamoDB.
        `attributes` pode conter {'password_hash': bytes, 'outro_attr': valor, ...}
        """
        if not self.dynamodb:
            print("⚠️ Cliente DynamoDB não disponível no UserService.")
            return False
        try:
            # Inicia o item com a chave primária
            item = self._format_user_key(username)

            # Adiciona outros atributos fornecidos
            for attr_name, attr_value in attributes.items():
                # Trata tipos específicos
                if isinstance(attr_value, bytes):
                    # Para password_hash, salva como tipo binário 'B'
                    item[attr_name] = {'B': attr_value}
                elif isinstance(attr_value, str):
                    # Para strings, salva como tipo string 'S'
                    item[attr_name] = {'S': attr_value}
                elif isinstance(attr_value, (int, float)):
                    # Para números, salva como tipo número 'N' (convertido para string)
                    item[attr_name] = {'N': str(attr_value)}
                else:
                    # Para outros tipos, converte para string e salva como 'S'
                    # (você pode querer ser mais específico aqui dependendo das suas necessidades)
                    print(
                        f"⚠️ Atributo '{attr_name}' tem tipo inesperado ({type(attr_value)}). Convertendo para string.")
                    item[attr_name] = {'S': str(attr_value)}

            self.dynamodb.put_item(
                TableName=self.table_name,
                Item=item
            )
            print(f"✅ Item de usuário '{username}' criado/Atualizado no DynamoDB.")
            return True
        except ClientError as e:
            print(f"❌ Erro do DynamoDB ao criar usuário '{username}': {e.response['Error']['Message']}")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado ao criar usuário '{username}': {e}")
            return False

    # Métodos para verificar senha, gerar token, etc., virão aqui depois.
