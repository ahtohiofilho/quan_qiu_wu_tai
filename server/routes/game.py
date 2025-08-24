# server/routes/game.py
from flask import Blueprint, jsonify, request
from server.services.user_service import UserService
from server.services.matchmaking_service import MatchmakingService  # ✅ Usa o serviço de matchmaking


jogo_bp = Blueprint('jogo', __name__, url_prefix='/jogo')

# Variáveis para injeção de dependência
_user_service = None
_matchmaking_service = None


def register_jogo_routes(user_service: UserService, matchmaking_service: MatchmakingService):
    """Função para injetar dependências no blueprint jogo."""
    global _user_service, _matchmaking_service
    _user_service = user_service
    _matchmaking_service = matchmaking_service


@jogo_bp.route('/entrar', methods=['POST'])
def entrar_na_fila():
    """Adiciona o jogador à fila de matchmaking online."""
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

    # ✅ Tenta entrar na fila
    mensagem = _matchmaking_service.entrar_na_fila(username)
    if "Erro ao entrar na fila" in mensagem:
        return jsonify({"success": False, "message": mensagem}), 409

    # ✅ Encontra a sala onde o jogador foi alocado
    sala_atual = None
    for sala in _matchmaking_service.salas:
        if username in sala.jogadores:
            sala_atual = sala
            break

    if not sala_atual:
        return jsonify({
            "success": False,
            "message": "Erro interno: jogador não encontrado em nenhuma sala."
        }), 500

    # ✅ Total de jogadores em todas as salas ativas
    total_na_fila = sum(len(sala.jogadores) for sala in _matchmaking_service.salas)

    return jsonify({
        "success": True,
        "message": mensagem,
        "modo": modo,
        "total_na_fila": total_na_fila,
        "max_jogadores": sala_atual.vagas  # Limite da sala
    }), 200


@jogo_bp.route('/sair', methods=['POST'])
def sair_da_fila():
    """
    Permite que um jogador saia da fila de matchmaking.
    Útil quando clica em 'Cancelar' na UI.
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON esperado"}), 400

    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"success": False, "message": "Username necessário."}), 400

    # ✅ Tenta remover o jogador da fila
    if _matchmaking_service.sair_da_fila(username):
        return jsonify({
            "success": True,
            "message": f"{username} saiu da fila com sucesso."
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Você não estava na fila."
        }), 400

@jogo_bp.route('/limpar_usuario', methods=['POST'])
def limpar_usuario():
    """Remove o jogador de qualquer fila ou sala, mesmo que não esteja na fila."""
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON esperado"}), 400
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"success": False, "message": "Username necessário"}), 400

    # Tenta remover da fila (não importa se já saiu, só garante o cleanup)
    _matchmaking_service.sair_da_fila(username)

    return jsonify({"success": True, "message": f"Estado de {username} limpo."}), 200


@jogo_bp.route('/status', methods=['GET'])
def status():
    """Retorna o status do jogador: se está na fila ou em partida."""
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username necessário"}), 400

    # Verificar se está na fila
    em_fila = any(username in sala.jogadores for sala in _matchmaking_service.salas)

    # Verificar se está em partida (você pode ter um serviço de "partidas ativas")
    # Por enquanto, assumimos que se está na fila e a partida iniciou, está em partida
    em_partida = False
    for sala in _matchmaking_service.salas:
        if username in sala.jogadores and len(sala.jogadores) >= 4:
            em_partida = True
            break

    return jsonify({
        "em_fila": em_fila,
        "em_partida": em_partida,
        "total_na_fila": sum(len(s.jogadores) for s in _matchmaking_service.salas)
    })