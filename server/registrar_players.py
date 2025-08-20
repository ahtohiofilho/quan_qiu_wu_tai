# server/registrar_players.py
import requests

# Lista de players a serem registrados
USUARIOS = [
    {"username": f"player{i:03d}", "password": "senha123"} for i in range(1, 51)
]

print("📝 Registrando 50 players de teste...")

for usuario in USUARIOS:
    response = requests.post("http://localhost:5000/auth/registrar", json=usuario)
    data = response.json()
    if data.get("success"):
        print(f"✅ {usuario['username']} registrado com sucesso.")
    else:
        # Pode já existir → não é erro
        if "já existe" in data.get("message", ""):
            print(f"🔁 {usuario['username']} já registrado.")
        else:
            print(f"❌ Falha ao registrar {usuario['username']}: {data['message']}")