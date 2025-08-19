# server/routes/auth.py
import bcrypt
from flask import Blueprint, request, jsonify, current_app

# Cria um Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Esta função será chamada em app.py para registrar as rotas e passar dependências
def register_routes(user_service_instance):
    """Registra as rotas do Blueprint com as dependências injetadas."""

    # --- Endpoint de Teste (já existente) ---
    @auth_bp.route('/teste_dynamodb')
    def teste_dynamodb():
        """Endpoint de teste para verificar a conexão com o DynamoDB."""
        if not user_service_instance.dynamodb:
            return jsonify({"status": "erro", "message": "Cliente DynamoDB não disponível no serviço."}), 500

        try:
            response = user_service_instance.dynamodb.list_tables()
            tabelas = response.get('TableNames', [])
            return jsonify({
                "status": "sucesso",
                "message": "Conexão com DynamoDB bem-sucedida via UserService.",
                "tabelas": tabelas
            }), 200
        except Exception as e:
            return jsonify({"status": "erro", "message": f"Falha ao testar DynamoDB: {str(e)}"}), 500

    # --- Novo Endpoint: Registro de Usuário ---
    @auth_bp.route('/registrar', methods=['POST'])
    def registrar():
        """
        Endpoint para registro de novo usuário.
        Espera um JSON: {"username": "nome", "password": "senha"}
        Retorna um JSON: {"success": true/false, "message": "..."}
        """
        # 1. Validar requisição
        if not request.is_json:
            return jsonify({"success": False, "message": "Content-Type deve ser application/json"}), 400

        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        # 2. Validar dados de entrada
        if not username or not password:
            return jsonify({"success": False, "message": "Username e password são obrigatórios."}), 400

        if len(username) < 3:
            return jsonify({"success": False, "message": "Username deve ter pelo menos 3 caracteres."}), 400
        if len(password) < 6:
            return jsonify({"success": False, "message": "Password deve ter pelo menos 6 caracteres."}), 400

        # 3. Verificar se o usuário já existe
        usuario_existente = user_service_instance.get_user(username)
        if usuario_existente:
            # É comum retornar 409 Conflict para recursos que já existem
            return jsonify({"success": False, "message": "Nome de usuário já está em uso."}), 409

        # 4. Hashear a senha
        try:
            salt = bcrypt.gensalt()
            # bcrypt.hashpw retorna bytes
            password_hash_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
        except Exception as e:
            print(f"❌ Erro ao hashear senha para usuário '{username}': {e}")
            return jsonify({"success": False, "message": "Erro interno ao processar a senha."}), 500

        # 5. Preparar atributos para salvar no DynamoDB
        # O username e PK/SK são definidos dentro do user_service
        atributos_usuario = {
            # Armazenar o hash como binário ('B')
            'password_hash': password_hash_bytes,
            # Você pode adicionar outros atributos aqui, como data de criação
            # 'data_criacao': datetime.utcnow().isoformat() + 'Z' # Se quiser salvar como string
        }

        # 6. Salvar o usuário no DynamoDB
        sucesso_criacao = user_service_instance.create_user_item(username, **atributos_usuario)

        if sucesso_criacao:
            print(f"✅ Usuário '{username}' registrado com sucesso.")
            # 201 Created é o código apropriado para criação bem-sucedida
            return jsonify({"success": True, "message": "Usuário registrado com sucesso."}), 201
        else:
            # A mensagem de erro já foi impressa pelo user_service
            return jsonify({"success": False, "message": "Falha ao registrar usuário no banco de dados."}), 500

    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        Endpoint para autenticação de usuário.
        Espera: {"username": "nome", "password": "senha"}
        Retorna: {"success": bool, "message": str}
        """
        # 1. Verificar se o corpo é JSON
        if not request.is_json:
            return jsonify({"success": False, "message": "Requisição deve ser JSON."}), 400

        data = request.get_json()

        # 2. Extrair e validar campos
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username:
            return jsonify({"success": False, "message": "Nome de usuário é obrigatório."}), 400
        if not password:
            return jsonify({"success": False, "message": "Senha é obrigatória."}), 400

        # 3. Buscar usuário
        try:
            usuario = user_service_instance.get_user(username)
            if not usuario:
                return jsonify({"success": False, "message": "Usuário não encontrado."}), 404
        except Exception as e:
            print(f"❌ Erro ao buscar usuário '{username}': {e}")
            return jsonify({"success": False, "message": "Erro interno ao acessar banco de dados."}), 500

        # 4. Extrair e validar hash da senha
        password_hash_attr = usuario.get('password_hash')
        if not password_hash_attr:
            return jsonify({"success": False, "message": "Usuário sem senha cadastrada."}), 500

        # Extrair bytes do campo 'B' se for um dict (formato DynamoDB)
        if isinstance(password_hash_attr, dict) and 'B' in password_hash_attr:
            stored_hash = password_hash_attr['B']
        elif isinstance(password_hash_attr, bytes):
            stored_hash = password_hash_attr
        else:
            print(f"⚠️ Formato inesperado de password_hash para '{username}': {type(password_hash_attr)}")
            return jsonify({"success": False, "message": "Erro interno de autenticação."}), 500

        # 5. Verificar senha com bcrypt
        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return jsonify({"success": True, "message": "Login bem-sucedido."}), 200
            else:
                return jsonify({"success": False, "message": "Senha incorreta."}), 401
        except Exception as e:
            print(f"❌ Erro ao verificar senha com bcrypt: {e}")
            return jsonify({"success": False, "message": "Erro interno ao processar autenticação."}), 500
