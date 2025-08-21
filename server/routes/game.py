# server/routes/game.py
from flask import Blueprint, jsonify, request
from server.services.user_service import UserService
from server.services.matchmaking_service import MatchmakingService  # ✅ Substituído: agora usa MatchmakingService

jogo_bp = Blueprint('jogo', __name__, url_prefix='/jogo')

# Variável para injeção de dependência
_user_service = None
_matchmaking_service = None  # ✅ Renomeado: _fila_service → _matchmaking_service


def register_jogo_routes(user_service: UserService, matchmaking_service: MatchmakingService):
    """Função para injetar dependências no blueprint jogo."""
    global _user_service, _matchmaking_service
    _user_service = user_service
    _matchmaking_service = matchmaking_service  # ✅ Injeta o novo serviço


@jogo_bp.route('/entrar', methods=['POST'])
def entrar_na_fila():
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON esperado"}), 400

    data = request.get_json()
    modo = data.get("modo")
    username = data.get("username")

    if modo != "online":
        return jsonify({"success": False, "message": "Modo inválido. Use 'online'."}), 400

    if not username:
        return jsonify({"success": False, "message": "Username necessário."}), 400

    # ✅ Validar se o usuário existe
    usuario = _user_service.get_user(username)
    if not usuario:
        return jsonify({"success": False, "message": "Usuário não encontrado."}), 404

    # ✅ ADICIONAR À FILA DE MATCHMAKING
    mensagem = _matchmaking_service.entrar_na_fila(username)

    # O método retorna uma mensagem; sucesso se não contiver erro
    if "Erro ao entrar na fila" in mensagem:
        return jsonify({
            "success": False,
            "message": mensagem
        }), 409

    # ✅ Contagem total de jogadores em todas as salas ativas
    total_na_fila = sum(len(sala.jogadores) for sala in _matchmaking_service.salas if sala.jogadores)

    return jsonify({
        "success": True,
        "message": mensagem,
        "modo": modo,
        "total_na_fila": total_na_fila
    }), 200