# simulador_players.py
import requests
import random
import time
import threading

# Lista de usuários simulados (você pode gerar ou registrar previamente)
USUARIOS_SIMULADOS = [
    {"username": "player1", "password": "senha123"},
    {"username": "player2", "password": "senha123"},
    {"username": "player3", "password": "senha123"},
    {"username": "player4", "password": "senha123"},
    {"username": "player5", "password": "senha123"},
]

URL_BASE = "http://localhost:5000"

def login_usuario(usuario):
    try:
        response = requests.post(f"{URL_BASE}/auth/login", json=usuario)
        data = response.json()
        if data.get("success"):
            print(f"✅ {usuario['username']} logou com sucesso.")
            return data.get("token")  # se você implementar tokens no futuro
        else:
            print(f"❌ {usuario['username']} falhou: {data.get('message')}")
            return None
    except Exception as e:
        print(f"⚠️  Erro ao conectar para {usuario['username']}: {e}")
        return None

def entrar_na_fila(usuario):
    token = login_usuario(usuario)
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.post(f"{URL_BASE}/jogo/entrar", json={"modo": "online"}, headers=headers)
        data = response.json()
        print(f"🎮 {usuario['username']} {data.get('message')}")
    except Exception as e:
        print(f"⚠️  Falha ao entrar na fila: {e}")

def simular_entrada_periodica(intervalo_min=2, intervalo_max=5):
    """Simula entrada aleatória de players no sistema."""
    while True:
        usuario = random.choice(USUARIOS_SIMULADOS)
        thread = threading.Thread(target=entrar_na_fila, args=(usuario,), daemon=True)
        thread.start()
        time.sleep(random.randint(intervalo_min, intervalo_max))

if __name__ == "__main__":
    print("🚀 Iniciando simulador de players...")
    simular_entrada_periodica()