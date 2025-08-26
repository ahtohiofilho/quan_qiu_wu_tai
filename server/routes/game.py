# server/routes/game.py
"""
Rotas relacionadas ao jogo online (fila de matchmaking, status, etc).
Todas as rotas são registradas dentro de uma função fábrica de blueprint,
permitindo injeção explícita de dependências (UserService, MatchmakingService).
"""

from flask import Blueprint, jsonify, request
from server.services.user_service import UserService
from server.services.matchmaking_service import MatchmakingService


def create_game_blueprint(
    user_service: UserService,
    matchmaking_service: MatchmakingService
) -> Blueprint:
    """
    Cria o blueprint de rotas do jogo com as dependências injetadas.
    """
    jogo_bp = Blueprint("jogo", __name__, url_prefix="/jogo")

    @jogo_bp.route("/entrar", methods=["POST"])
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

        # Validar se o usuário existe
        usuario = user_service.get_user(username)
        if not usuario:
            return jsonify({"success": False, "message": "Usuário não encontrado."}), 404

        # Tenta entrar na fila
        mensagem = matchmaking_service.entrar_na_fila(username)
        if "Erro ao entrar na fila" in mensagem:
            return jsonify({"success": False, "message": mensagem}), 409

        # Encontra a sala onde o jogador foi alocado
        sala_atual = next(
            (s for s in matchmaking_service.salas if username in s.jogadores),
            None
        )
        if not sala_atual:
            return jsonify({
                "success": False,
                "message": "Erro interno: jogador não encontrado em nenhuma sala."
            }), 500

        total_na_fila = sum(len(sala.jogadores) for sala in matchmaking_service.salas)

        return jsonify({
            "success": True,
            "message": mensagem,
            "modo": modo,
            "total_na_fila": total_na_fila,
            "max_jogadores": sala_atual.vagas
        }), 200

    @jogo_bp.route("/sair", methods=["POST"])
    def sair_da_fila():
        """
        Permite que um jogador saia da fila de matchmaking.
        Útil quando clica em 'Cancelar' na UI.
        """
        if not request.is_json:
            return jsonify({"success": False, "message": "JSON esperado"}), 400

        username = request.get_json().get("username")
        if not username:
            return jsonify({"success": False, "message": "Username necessário."}), 400

        if matchmaking_service.sair_da_fila(username):
            return jsonify({
                "success": True,
                "message": f"{username} saiu da fila com sucesso."
            }), 200

        return jsonify({
            "success": False,
            "message": "Você não estava na fila."
        }), 400

    @jogo_bp.route("/limpar_usuario", methods=["POST"])
    def limpar_usuario():
        """Remove o jogador de qualquer fila ou sala, mesmo que não esteja na fila."""
        if not request.is_json:
            return jsonify({"success": False, "message": "JSON esperado"}), 400

        username = request.get_json().get("username")
        if not username:
            return jsonify({"success": False, "message": "Username necessário"}), 400

        # Cleanup independente do estado
        matchmaking_service.sair_da_fila(username)
        return jsonify({"success": True, "message": f"Estado de {username} limpo."}), 200

    @jogo_bp.route("/status", methods=["GET"])
    def status():
        """Retorna o status do jogador: se está na fila ou em partida."""
        username = request.args.get("username")
        if not username:
            return jsonify({"error": "Username necessário"}), 400

        em_fila = any(username in sala.jogadores for sala in matchmaking_service.salas)

        # Por enquanto, "em partida" = sala cheia
        em_partida = any(
            username in sala.jogadores and len(sala.jogadores) >= sala.vagas
            for sala in matchmaking_service.salas
        )

        return jsonify({
            "em_fila": em_fila,
            "em_partida": em_partida,
            "total_na_fila": sum(len(s.jogadores) for s in matchmaking_service.salas)
        })

    return jogo_bp
