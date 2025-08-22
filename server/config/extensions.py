# server/extensions.py
from server.integrations.aws_loader import AWSLoader

class Extensions:
    def __init__(self):
        self.dynamodb = None
        # self.redis = None # Futuro

    def init_app(self, app):
        """Inicializa as extensões com base na configuração da app Flask."""
        try:
            aws_loader = AWSLoader(
                profile_name=app.config['AWS_PROFILE_NAME'],
                region_name=app.config['AWS_REGION_NAME']
            )
            self.dynamodb = aws_loader.get_client('dynamodb')
            print("✅ Cliente DynamoDB conectado via Extensions.")
        except Exception as e:
            print(f"❌ Falha ao conectar ao DynamoDB na inicialização: {e}")
            self.dynamodb = None # Ou lançar exceção, dependendo da política de falhas

# Instância global
ext = Extensions()