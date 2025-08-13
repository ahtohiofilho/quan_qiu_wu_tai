# client/aws_loader.py

"""
Ponto de entrada do cliente gráfico.
Inicializa a janela OpenGL em fullscreen e inicia o loop principal.
"""

import sys
from client.window import Janela


def main():
    """
    Função principal do cliente.
    Cria a janela e inicia o loop de renderização.
    """
    print("Inicializando cliente gráfico...")

    try:
        # Cria a janela em fullscreen
        app = Janela(title="Cliente OpenGL - Fullscreen")

        # Inicia o loop principal (renderização + eventos)
        app.run()

        print("Cliente encerrado com sucesso.")
        return 0

    except Exception as e:
        print(f"Erro crítico no cliente: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Executa a aplicação e retorna código de saída
    sys.exit(main())