# server/config.py
import os


class Config:
    # Flask
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'chave_secreta_dev_super_segura'  # Em produção, use variável de ambiente

    # AWS
    AWS_PROFILE_NAME = os.environ.get('AWS_PROFILE_NAME') or None
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME') or 'us-east-2'  # Certifique-se de usar a mesma região

    # DynamoDB
    DYNAMODB_TABLE_NAME = os.environ.get(
        'DYNAMODB_TABLE_NAME') or 'GlobalArena'  # Ou 'UsuariosGlobalArena' se criar uma nova

    # Futuras configurações (ex: Redis, Logging)
    # REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # SECRET_KEY = os.environ.get('SECRET_KEY') # Obrigatório em produção


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}