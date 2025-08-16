# client/window.py
import glfw
from OpenGL.GL import *
import sys
import imgui
# Importa o backend GlfwRenderer. Este é o ponto chave.
# Se o import falhar, significa que `imgui` ou o backend específico não está instalado corretamente.
from imgui.integrations.glfw import GlfwRenderer
# Corrigir a importação do glm também
from pyglm import glm


class Janela:
    def __init__(self, title="Global Arena"):
        self.title = title
        self.window = None
        self.monitor = None
        self.imgui_impl = None  # Vai armazenar o backend do ImGui

        # Inicializa o GLFW
        if not glfw.init():
            raise Exception("Falha ao inicializar o GLFW")

        # Configurações da janela (OpenGL 3.3 Core Profile)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)  # Necessário no macOS

        # Modo fullscreen com resolução nativa
        self.monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(self.monitor)
        self.width = mode.size.width
        self.height = mode.size.height

        # Criar janela em fullscreen
        self.window = glfw.create_window(self.width, self.height, self.title, self.monitor, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Falha ao criar a janela")

        # Tornar o contexto OpenGL atual
        glfw.make_context_current(self.window)

        # === INICIALIZAÇÃO DO DEAR IMGUI ===
        # 1. Criar contexto do ImGui
        imgui.create_context()
        # 2. Criar o backend de renderização.
        # Usando attach_callbacks=True (padrão) para que ele gerencie os callbacks automaticamente.
        # Isso elimina a necessidade de chamar manualmente imgui_impl.algum_callback.
        self.imgui_impl = GlfwRenderer(self.window, attach_callbacks=True)

        # === CALLBACKS (apenas os específicos da sua aplicação, se necessário) ===
        # Capturar teclado (para ESC). O ImGui receberá os eventos automaticamente.
        glfw.set_key_callback(self.window, self._key_callback)
        # Se você precisar de callbacks adicionais para lógica específica (além do ImGui),
        # pode adicioná-los aqui. Mas os básicos (mouse, teclado) são tratados pelo backend.

        # Habilitar vsync
        glfw.swap_interval(1)

        # Estados de input (opcional, pode ser simplificado ou removido se usar ImGui para input)
        # Se você não usar mais esses estados, pode removê-los.
        self.keys = {}
        self.mouse_b1_pressed = False
        self.mouse_x = 0.0
        self.mouse_y = 0.0

        # === ESCALA E PROJEÇÃO ===
        self.base_resolution = (1600, 900)
        self.scale = self.width / self.base_resolution[0]
        self.projection_matrix = glm.ortho(
            0.0, float(self.width),
            float(self.height), 0.0,
            -1.0, 1.0
        )

        self.ui_sidebar_width = 320  # Largura das barras laterais
        self.ui_toolbar_height = 30  # Altura das barras superior e inferior

        print(f"🎮 Janela criada em fullscreen: {self.width}x{self.height}")
        print(f"📐 Escala de UI: {self.scale:.2f}x (base: {self.base_resolution[0]}x{self.base_resolution[1]})")
        print("🎨 Dear ImGui inicializado.")

    # === CALLBACKS PARA LÓGICA ESPECÍFICA DA APLICAÇÃO ===
    # O backend do ImGui já está ouvindo esses eventos.
    def _key_callback(self, window, key, scancode, action, mods):
        """Callback para teclas — fecha com ESC"""
        # Lógica específica da sua aplicação
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    # Se você não precisar mais desses callbacks para lógica própria, pode removê-los.
    # O backend do ImGui os trata.
    # def _mouse_position_callback(self, window, xpos, ypos):
    #     """Atualiza posição do mouse"""
    #     # O ImGui já processa isso. Se precisar para lógica própria:
    #     self.mouse_x = xpos
    #     self.mouse_y = self.height - ypos  # Inverte Y: 0 no topo

    # def _mouse_button_callback(self, window, button, action, mods):
    #     """Detecta clique do botão esquerdo"""
    #     # O ImGui já processa isso. Se precisar para lógica própria:
    #     if button == glfw.MOUSE_BUTTON_LEFT:
    #         self.mouse_b1_pressed = (action == glfw.PRESS)

    # === MÉTODOS PARA INTEGRAR IMGUI NO LOOP ===
    def processar_eventos(self):
        """Processa eventos do GLFW e inicia o frame do ImGui"""
        # O backend do ImGui (com attach_callbacks=True) já processou os eventos de input.
        glfw.poll_events()
        # Inicia um novo frame do ImGui
        if self.imgui_impl:
            # self.imgui_impl.process_inputs() # Geralmente chamado internamente por new_frame no backend
            imgui.new_frame()

    def trocar_buffers(self):
        """Renderiza a interface ImGui e troca os buffers"""
        # Finaliza o frame do ImGui e obtém os dados de renderização
        imgui.render()
        if self.imgui_impl:
            # O backend desenha a interface ImGui usando OpenGL
            self.imgui_impl.render(imgui.get_draw_data())

        glfw.swap_buffers(self.window)

    # === FINALIZAÇÃO ===
    def terminar(self):
        """Libera recursos do GLFW e do ImGui"""
        # Limpa o backend do ImGui primeiro.
        # O shutdown do backend geralmente cuida da destruição do contexto imgui.
        if self.imgui_impl:
            self.imgui_impl.shutdown()
            # Definir como None para evitar uso acidental após shutdown
            self.imgui_impl = None

            # O imgui.destroy_context() pode não ser necessário se o backend já cuidou disso.
        # Mas, para garantir (e evitar o erro se o backend não tiver feito),
        # podemos verificar se o contexto ainda é válido antes de destruí-lo.
        # No entanto, a forma mais segura é confiar no backend e NÃO chamar
        # imgui.destroy_context() manualmente neste ponto.
        #
        # Se você quiser ser explícito, pode fazer uma verificação, mas geralmente
        # não é necessária:
        # contexto_atual = imgui.get_current_context()
        # if contexto_atual is not None:
        #     imgui.destroy_context(contexto_atual) # Destroi o contexto específico

        # Libera recursos do GLFW
        if self.window:
            glfw.destroy_window(self.window)
            self.window = None  # Boa prática
        glfw.terminate()

    # --- Métodos de utilidade para renderização (sem alterações) ---
    # Mantenha esses métodos conforme sua necessidade.
    def definir_viewport(self):
        glViewport(0, 0, self.width, self.height)

    def limpar_tela(self, r=0.1, g=0.1, b=0.4, a=1.0):
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def habilitar_depth_test(self):
        glEnable(GL_DEPTH_TEST)

    def desabilitar_depth_test(self):
        glDisable(GL_DEPTH_TEST)

    def habilitar_blend(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def desabilitar_blend(self):
        glDisable(GL_BLEND)

    # Se você removeu os callbacks de mouse/teclado, pode remover esses métodos também,
    # ou mantê-los se ainda forem usados para alguma lógica específica.
    def get_mouse_position(self):
        """Retorna posição do mouse com origem no canto superior esquerdo"""
        xpos, ypos = glfw.get_cursor_pos(self.window)
        return xpos, self.height - ypos  # Inverte Y

    def is_key_pressed(self, key):
        """Verifica se uma tecla está pressionada"""
        return glfw.get_key(self.window, key) == glfw.PRESS

    def deve_fechar(self):  # <-- Adicionado conforme solicitado
        """Verifica se a janela deve ser fechada."""
        return glfw.window_should_close(self.window)

    # === MÉTODO AUXILIAR PARA TESTE ===
    def renderizar_demo_imgui(self):
        """Renderiza a janela de demonstração do ImGui. Útil para testes."""
        imgui.show_demo_window()
