# server/simulador_players.py
import requests
import random
import time
import threading

# Configuração
URL_BASE = "http://localhost:5000"
NUM_PLAYERS = 50  # Quantidade de players simulados: player001 até player050

# Gera usuários dinamicamente
USUARIOS_SIMULADOS = [{"username": f"player{i:03d}", "password": "senha123"} for i in range(1, 51)]
print("🎯 Simulador carregado com formatos: player001, player002, ...")

def registrar_usuario(usuario):
    """Tenta registrar o usuário no servidor."""
    try:
        response = requests.post(f"{URL_BASE}/auth/registrar", json=usuario, timeout=3)
        data = response.json()
        if data.get("success"):
            print(f"🆕 Registrado: {usuario['username']}")
            return True
        else:
            # Pode já existir → não é erro
            if "já está em uso" in data.get("message", ""):
                return True
            print(f"❌ Falha ao registrar {usuario['username']}: {data.get('message')}")
            return False
    except Exception as e:
        print(f"⚠️ Erro ao registrar {usuario['username']}: {e}")
        return False

def login_usuario(usuario):
    """Tenta fazer login. Se falhar por usuário não encontrado, tenta registrar."""
    try:
        response = requests.post(f"{URL_BASE}/auth/login", json=usuario, timeout=3)
        data = response.json()

        if data.get("success"):
            print(f"✅ {usuario['username']} logou com sucesso.")
            return data.get("token")  # futuro: JWT
        else:
            mensagem = data.get("message", "")
            if "não encontrado" in mensagem:
                print(f"🔁 {usuario['username']} não existe. Tentando registrar...")
                if registrar_usuario(usuario):
                    return login_usuario(usuario)  # Tenta logar novamente após registrar
            else:
                print(f"❌ {usuario['username']} falhou: {mensagem}")
        return None
    except requests.exceptions.ConnectionError:
        print("🛑 Erro: Não foi possível conectar ao servidor. Certifique-se de que o servidor está rodando em http://localhost:5000")
        return None
    except Exception as e:
        print(f"⚠️ Erro inesperado ao logar {usuario['username']}: {e}")
        return None

def entrar_na_fila(usuario):
    """Após login, entra na fila de jogo online."""
    token = login_usuario(usuario)
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.post(
            f"{URL_BASE}/jogo/entrar",
            json={"modo": "online", "username": usuario["username"]},
            headers=headers,
            timeout=3
        )
        data = response.json()
        print(f"🎮 {usuario['username']} → {data.get('message')}")
    except Exception as e:
        print(f"⚠️ Falha ao entrar na fila: {e}")

def simular_entrada_periodica(intervalo_min=2, intervalo_max=5):
    """
    Simula entrada periódica e aleatória de players no sistema.
    Cada player tenta:
    1. Logar (ou se registrar, se necessário)
    2. Entrar na fila de matchmaking
    """
    print(f"🔄 Iniciando simulação com {len(USUARIOS_SIMULADOS)} players...")
    print(f"💡 Intervalo: {intervalo_min}s a {intervalo_max}s entre tentativas")
    print("ℹ️  Pressione Ctrl+C para parar.")

    while True:
        usuario = random.choice(USUARIOS_SIMULADOS)
        thread = threading.Thread(target=entrar_na_fila, args=(usuario,), daemon=True)
        thread.start()
        time.sleep(random.uniform(intervalo_min, intervalo_max))

if __name__ == "__main__":
    print("🚀 Iniciando simulador de players online...")
    try:
        simular_entrada_periodica(intervalo_min=1.5, intervalo_max=4.0)
    except KeyboardInterrupt:
        print("\n🛑 Simulação encerrada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")