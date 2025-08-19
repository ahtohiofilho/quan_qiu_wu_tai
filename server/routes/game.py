# server/routes/game.py
from flask import Blueprint, jsonify, request
from server.services.user_service import UserService
jogo_bp = Blueprint('jogo', __name__, url_prefix='/jogo')

# Variável para injeção de dependência
_user_service = None

def register_jogo_routes(user_service: UserService):
    """Função para injetar dependências no blueprint jogo."""
    global _user_service
    _user_service = user_service

@jogo_bp.route('/entrar', methods=['POST'])
def entrar_na_fila():
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON esperado"}), 400

    data = request.get_json()
    modo = data.get("modo")

    if modo != "online":
        return jsonify({"success": False, "message": "Modo inválido. Use 'online'."}), 400

    # Aqui você pode validar o usuário via token depois
    username = data.get("username")
    if not username:
        return jsonify({"success": False, "message": "Username necessário."}), 400

    # Simples validação de existência (opcional)
    usuario = _user_service.get_user(username)
    if not usuario:
        return jsonify({"success": False, "message": "Usuário não encontrado."}), 404

    # 🔮 Futuramente: adicionar à fila de matchmaking
    return jsonify({
        "success": True,
        "message": f"{username} entrou na fila de jogo online.",
        "modo": modo
    }), 200