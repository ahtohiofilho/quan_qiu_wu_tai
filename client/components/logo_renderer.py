# client/components/logo_renderer.py
"""Componente reutilizável para renderizar logotipos dinâmicos baseados no estado de login."""

import imgui
import glfw
from OpenGL.GL import *
from PIL import Image
import os
from pathlib import Path


class LogoRenderer:
    def __init__(self, resources_path="client/resources", janela_ref=None):
        """
        Inicializa o renderizador de logotipos.

        :param resources_path: Caminho base para os recursos (texturas).
        :param janela_ref: Referência à instância da Janela principal (para contexto OpenGL).
        """
        self.resources_path = Path(resources_path)
        self.janela_ref = janela_ref  # Necessário para garantir contexto OpenGL
        self.logged_in = self._check_login_status()
        self._texture_id = None
        self._texture_width = 0
        self._texture_height = 0

    def _check_login_status(self):
        """Verifica se o usuário está logado checando a existência do token."""
        session_file = Path("session.txt")
        return session_file.exists()

    def get_logo_texture_path(self):
        """
        Determina o caminho do logotipo com base no estado de login.

        :return: Path para o arquivo de textura.
        """
        if self.logged_in:
            logo_path = self.resources_path / "logo_logged_in.png"  # Smile
        else:
            logo_path = self.resources_path / "logo_default.png"  # Login

        # Se o logotipo específico não existir, usa um genérico
        if not logo_path.exists():
            logo_path = self.resources_path / "logo_generic.png"  # Fallback

        return logo_path

    def _load_texture_from_file(self, image_path):
        """
        Carrega uma textura OpenGL a partir de um arquivo de imagem.
        Esta é a parte que substitui o placeholder.
        """
        try:
            # Carrega a imagem usando PIL
            image = Image.open(image_path)

            # Converte para RGBA se não estiver
            if image.mode != "RGBA":
                image = image.convert("RGBA")

            ix, iy, image_data = image.size[0], image.size[1], image.tobytes()

            # Gera um ID de textura OpenGL
            texture_id = glGenTextures(1)

            # Vincula a textura
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Define parâmetros de textura
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # Carrega os dados da imagem na textura
            glTexImage2D(GL_TEXTURE_2D,0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            glGenerateMipmap(GL_TEXTURE_2D)  # Opcional, mas recomendado
            # Desvincula a textura
            glBindTexture(GL_TEXTURE_2D, 0)

            print(f"[LogoRenderer] Textura carregada com sucesso: {image_path} (ID: {texture_id})")
            return texture_id, ix, iy

        except Exception as e:
            print(f"[LogoRenderer] Erro ao carregar textura '{image_path}': {e}")
            # Retorna um ID inválido e dimensões 0
            return 0, 0, 0

    def load_texture(self):
        """
        Carrega a textura apropriada com base no estado de login.
        """
        if self.janela_ref is None:
            print("[LogoRenderer] Erro: janela_ref não fornecida. Necessário para contexto OpenGL.")
            return 0

        # Certifique-se de estar no contexto OpenGL correto (importante!)
        # glfw.make_context_current(self.janela_ref.window) # Geralmente já está ativo no loop principal

        logo_path = self.get_logo_texture_path()
        texture_id, width, height = self._load_texture_from_file(logo_path)

        self._texture_id = texture_id
        self._texture_width = width
        self._texture_height = height

        return texture_id

    def render(self, width=None, height=None, center_x=None, center_y=None):
        """
        Renderiza o logotipo usando Dear ImGui.

        :param width: Largura desejada do logotipo. Se None, usa largura original.
        :param height: Altura desejada do logotipo. Se None, usa altura original.
        :param center_x: Posição X central da tela (para centralizar).
        :param center_y: Posição Y central da tela (para centralizar).
        """
        # Se a textura ainda não foi carregada, carrega agora
        if self._texture_id is None or self._texture_id == 0:
            self.load_texture()
            # Se ainda falhar, não renderiza nada
            if self._texture_id is None or self._texture_id == 0:
                print("[LogoRenderer] Não foi possível carregar a textura para renderização.")
                return False  # Indica que não foi renderizado

        # Determina as dimensões finais
        final_width = width if width is not None else self._texture_width
        final_height = height if height is not None else self._texture_height

        # Calcula a posição se centralização for solicitada
        if center_x is not None and center_y is not None:
            cursor_x = center_x - (final_width / 2)
            cursor_y = center_y - (final_height / 2) - 50  # 50 pixels acima do centro
            imgui.set_cursor_pos((cursor_x, cursor_y))

        # Verifica se a textura é válida antes de tentar renderizar
        if self._texture_id > 0:
            # Finalmente, renderiza a imagem usando o ID da textura OpenGL
            # imgui.image espera o ID da textura, largura e altura
            imgui.image(self._texture_id, final_width, final_height)
            rendered = True
        else:
            # Placeholder se a textura falhar
            print("[LogoRenderer] Renderizando placeholder para logotipo.")
            imgui.dummy(final_width, final_height)
            rendered = False

        # Espaço reservado para garantir layout
        imgui.dummy(final_width, final_height)

        return rendered  # Retorna se foi renderizado com sucesso

    def refresh_login_status(self):
        """Atualiza o estado de login e recarrega a textura se necessário."""
        old_status = self.logged_in
        self.logged_in = self._check_login_status()
        if old_status != self.logged_in:
            # Se o status mudou, invalida a textura atual para forçar recarregamento
            if self._texture_id is not None and self._texture_id > 0:
                glDeleteTextures([self._texture_id])  # Libera a textura OpenGL anterior
            self._texture_id = None
            print(f"[LogoRenderer] Status de login atualizado: {'Logado' if self.logged_in else 'Não logado'}")


# === Como usar no EstadoMenuPrincipal (client/states/main_menu.py) ===
"""
# No __init__ do EstadoMenuPrincipal:
# Certifique-se de importar o componente
# from client.components.logo_renderer import LogoRenderer

def __init__(self, mudar_estado_callback, janela_ref):
    self.mudar_estado = mudar_estado_callback
    self.janela_ref = janela_ref
    # Passa a referência da janela para o LogoRenderer
    self.logo_renderer = LogoRenderer(janela_ref=self.janela_ref) 

# No método atualizar_e_renderizar:
def atualizar_e_renderizar(self):
    # ... (código existente para barras e áreas) ...
    central_x, central_y, central_w, central_h = self._renderizar_barras_e_areas()

    # ... (código existente para janela central) ...
    imgui.begin("##CentralPlayArea", flags=...)

    # --- Renderiza o logotipo ---
    # Centraliza na área central
    center_x_area = central_x + central_w / 2.0
    center_y_area = central_y + central_h / 2.0

    # Opcional: Atualiza o status de login dinamicamente (útil se login/logout acontecer)
    # self.logo_renderer.refresh_login_status() 

    # Renderiza com dimensões desejadas (ex: 150x150)
    self.logo_renderer.render(width=150, height=150, center_x=center_x_area, center_y=center_y_area)
    # ----------------------------

    # ... (restante do código do menu) ...
    imgui.end()
"""
```