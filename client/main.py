# client/sei_la_o_que.py
"""Ponto de entrada do cliente gráfico.
Inicializa a janela com suporte Dear ImGui e inicia o loop principal."""
import sys
import imgui
import glfw # Importar glfw no topo
from client.window import Janela
# Importa o novo estado (certifique-se de que o caminho está correto)
# Se o arquivo for client/states/main_menu.py, a importação está correta.
from client.states.main_menu import EstadoMenuPrincipal

def main():
    print("🎮 Inicializando cliente gráfico...")
    try:
        # 1. Criar a janela (com suporte ao Dear ImGui)
        janela = Janela(title="Global Arena - Dear ImGui")

        # === INÍCIO DA GESTÃO DE ESTADOS ===

        # Variável para armazenar o estado atual da UI
        estado_atual_nome = "menu_principal"
        estado_atual_objeto = None

        # Função callback para mudar de estado
        def mudar_estado(novo_estado_nome):
            nonlocal estado_atual_nome, estado_atual_objeto
            print(f"🔁 Mudando estado de '{estado_atual_nome}' para '{novo_estado_nome}'")
            estado_atual_nome = novo_estado_nome

            if novo_estado_nome == "menu_principal":
                # Passa o callback E a referência da janela
                estado_atual_objeto = EstadoMenuPrincipal(mudar_estado, janela)
            elif novo_estado_nome == "offline":
                print("⚠️ Estado 'offline' ainda não implementado.")
            elif novo_estado_nome == "login":
                print("⚠️ Estado 'login' ainda não implementado.")
            elif novo_estado_nome == "sair":
                glfw.set_window_should_close(janela.window, True) # Usar glfw diretamente
            else:
                print(f"❓ Estado '{novo_estado_nome}' desconhecido.")
                estado_atual_nome = "menu_principal"

            if estado_atual_objeto is None and estado_atual_nome not in ["sair"]:
                 print("❗ Objeto do estado não foi criado. Voltando ao menu principal.")
                 estado_atual_nome = "menu_principal"
                 estado_atual_objeto = EstadoMenuPrincipal(mudar_estado, janela) # Passa a janela

        # Inicializa o primeiro estado - AGORA que a função mudar_estado está definida
        mudar_estado("menu_principal")

        print("🔁 Iniciando loop principal...")
        while not janela.deve_fechar():
            # Processa eventos do GLFW e inicia o frame do ImGui
            janela.processar_eventos()

            # Limpar tela
            janela.limpar_tela(r=0.1, g=0.1, b=0.4, a=1.0) # Cor de fundo padrão

            # === INÍCIO DA RENDERIZAÇÃO BASEADA NO ESTADO ===

            # Chama o método de atualização/renderização do estado atual
            if estado_atual_objeto:
                estado_atual_objeto.atualizar_e_renderizar()

            # === FIM DA RENDERIZAÇÃO BASEADA NO ESTADO ===

            # Troca os buffers, renderizando a UI do ImGui
            janela.trocar_buffers()

        print("👋 Cliente encerrado com sucesso.")
        janela.terminar()
        return 0

    except Exception as e:
        print(f"❌ Erro crítico no cliente: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        # Certifique-se de terminar a janela mesmo em caso de erro
        try:
            if 'janela' in locals():
                janela.terminar()
        except:
            pass
        return 1

if __name__ == "__main__":
    sys.exit(main())