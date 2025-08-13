# aws_loader.py

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class AWSLoader:
    def __init__(self, profile_name=None, region_name='us-east-2'):
        """
        Inicializa o loader de credenciais AWS.

        :param profile_name: Nome do perfil no arquivo ~/.aws/credentials (opcional)
        :param region_name: Região AWS padrão
        """
        self.profile_name = profile_name
        self.region_name = region_name
        self.session = None
        self._create_session()

    def _create_session(self):
        """Cria uma sessão boto3 com base no perfil ou nas credenciais padrão."""
        try:
            if self.profile_name:
                self.session = boto3.Session(profile_name=self.profile_name, region_name=self.region_name)
            else:
                self.session = boto3.Session(region_name=self.region_name)

            # Testa credenciais
            sts = self.session.client('sts')
            sts.get_caller_identity()
            print("✅ Credenciais AWS carregadas com sucesso.")

        except NoCredentialsError:
            raise Exception("❌ Credenciais AWS não encontradas. Configure AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY.")
        except PartialCredentialsError:
            raise Exception("❌ Credenciais incompletas. Verifique AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY.")
        except Exception as e:
            raise Exception(f"❌ Erro ao carregar credenciais: {e}")

    def get_credentials(self):
        """
        Retorna as credenciais (access key, secret key, token).
        """
        credentials = self.session.get_credentials()
        frozen_creds = credentials.get_frozen_credentials()
        return {
            'access_key': frozen_creds.access_key,
            'secret_key': frozen_creds.secret_key,
            'token': frozen_creds.token
        }

    def get_client(self, service_name):
        """Retorna um cliente boto3 para o serviço especificado."""
        return self.session.client(service_name)

    def get_resource(self, service_name):
        """Retorna um recurso boto3 (ex: S3 resource)."""
        return self.session.resource(service_name)

    # --- 🔧 Novos métodos adicionados ---
    def get_account_info(self):
        """Retorna informações da conta AWS: ID, ARN, usuário, região."""
        sts = self.session.client('sts')
        identity = sts.get_caller_identity()
        return {
            'account_id': identity['Account'],
            'user_id': identity['UserId'],
            'arn': identity['Arn'],
            'region': self.region_name
        }

    def list_s3_buckets(self):
        """Lista todos os buckets S3 da conta."""
        s3 = self.get_client('s3')
        response = s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]

    def list_dynamodb_tables(self):
        """Lista todas as tabelas DynamoDB da conta."""
        dynamodb = self.get_client('dynamodb')
        response = dynamodb.list_tables()
        return response['TableNames']