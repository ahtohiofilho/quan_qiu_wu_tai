# client/states/main_menu.py
"""Estado: Menu Principal do Jogo"""
import imgui

class EstadoMenuPrincipal:
    """
    Representa o estado da UI quando o menu principal está ativo.
    Layout: Barras Superior/Inferior (90px), Laterais (320px), Área Central para conteúdo.
    A barra lateral direita comporta um banner 300x600.
    """

    def __init__(self, mudar_estado_callback, janela_ref):
        """
        :param mudar_estado_callback: Função para chamar quando se quer mudar de estado.
        :param janela_ref: Referência à instância da Janela principal.
        """
        self.mudar_estado = mudar_estado_callback
        self.janela_ref = janela_ref

    def _renderizar_barras_e_areas(self):
        """Renderiza as barras fixas (com efeito 3D) e define a área central jogável."""
        screen_width = self.janela_ref.width
        screen_height = self.janela_ref.height
        sidebar_w = self.janela_ref.ui_sidebar_width
        toolbar_h = self.janela_ref.ui_toolbar_height

        # --- Obter a lista de desenho da tela principal para desenhar barras ---
        draw_list = imgui.get_background_draw_list()

        # --- Definir cores para o efeito de luz/sombra nas barras ---
        bar_color_base = imgui.get_color_u32_rgba(0.12, 0.12, 0.12, 0.9)   # Cor base da barra
        bar_color_light = imgui.get_color_u32_rgba(0.25, 0.25, 0.25, 0.9)   # Cor de luz (topo/esquerda)
        bar_color_shadow = imgui.get_color_u32_rgba(0.05, 0.05, 0.05, 0.9)  # Cor de sombra (base/direita)
        border_thickness = 2.0  # Espessura das linhas de luz/sombra

        # --- 1. Barra Superior (com efeito 3D) ---
        # 1.1. Desenhar o retângulo principal
        draw_list.add_rect_filled(0, 0, screen_width, toolbar_h, bar_color_base)
        # 1.2. Linha de luz no topo
        draw_list.add_line(0, 0, screen_width, 0, bar_color_light, thickness=border_thickness)
        # 1.3. Linha de luz à esquerda (vertical)
        draw_list.add_line(0, 0, 0, toolbar_h, bar_color_light, thickness=border_thickness)
        # 1.4. Linha de sombra na base
        draw_list.add_line(0, toolbar_h - border_thickness, screen_width, toolbar_h - border_thickness,
                           bar_color_shadow, thickness=border_thickness)
        # 1.5. Linha de sombra à direita (vertical)
        draw_list.add_line(screen_width - border_thickness, 0, screen_width - border_thickness, toolbar_h,
                           bar_color_shadow, thickness=border_thickness)

        # --- 2. Barra Inferior (com efeito 3D) ---
        draw_list.add_rect_filled(0, screen_height - toolbar_h, screen_width, screen_height, bar_color_base)
        draw_list.add_line(0, screen_height - toolbar_h, screen_width, screen_height - toolbar_h,
                           bar_color_light, thickness=border_thickness)
        draw_list.add_line(0, screen_height - toolbar_h, 0, screen_height,
                           bar_color_light, thickness=border_thickness)
        draw_list.add_line(0, screen_height - border_thickness, screen_width, screen_height - border_thickness,
                           bar_color_shadow, thickness=border_thickness)
        draw_list.add_line(screen_width - border_thickness, screen_height - toolbar_h,
                           screen_width - border_thickness, screen_height,
                           bar_color_shadow, thickness=border_thickness)

        # --- 3. Barra Lateral Esquerda (com efeito 3D) ---
        sidebar_height = screen_height - 2 * toolbar_h
        draw_list.add_rect_filled(0, toolbar_h, sidebar_w, toolbar_h + sidebar_height, bar_color_base)
        draw_list.add_line(0, toolbar_h, sidebar_w, toolbar_h,
                           bar_color_light, thickness=border_thickness)
        draw_list.add_line(0, toolbar_h, 0, toolbar_h + sidebar_height,
                           bar_color_light, thickness=border_thickness)
        draw_list.add_line(0, toolbar_h + sidebar_height - border_thickness,
                           sidebar_w, toolbar_h + sidebar_height - border_thickness,
                           bar_color_shadow, thickness=border_thickness)
        draw_list.add_line(sidebar_w - border_thickness, toolbar_h,
                           sidebar_w - border_thickness, toolbar_h + sidebar_height,
                           bar_color_shadow, thickness=border_thickness)

        # --- 4. Barra Lateral Direita (para o Banner) (com efeito 3D) ---
        draw_list.add_rect_filled(screen_width - sidebar_w, toolbar_h,
                                  screen_width, toolbar_h + sidebar_height, bar_color_base)
        draw_list.add_line(screen_width - sidebar_w, toolbar_h, screen_width, toolbar_h,
                           bar_color_light, thickness=border_thickness)
        draw_list.add_line(screen_width - sidebar_w, toolbar_h,
                           screen_width - sidebar_w, toolbar_h + sidebar_height,
                           bar_color_light, thickness=border_thickness)
        draw_list.add_line(screen_width - sidebar_w, toolbar_h + sidebar_height - border_thickness,
                           screen_width, toolbar_h + sidebar_height - border_thickness,
                           bar_color_shadow, thickness=border_thickness)
        draw_list.add_line(screen_width - border_thickness, toolbar_h,
                           screen_width - border_thickness, toolbar_h + sidebar_height,
                           bar_color_shadow, thickness=border_thickness)

        # --- 6. Agora, criar as janelas ImGui INVISÍVEIS sobre as barras para colocar texto ---
        # --- 6.1. Barra Superior (Janela invisível para texto) ---
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(screen_width, toolbar_h)
        imgui.begin("##TopToolbar", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE |
                                      imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE |
                                      imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_BACKGROUND |
                                      imgui.WINDOW_NO_SCROLL_WITH_MOUSE)
        text = "Barra Superior (90px)"
        text_size = imgui.calc_text_size(text).x
        imgui.set_cursor_pos_x((imgui.get_window_width() - text_size) / 2.0)
        imgui.text(text)
        imgui.end()

        # --- 6.2. Barra Inferior ---
        imgui.set_next_window_position(0, screen_height - toolbar_h)
        imgui.set_next_window_size(screen_width, toolbar_h)
        imgui.begin("##BottomToolbar", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE |
                                         imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE |
                                         imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_BACKGROUND |
                                         imgui.WINDOW_NO_SCROLL_WITH_MOUSE)
        text = "Barra Inferior (90px)"
        text_size = imgui.calc_text_size(text).x
        imgui.set_cursor_pos_x((imgui.get_window_width() - text_size) / 2.0)
        imgui.text(text)
        imgui.end()

        # --- 6.3. Barra Lateral Esquerda ---
        imgui.set_next_window_position(0, toolbar_h)
        imgui.set_next_window_size(sidebar_w, sidebar_height)
        imgui.begin("##LeftSidebar", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE |
                                      imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE |
                                      imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_BACKGROUND |
                                      imgui.WINDOW_NO_SCROLL_WITH_MOUSE)
        text = "Barra Lateral Esquerda (320px)"
        text_size = imgui.calc_text_size(text).x
        imgui.set_cursor_pos_x((imgui.get_window_width() - text_size) / 2.0)
        imgui.dummy(0.0, 20.0)
        imgui.set_cursor_pos_x((imgui.get_window_width() - text_size) / 2.0)
        imgui.text(text)
        imgui.end()

        # --- 6.4. Barra Lateral Direita (para o Banner) ---
        imgui.set_next_window_position(screen_width - sidebar_w, toolbar_h)
        imgui.set_next_window_size(sidebar_w, sidebar_height)
        imgui.begin("##RightBannerArea", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE |
                                          imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE |
                                          imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_BACKGROUND |
                                          imgui.WINDOW_NO_SCROLL_WITH_MOUSE)

        # --- 6.4.1. Conteúdo da Barra Direita: O Banner 300x600 ---
        # Calcular posição para centralizar o banner de 300x600 dentro da barra de 320px de largura
        banner_width = 300
        banner_height = 600
        banner_x_offset = (sidebar_w - banner_width) / 2.0 # Centraliza horizontalmente
        banner_y_offset = max(0, (sidebar_height - banner_height) / 2.0) # Centraliza verticalmente

        # --- Efeito 3D para o Banner Placeholder ---
        # Cores para o banner placeholder
        banner_color_base = imgui.get_color_u32_rgba(0.2, 0.2, 0.3, 0.7)    # Base do banner
        banner_color_light = imgui.get_color_u32_rgba(0.3, 0.3, 0.4, 0.7)   # Luz
        banner_color_shadow = imgui.get_color_u32_rgba(0.1, 0.1, 0.2, 0.7)  # Sombra

        # Obter a posição absoluta da tela para a janela da barra direita
        window_pos_x, window_pos_y = imgui.get_window_position()
        # Coordenadas absolutas do retângulo do banner
        banner_abs_x = window_pos_x + banner_x_offset
        banner_abs_y = window_pos_y + banner_y_offset

        # 1. Desenhar o retângulo principal do banner
        draw_list.add_rect_filled(banner_abs_x, banner_abs_y,
                                  banner_abs_x + banner_width, banner_abs_y + banner_height,
                                  banner_color_base)
        # 2. Linha de luz no topo
        draw_list.add_line(banner_abs_x, banner_abs_y,
                           banner_abs_x + banner_width, banner_abs_y,
                           banner_color_light, thickness=border_thickness)
        # 3. Linha de luz à esquerda
        draw_list.add_line(banner_abs_x, banner_abs_y,
                           banner_abs_x, banner_abs_y + banner_height,
                           banner_color_light, thickness=border_thickness)
        # 4. Linha de sombra na base
        draw_list.add_line(banner_abs_x, banner_abs_y + banner_height - border_thickness,
                           banner_abs_x + banner_width, banner_abs_y + banner_height - border_thickness,
                           banner_color_shadow, thickness=border_thickness)
        # 5. Linha de sombra à direita
        draw_list.add_line(banner_abs_x + banner_width - border_thickness, banner_abs_y,
                           banner_abs_x + banner_width - border_thickness, banner_abs_y + banner_height,
                           banner_color_shadow, thickness=border_thickness)
        # --- Fim do Efeito 3D para o Banner ---

        # Adicionar texto dentro da área do banner (janela invisível)
        imgui.set_cursor_pos((banner_x_offset, banner_y_offset))
        imgui.text("Banner 300x600")
        placeholder_text = "[BANNER PLACEHOLDER]"
        text_size_x = imgui.calc_text_size(placeholder_text).x
        text_size_y = imgui.calc_text_size(placeholder_text).y
        imgui.set_cursor_pos((
            banner_x_offset + (banner_width - text_size_x) / 2.0,
            banner_y_offset + (min(banner_height, sidebar_height) - text_size_y) / 2.0
        ))
        imgui.text(placeholder_text)

        imgui.end()

        # --- 7. Área Jogável Central ---
        central_area_x = sidebar_w
        central_area_y = toolbar_h
        central_area_width = screen_width - 2 * sidebar_w
        central_area_height = screen_height - 2 * toolbar_h

        # Retorna as dimensões para que outros elementos possam ser posicionados dentro
        return central_area_x, central_area_y, central_area_width, central_area_height

    def atualizar_e_renderizar(self):
        """
        Método chamado a cada frame para atualizar a lógica (se houver)
        e renderizar a interface do menu principal dentro do layout definido.
        """
        # --- 1. Renderizar as áreas fixas e obter dimensões da área central ---
        central_x, central_y, central_w, central_h = self._renderizar_barras_e_areas()

        # --- 2. Conteúdo da Área Jogável Central (Menu Principal) ---
        imgui.set_next_window_position(central_x, central_y)
        imgui.set_next_window_size(central_w, central_h)
        imgui.begin("##CentralPlayArea", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE |
                                                       imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE |
                                                       imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_BACKGROUND)

        # --- 3. Posicionar elementos do menu dentro da área central ---
        menu_block_height = 300.0
        start_y = central_y + (central_h - menu_block_height) / 2.0
        button_width = 250.0
        button_x = central_x + (central_w - button_width) / 2.0

        # --- Título Centralizado na Área Central ---
        title_text = "GLOBAL ARENA"
        title_size = imgui.calc_text_size(title_text)
        title_x = central_x + (central_w - title_size.x) / 2.0
        imgui.set_cursor_pos((title_x - central_x, start_y - 100 - central_y))
        imgui.text(title_text)

        # --- Botões ---
        # Botão "Offline"
        imgui.set_cursor_pos((button_x - central_x, start_y - central_y))
        imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 5.0)
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (15.0, 15.0))
        if imgui.button("Offline", width=button_width, height=60):
            print("Botão 'Offline' clicado.")
            self.mudar_estado("offline")

        # Botão "Online"
        imgui.set_cursor_pos((button_x - central_x, start_y + 80 - central_y))
        if imgui.button("Online", width=button_width, height=60):
            print("Botão 'Online' clicado.")
            self.mudar_estado("login")

        # Botão "Sair" (estilo vermelho)
        imgui.set_cursor_pos((button_x - central_x, start_y + 160 - central_y))
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.7, 0.2, 0.2, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.8, 0.3, 0.3, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.9, 0.1, 0.1, 1.0)
        if imgui.button("Sair", width=button_width, height=60):
            print("Botão 'Sair' clicado.")
            self.mudar_estado("sair")
        imgui.pop_style_color(3)

        imgui.pop_style_var(2)

        # --- Finaliza a janela da área central ---
        imgui.end()
