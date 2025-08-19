# server/app.py
from flask import Flask
from server.config import config
from server.extensions import ext
from server.services.user_service import UserService
from server.routes.auth import auth_bp, register_routes
from server.routes.game import jogo_bp, register_jogo_routes

def create_app(config_name='default'):
    """Factory function para criar a aplicação Flask."""
    app = Flask(__name__)

    # 1. Carrega a configuração
    app.config.from_object(config[config_name])

    # 2. Inicializa as extensões
    ext.init_app(app)

    # 3. Cria instâncias de serviços, injetando dependências
    user_service = UserService(ext.dynamodb, app.config['DYNAMODB_TABLE_NAME'])

    # 4. Registra os Blueprints e injeta dependências

    # --- 🔹 Auth ---
    register_routes(user_service)
    app.register_blueprint(auth_bp)

    # --- 🔹 Jogo Online (NOVO) ---
    register_jogo_routes(user_service)  # Pode injetar outros serviços depois
    app.register_blueprint(jogo_bp)    # Registra o blueprint

    # 5. Rotas principais (opcional)
    @app.route('/')
    def home():
        return "🚀 Servidor Global Arena - API (Refatorado com Classes)", 200

    return app

# Para execução direta (ex: python server/app.py)
if __name__ == '__main__':
    app = create_app('development')  # Ou 'production'
    print("🚀 Iniciando Servidor Global Arena (Flask - Refatorado)...")
    print("📄 Endpoints disponíveis:")
    print("   GET  /                        - Status do servidor")
    print("   GET  /auth/teste_dynamodb     - Teste de conexão com DynamoDB")
    print("   POST /jogo/entrar             - Entrar na fila de jogo online (novo)")
    print("-" * 40)
    app.run(host='127.0.0.1', port=5000, debug=app.config['DEBUG'])