#!/usr/bin/env python3
"""
Ponto de entrada principal do projeto Global Arena.

Comandos disponíveis:
    python start.py server           → Inicia o servidor Flask
    python start.py client           → Inicia o cliente gráfico do jogador
    python start.py interface        → Abre a interface de administração do servidor
    python start.py init             → Reinicializa a infra AWS
    python start.py create-world     → Cria e faz upload de um novo mundo
    python start.py test             → Testa conexão com AWS
    python start.py simulador        → Simula entrada de players online (teste de carga)
"""

import sys
from pathlib import Path
import argparse
import signal

# Adiciona o diretório raiz ao caminho de imports
sys.path.insert(0, str(Path(__file__).parent))


def main():
    parser = argparse.ArgumentParser(description="🌍 Global Arena - Sistema de inicialização central")
    parser.add_argument(
        'command',
        choices=['server', 'client', 'interface', 'init', 'create-world', 'test', 'simulador'],
        help="Comando a ser executado"
    )
    parser.add_argument('--fator', type=int, default=4, help="Fator do mundo (nível de detalhe)")
    parser.add_argument('--bioma', type=str, default="Meadow", help="Bioma inicial para capitais")

    args = parser.parse_args()

    try:
        if args.command == 'server':
            print("🚀 Iniciando servidor Flask...")
            from server.app import create_app
            app = create_app('development')

            # DEBUG: Listar todas as rotas registradas
            print("\n📋 Rotas registradas no app (debug real):")
            for rule in app.url_map.iter_rules():
                print(f"  {rule.rule} -> {rule.endpoint}")
            print("\n")

            print("✅ Servidor configurado. Acesse em http://127.0.0.1:5000")
            app.run(host='127.0.0.1', port=5000, debug=False)

        elif args.command == 'client':
            print("🎮 Iniciando cliente gráfico (jogador)...")
            from client.main import main as client_main
            client_main()

        elif args.command == 'interface':
            print("🔧 Abrindo interface de administração do servidor...")
            from server.core.interface import Interface
            from PyQt6.QtWidgets import QApplication
            app = QApplication(sys.argv)
            window = Interface()
            window.show()
            print("✅ Interface de administração carregada.")
            sys.exit(app.exec())

        elif args.command == 'init':
            print("🔧 Reinicializando infraestrutura AWS...")
            from server.config.initializer import InicializadorAWS
            from server.integrations.aws_loader import AWSLoader
            loader = AWSLoader(region_name='us-east-2')
            inicializador = InicializadorAWS(loader)
            sucesso = inicializador.inicializar(confirmar=True)
            if sucesso:
                print("✅ Infraestrutura AWS reinicializada com sucesso.")
            else:
                print("❌ Falha ao reinicializar a infraestrutura AWS.")
                sys.exit(1)

        elif args.command == 'create-world':
            print(f"🌍 Criando novo mundo com fator={args.fator}, bioma='{args.bioma}'...")
            from server.core.commander import Comandante
            from server.integrations.aws_loader import AWSLoader
            from server.core.manager import Gerenciador

            loader = AWSLoader(region_name='us-east-2')
            gerenciador = Gerenciador(loader)  # ✅ Correto: Comandante precisa do Gerenciador
            comandante = Comandante(gerenciador, loader)  # ✅ Agora está correto

            # Usar o método correto com retorno
            sucesso, mundo = comandante.criar_e_upload_mundo_com_retorno(
                fator=args.fator,
                bioma=args.bioma
            )
            if sucesso:
                print(f"✅ Mundo {mundo.id_mundo} criado e enviado para AWS com sucesso.")
            else:
                print("❌ Falha ao criar ou enviar o mundo.")
                sys.exit(1)

        elif args.command == 'test':
            print("🧪 Testando conexão com AWS...")
            from server.integrations.aws_loader import AWSLoader
            loader = AWSLoader(region_name='us-east-2')
            try:
                account = loader.get_account_info()
                print(f"✅ Conectado à AWS: Conta {account['account_id']}")
                buckets = loader.list_s3_buckets()
                print(f"📦 Buckets S3: {len(buckets)} encontrados.")
                tables = loader.list_dynamodb_tables()
                print(f"📊 Tabelas DynamoDB: {len(tables)} encontradas.")
            except Exception as e:
                print(f"❌ Erro ao conectar à AWS: {e}")
                sys.exit(1)

        elif args.command == 'simulador':
            print("🎮 Iniciando simulador de players online...")
            print("💡 Pressione Ctrl+C para encerrar a simulação.")
            from server.core.simulador_players import simular_entrada_periodica
            try:
                # Captura Ctrl+C de forma limpa
                simular_entrada_periodica(intervalo_min=2, intervalo_max=8)
            except KeyboardInterrupt:
                print("\n🛑 Simulador de players encerrado pelo usuário.")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Erro no simulador: {e}")
                sys.exit(1)

    except ModuleNotFoundError as e:
        print(f"❌ Módulo não encontrado: {e}")
        print("💡 Dica: certifique-se de estar na raiz do projeto.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# Garante que Ctrl+C funcione corretamente
def signal_handler(signum, frame):
    print("\n🛑 Sinal recebido. Encerrando...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    main()