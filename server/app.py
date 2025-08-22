# server/app.py
from flask import Flask, jsonify
from server.config.config import config
from server.config.extensions import ext
from server.services.user_service import UserService
from server.routes.auth import auth_bp, register_routes
from server.routes.game import jogo_bp, register_jogo_routes
from server.services.matchmaking_service import MatchmakingService
from server.services.world_pool import MundoPoolService  # ✅ Importe o novo serviço
from server.integrations.aws_loader import AWSLoader
from server.core.manager import Gerenciador


def create_app(config_name='default'):
    """Factory function para criar a aplicação Flask."""
    app = Flask(__name__)

    # 1. Carrega a configuração
    app.config.from_object(config[config_name])

    # 2. Inicializa as extensões
    ext.init_app(app)

    # 3. Cria instâncias de serviços, injetando dependências
    user_service = UserService(ext.dynamodb, app.config['DYNAMODB_TABLE_NAME'])
    print(f"✅ DEBUG: UserService criado: {user_service}")

    # --- 🔹 AWS Loader e Gerenciador de Mundos ---
    aws_loader = AWSLoader(
        profile_name=app.config.get('AWS_PROFILE_NAME'),
        region_name=app.config.get('AWS_REGION_NAME')
    )

    # ✅ Passando o nome da tabela DynamoDB para o Gerenciador
    gerenciador = Gerenciador(
        aws_loader=aws_loader,
        save_dir="saves",
        dynamodb_table_name=app.config['DYNAMODB_TABLE_NAME']  # ← Correção essencial
    )

    # --- 🔹 World Pool: Gerencia mundos pré-criados ---
    world_pool = MundoPoolService(
        gerenciador=gerenciador,
        fator=4,
        bioma="Meadow",
        min_mundos=3,
        max_mundos=10,
        intervalo_verificacao=5.0
    )

    # --- 🔹 Matchmaking: Sistema Avançado de Salas ---
    # MatchmakingService agora recebe o world_pool, não o gerenciador diretamente
    matchmaking_service = MatchmakingService(world_pool=world_pool)

    # Callback para quando uma partida for formada
    def partida_formada(jogadores):
        print(f"\n🎉🎉🎉 PARTIDA INICIADA COM: {jogadores}")
        print(f"🎮 Os jogadores estão prontos para o combate!\n")
        # Aqui você pode:
        # - Notificar jogadores via WebSocket
        # - Registrar a partida no DynamoDB
        # - Iniciar a lógica do jogo

    # ✅ Registra o callback no novo serviço
    matchmaking_service.partida_iniciada_callback = partida_formada

    # Armazena serviços no app.config para acesso futuro, se necessário
    app.config['USER_SERVICE'] = user_service
    app.config['MATCHMAKING_SERVICE'] = matchmaking_service

    # 4. Registra os Blueprints e injeta dependências
    print("📋 DEBUG: Iniciando injeção de dependências e registro de blueprints...")

    # --- 🔹 Auth ---
    print("🔧 DEBUG: Injetando UserService em auth_bp...")
    register_routes(user_service)
    print(f"✅ DEBUG: register_routes(user_service) chamado com sucesso.")
    app.register_blueprint(auth_bp)
    print("✅ DEBUG: auth_bp registrado no app.")

    # --- 🔹 Jogo Online (NOVO) ---
    register_jogo_routes(user_service, matchmaking_service)
    app.register_blueprint(jogo_bp)
    print("✅ DEBUG: jogo_bp registrado no app.")

    # 5. Rotas principais (opcional)
    @app.route('/')
    def home():
        return "🚀 Servidor Global Arena - API (Refatorado com Classes)", 200

    # 🔍 Rota de status do matchmaking (monitoramento)
    @app.route('/status')
    def status():
        return jsonify({
            "success": True,
            "total_na_fila": world_pool.total_jogadores_na_fila(),  # ✅ Agora existe
            "mundos_no_pool": world_pool.quantidade_total(),
            "vagas_disponiveis": world_pool.quantidade_vagas(),
            "partidas_ativas": len(matchmaking_service.salas)
        })

    return app


# Para execução direta (ex: python server/app.py)
if __name__ == '__main__':
    app = create_app('development')  # Ou 'production'
    print("🚀 Iniciando Servidor Global Arena (Flask - Refatorado)...")
    print("📄 Endpoints disponíveis:")
    print("   GET  /                        - Status do servidor")
    print("   GET  /status                  - Status do matchmaking e pool de mundos")
    print("   GET  /auth/teste_dynamodb     - Teste de conexão com DynamoDB")
    print("   POST /jogo/entrar             - Entrar na fila de jogo online (novo)")
    print("-" * 40)
    app.run(host='127.0.0.1', port=5000, debug=app.config['DEBUG'])