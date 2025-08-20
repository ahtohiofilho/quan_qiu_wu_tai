# server/routes/auth.py
"""
Módulo de rotas de autenticação (login, registro).
Gerencia a injeção de dependência do UserService.
"""
import re
import bcrypt
import unicodedata
from flask import Blueprint, request, jsonify, current_app

# Cria o Blueprint com prefixo
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Variável global para injeção de dependência
_user_service = None


def normalizar_username(username: str) -> str:
    """
    Normaliza o username: remove acentos, converte para minúsculas,
    substitui caracteres especiais por underscores.
    Retorna None se resultar em string vazia.
    """
    if not username:
        return None
    # Remove acentos
    username = unicodedata.normalize('NFKD', username)
    username = ''.join(c for c in username if not unicodedata.combining(c))
    # Substitui não alfanuméricos por underscore
    username = re.sub(r'[^a-zA-Z0-9]', '_', username)
    # Minúsculas
    username = username.lower()
    # Underscores múltiplos → único
    username = re.sub(r'_+', '_', username).strip('_')
    return username or None


def register_routes(user_service):
    """
    Função de injeção de dependência.
    Configura as rotas do auth_bp com o UserService fornecido.
    Deve ser chamada ANTES de registrar o blueprint no app.
    """
    global _user_service
    print(f"📥 DEBUG: Injetando user_service: {user_service}")
    _user_service = user_service

    # Valida se o serviço foi injetado
    if not _user_service:
        print("❌ ERRO GRAVE: user_service é None em register_routes!")
        raise RuntimeError("UserService não injetado em auth_bp.")
    else:
        print(f"✅ DEBUG: _user_service atribuído com sucesso: {_user_service}")


# --- ENDPOINT: Teste de Conexão ---
@auth_bp.route('/teste_dynamodb', methods=['GET'])
def teste_dynamodb():
    """Testa a conexão com o DynamoDB via UserService."""
    if not _user_service or not _user_service.dynamodb:
        return jsonify({
            "status": "erro",
            "message": "Cliente DynamoDB não disponível."
        }), 500

    try:
        response = _user_service.dynamodb.list_tables()
        tabelas = response.get('TableNames', [])
        return jsonify({
            "status": "sucesso",
            "message": "Conexão com DynamoDB bem-sucedida.",
            "tabelas": tabelas
        }), 200
    except Exception as e:
        return jsonify({
            "status": "erro",
            "message": f"Falha ao acessar DynamoDB: {str(e)}"
        }), 500


# --- ENDPOINT: Registrar Usuário ---
@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    """
    Registra um novo usuário.
    Expects: {"username": "str", "password": "str"}
    Returns: {"success": bool, "message": str}
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON esperado."}), 400

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    # Validar campos
    if not username or not password:
        return jsonify({"success": False, "message": "Username e senha são obrigatórios."}), 400
    if len(username) < 3:
        return jsonify({"success": False, "message": "Username deve ter pelo menos 3 caracteres."}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "Senha deve ter pelo menos 6 caracteres."}), 400

    # Normalizar username (opcional)
    username_normalizado = normalizar_username(username)
    if not username_normalizado:
        return jsonify({"success": False, "message": "Username inválido após normalização."}), 400

    # Verificar se já existe (usando o nome original)
    if _user_service.get_user(username):
        return jsonify({"success": False, "message": "Username já está em uso."}), 409

    # Hashear senha
    try:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    except Exception as e:
        print(f"❌ Erro ao hashear senha para '{username}': {e}")
        return jsonify({"success": False, "message": "Erro ao processar senha."}), 500

    # Salvar no DynamoDB
    sucesso = _user_service.create_user_item(username, password_hash=password_hash)
    if sucesso:
        print(f"✅ Usuário '{username}' registrado com sucesso.")
        return jsonify({"success": True, "message": "Usuário registrado com sucesso."}), 201
    else:
        return jsonify({"success": False, "message": "Falha ao salvar no banco."}), 500


# --- ENDPOINT: Login ---
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica um usuário.
    Expects: {"username": "str", "password": "str"}
    Returns: {"success": bool, "message": str, "token": str (opcional)}
    """
    print("🔍 DEBUG: Rota /auth/login foi chamada!")

    # Garantir acesso ao serviço injetado via register_routes
    global _user_service
    if not _user_service:
        print("💥 ERRO: _user_service não foi injetado!")
        return jsonify({
            "success": False,
            "message": "Erro interno do servidor."
        }), 500

    try:
        # 1. Validar formato da requisição
        if not request.is_json:
            print("❌ Requisição não é JSON")
            return jsonify({
                "success": False,
                "message": "JSON esperado."
            }), 400

        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        print(f"🔐 Tentativa de login - username: {username}")

        # 2. Validar campos obrigatórios
        if not username:
            print("⚠️ Username ausente")
            return jsonify({
                "success": False,
                "message": "Username é obrigatório."
            }), 400
        if not password:
            print("⚠️ Senha ausente")
            return jsonify({
                "success": False,
                "message": "Senha é obrigatória."
            }), 400

        # 3. Buscar usuário no DynamoDB
        usuario = _user_service.get_user(username)
        if not usuario:
            print(f"❌ Credenciais inválidas para '{username}'.")
            return jsonify({
                "success": False,
                "message": "Credenciais inválidas."
            }), 401

        # 4. Extrair e validar hash da senha
        password_hash_attr = usuario.get('password_hash')
        if not password_hash_attr:
            print(f"❌ Usuário '{username}' sem password_hash.")
            return jsonify({
                "success": False,
                "message": "Credenciais inválidas."
            }), 401

        # Suporta formato DynamoDB {'B': bytes} ou bytes direto
        stored_hash = password_hash_attr.get('B') if isinstance(password_hash_attr, dict) else password_hash_attr

        if not isinstance(stored_hash, bytes):
            print(f"⚠️ Hash inválido para '{username}': {type(stored_hash)}")
            return jsonify({
                "success": False,
                "message": "Credenciais inválidas."
            }), 401

        # 5. Verificar senha com bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print(f"✅ Login bem-sucedido para '{username}'.")

            # 🔐 Gera um token fake para compatibilidade com o simulador
            # (Futuro: substituir por JWT real)
            fake_token = f"fake-jwt-{username}-{hash(username) % 10000}"

            return jsonify({
                "success": True,
                "message": "Login bem-sucedido.",
                "token": fake_token  # ← Adicionado para o simulador usar
            }), 200
        else:
            print(f"❌ Senha incorreta para '{username}'.")
            return jsonify({
                "success": False,
                "message": "Credenciais inválidas."
            }), 401

    except Exception as e:
        print(f"💥 ERRO NÃO TRATADO em /auth/login: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "Erro interno no servidor."
        }), 500