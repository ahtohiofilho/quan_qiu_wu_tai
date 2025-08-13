import glfw
from OpenGL.GL import *
import sys


class Janela:
    def __init__(self, width=800, height=600, title="OpenGL Fullscreen"):
        self.width = width
        self.height = height
        self.title = title
        self.window = None

        # Inicializa o GLFW
        if not glfw.init():
            raise Exception("Falha ao inicializar o GLFW")

        # Configurações da janela (OpenGL 3.3 Core Profile)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)  # Necessário no macOS

        # Obter o monitor primário e modo de vídeo
        self.monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(self.monitor)
        self.width = mode.size.width
        self.height = mode.size.height

        # Criar janela em fullscreen
        self.window = glfw.create_window(
            self.width, self.height, self.title, self.monitor, None
        )
        if not self.window:
            glfw.terminate()
            raise Exception("Falha ao criar a janela")

        # Tornar o contexto OpenGL atual
        glfw.make_context_current(self.window)

        # Capturar teclado (para ESC)
        glfw.set_key_callback(self.window, self.key_callback)

        # Habilitar vsync
        glfw.swap_interval(1)

        print(f"Janela em fullscreen: {self.width}x{self.height}")

    def key_callback(self, window, key, scancode, action, mods):
        """Callback para teclas"""
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def setup_opengl(self):
        """Configurações iniciais do OpenGL"""
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.1, 0.1, 0.4, 1.0)  # Fundo azul escuro

    def main_loop(self):
        """Loop principal de renderização"""
        self.setup_opengl()

        while not glfw.window_should_close(self.window):
            # Processar eventos
            glfw.poll_events()

            # Limpar tela
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Aqui você pode adicionar sua renderização (shaders, buffers, etc.)

            # Trocar buffers
            glfw.swap_buffers(self.window)

        self.terminate()

    def terminate(self):
        """Encerra o GLFW"""
        glfw.destroy_window(self.window)
        glfw.terminate()
        print("Aplicação encerrada.")

    def run(self):
        """Inicia a aplicação"""
        self.main_loop()


# === Execução ===
if __name__ == "__main__":
    app = Janela(title="Minha Janela Fullscreen")
    app.run()
    sys.exit()