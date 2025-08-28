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
        print(f"🔔 Rota /jogo/sair chamada")
        if not request.is_json:
            print(f"❌ Requisição não é JSON")
            return jsonify({"success": False, "message": "JSON esperado"}), 400

        username = request.get_json().get("username")
        if not username:
            print(f"⚠️ Username ausente")
            return jsonify({"success": False, "message": "Username necessário."}), 400

        if matchmaking_service.sair_da_fila(username):
            print(f"✅ {username} saiu da fila com sucesso.")
            return jsonify({
                "success": True,
                "message": f"{username} saiu da fila com sucesso."
            }), 200
        print(f"⚠️ {username} não estava na fila.")
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

    @jogo_bp.route("/estado", methods=["POST"])
    def estado_jogador():
        """
        Retorna o estado atual do jogador: se está na fila, em partida ou livre.
        Útil para o cliente decidir qual UI mostrar.
        """
        print("🔵 [DEBUG] /jogo/estado: Requisição recebida")

        # 1. Verificar se o corpo é JSON
        if not request.is_json:
            print("🔴 [DEBUG] /jogo/estado: Requisição não é JSON")
            return jsonify({"error": "JSON esperado."}), 400

        # 2. Extrair o username
        data = request.get_json()
        print(f"🔵 [DEBUG] /jogo/estado: Dados recebidos: {data}")

        username = data.get("username")
        if not username:
            print("🔴 [DEBUG] /jogo/estado: Username ausente no JSON")
            return jsonify({"error": "Username necessário."}), 400

        print(f"🟢 [DEBUG] /jogo/estado: Consultando estado do jogador: {username}")

        # 3. Verificar no MatchmakingService
        try:
            # Verifica se está em alguma sala (na fila)
            em_fila = any(username in sala.jogadores for sala in matchmaking_service.salas)
            print(f"🔵 [DEBUG] /jogo/estado: em_fila = {em_fila}")

            # Verifica se está em uma partida (sala cheia)
            em_partida = any(
                username in sala.jogadores and len(sala.jogadores) >= sala.vagas
                for sala in matchmaking_service.salas
            )
            print(f"🔵 [DEBUG] /jogo/estado: em_partida = {em_partida}")

            # Conta o total na fila
            total_na_fila = sum(len(sala.jogadores) for sala in matchmaking_service.salas)
            print(f"🟢 [DEBUG] /jogo/estado: total_na_fila = {total_na_fila}")

            # Detalhar cada sala (para depuração profunda)
            for i, sala in enumerate(matchmaking_service.salas):
                jogadores = sala.jogadores
                vagas = sala.vagas
                cheia = len(jogadores) >= vagas
                tem_usuario = username in jogadores
                print(
                    f"🔍 [DEBUG] /jogo/estado: Sala {i}: jogadores={jogadores}, vagas={vagas}, cheia={cheia}, tem_usuario={tem_usuario}")

        except Exception as e:
            print(f"❌ [DEBUG] /jogo/estado: Erro ao verificar estado: {e}")
            return jsonify({"error": "Erro interno ao verificar estado."}), 500

        # 4. Retornar resposta
        response_data = {
            "success": True,
            "username": username,
            "em_fila": em_fila,
            "em_partida": em_partida,
            "total_na_fila": total_na_fila
        }
        print(f"🟢 [DEBUG] /jogo/estado: Resposta enviada: {response_data}")

        return jsonify(response_data), 200

    @jogo_bp.route("/debug/salas", methods=["GET"])
    def debug_salas():
        """Rota de depuração: mostra o estado de todas as salas."""
        with matchmaking_service.lock:
            salas_info = []
            for i, sala in enumerate(matchmaking_service.salas):
                with sala.lock:  # Acessa o estado interno da sala com segurança
                    salas_info.append({
                        "indice": i,
                        "id_mundo": sala.mundo.id_mundo,
                        "vagas": sala.vagas,
                        "jogadores": sala.jogadores.copy(),  # Cópia segura
                        "tamanho": len(sala.jogadores),
                        "esta_cheia": len(sala.jogadores) >= sala.vagas
                    })
            return jsonify({
                "success": True,
                "total_salas": len(salas_info),
                "salas": salas_info
            }), 200

    @jogo_bp.route("/minha_sala", methods=["POST"])
    def minha_sala():
        """Retorna o estado da sala do jogador: jogadores, vagas, se está cheia."""
        if not request.is_json:
            return jsonify({"error": "JSON esperado."}), 400

        username = request.get_json().get("username")
        if not username:
            return jsonify({"error": "Username necessário."}), 400

        # Procurar a sala onde o jogador está
        for sala in matchmaking_service.salas:
            if username in sala.jogadores:
                return jsonify({
                    "em_fila": True,
                    "jogadores_na_sala": sala.jogadores.copy(),
                    "vagas": sala.vagas,
                    "esta_cheia": len(sala.jogadores) >= sala.vagas
                })

        # Se não está em nenhuma sala
        return jsonify({
            "em_fila": False,
            "jogadores_na_sala": [],
            "vagas": 0,
            "esta_cheia": False
        }), 200

    return jogo_bp