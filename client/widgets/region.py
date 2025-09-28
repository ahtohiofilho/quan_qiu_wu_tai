# client/widgets/region.py
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QImage, QColor, QPainter, QMouseEvent
from PyQt6.QtCore import Qt, QPoint, pyqtSignal # Adicionado pyqtSignal

class Regiao(QWidget):
    """
    Widget para overlays regionais em tiles (hexágonos/pentágonos).
    Mostra uma máscara diferente ao passar o mouse em regiões definidas por cores em uma imagem.
    Agora com correção de centralização para o color picking e para o overlay.
    Agora detecta clique esquerdo e emite sinal.
    """
    region_clicked = pyqtSignal(str)
    def __init__(self, mask_image_path, region_color_map, parent=None):
        """
        :param mask_image_path: Caminho para a imagem da máscara colorida (PNG).
        :param region_color_map: Dict mapeando (QColor ou RGB tuple) para nome/código da região.
        """
        super().__init__(parent)
        self.mask_image = QImage(mask_image_path)
        if self.mask_image.isNull():
             print(f"❌ [Regiao] Falha ao carregar imagem de máscara: {mask_image_path}")
             # Carregar uma imagem vazia ou placeholder para evitar erros
             self.mask_image = QImage(100, 100, QImage.Format.Format_RGB32)
             self.mask_image.fill(Qt.GlobalColor.black)

        self.region_color_map = region_color_map  # Ex: {(255,0,0): "centro", (0,255,0): "lado1", ...}
        self.current_region = None
        self.setMouseTracking(True)
        # self.overlay_pixmap agora é um dicionário {region_name: QPixmap}
        self.overlay_pixmaps = {} # Nome alterado para evitar confusão

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        print(f"🟢 [Regiao] Inicializado com mask: {mask_image_path}, regions: {list(region_color_map.values())}")
        print(f"📏 [Regiao] Tamanho da mask_image carregada: {self.mask_image.size()}")

    def mouseMoveEvent(self, event: QMouseEvent):
        mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
        print(f"🔍 [Regiao] MouseMoveEvent em ({mouse_x}, {mouse_y})")

        # --- CORREÇÃO DE CENTRALIZAÇÃO (Mesma lógica usada para picking) ---
        widget_width = self.width()
        widget_height = self.height()
        image_width = self.mask_image.width()
        image_height = self.mask_image.height()

        if image_width > 0 and image_height > 0:
            scale_w = widget_width / image_width
            scale_h = widget_height / image_height
            scale = min(scale_w, scale_h)

            scaled_image_w = int(image_width * scale)
            scaled_image_h = int(image_height * scale)

            offset_x = (widget_width - scaled_image_w) // 2
            offset_y = (widget_height - scaled_image_h) // 2

            print(f"📏 [Regiao] Widget: ({widget_width}x{widget_height}), Mask: ({image_width}x{image_height})")
            print(f"📏 [Regiao] Scaled Mask: ({scaled_image_w}x{scaled_image_h}), Offset: ({offset_x}, {offset_y})")

            if (offset_x <= mouse_x < offset_x + scaled_image_w and
                offset_y <= mouse_y < offset_y + scaled_image_h):

                relative_x = mouse_x - offset_x
                relative_y = mouse_y - offset_y

                original_x = int(relative_x / scale)
                original_y = int(relative_y / scale)

                if 0 <= original_x < self.mask_image.width() and 0 <= original_y < self.mask_image.height():
                    pixel_color = QColor(self.mask_image.pixel(original_x, original_y))
                    key = (pixel_color.red(), pixel_color.green(), pixel_color.blue())
                    region = self.region_color_map.get(key)
                    if region != self.current_region:
                        print(f"🔍 [Regiao] Coordenadas corrigidas ({original_x},{original_y}) - Cor: {key} → Região: {region}")
                        self.current_region = region
                        self.update()  # Dispara o repaint
                    else:
                        # print(f"🔍 [Regiao] Mesma região '{region}' detectada em ({original_x},{original_y})") # Muito verboso
                        pass
                else:
                    print(f"🟡 [Regiao] Coordenadas corrigidas ({original_x},{original_y}) fora dos limites da mask_image.")
                    if self.current_region is not None:
                        self.current_region = None
                        self.update()
            else:
                print(f"🟡 [Regiao] Mouse fora do retângulo centralizado da imagem em ({mouse_x},{mouse_y}).")
                if self.current_region is not None:
                    self.current_region = None
                    self.update()
        else:
            print(f"⚠️ [Regiao] Dimensões da mask_image inválidas: ({image_width}x{image_height}).")
            if self.current_region is not None:
                self.current_region = None
                self.update()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Verifica se há uma região ativa sob o mouse (detectada pelo color picking)
            # A condição original incluía 'self.overlay_pixmaps.get(self.current_region)'
            # para garantir um overlay visível. Se o objetivo é clicar em *qualquer* região
            # detectada (onde o hover funciona), removemos essa verificação específica do overlay.
            if self.current_region: # <-- Condição simplificada
                print(f"🖱️ [Regiao] Clique esquerdo detectado na região: {self.current_region}") # Log de confirmação
                # Emite o sinal com o nome da região
                self.region_clicked.emit(self.current_region)
            else:
                print(f"🖱️ [Regiao] Clique esquerdo, mas nenhuma região detectada sob o mouse.")
                print(f"   - self.current_region: {self.current_region}")
        # Propaga o evento para outros widgets se necessário
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        print(f"🚪 [Regiao] Mouse saiu do widget. Limpando região.")
        self.current_region = None
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # CORREÇÃO: Desenhar o pixmap da região atual, se existir, com a mesma centralização
        overlay_to_draw = None
        if self.current_region and self.overlay_pixmaps:
            overlay_to_draw = self.overlay_pixmaps.get(self.current_region)
            if overlay_to_draw:
                 # print(f"🎨 [Regiao] paintEvent: Tentando desenhar overlay para '{self.current_region}'") # Muito verboso
                 pass
            else:
                 print(f"🟡 [Regiao] paintEvent: Região '{self.current_region}' detectada, mas overlay não encontrado.")
        else:
            # print(f"🎨 [Regiao] paintEvent: Nenhuma região ativa ou overlays não definidos.") # Muito verboso
            pass # Nada para desenhar

        if overlay_to_draw:
            # --- Calcular o retângulo de centralização (mesma lógica do mouseMoveEvent) ---
            widget_width = self.width()
            widget_height = self.height()
            image_width = self.mask_image.width() # Usar a mesma imagem base para cálculo
            image_height = self.mask_image.height()

            if image_width > 0 and image_height > 0:
                # Calcular o tamanho do pixmap da máscara se fosse dimensionado para caber no widget
                # Aqui, assumimos que overlay_to_draw deve ser dimensionado proporcionalmente
                # da mesma forma que a imagem base e a picking. Se já estiver dimensionado corretamente,
                # isso é redundante, mas garante consistência se não estiver.
                # Se os overlays já estiverem com as dimensões exatas da imagem base/picking, o scale será 1.
                scale_w = widget_width / image_width
                scale_h = widget_height / image_height
                scale = min(scale_w, scale_h)

                scaled_image_w = int(image_width * scale)
                scaled_image_h = int(image_height * scale)

                # Calcula a posição (x, y) do retângulo centralizado
                offset_x = (widget_width - scaled_image_w) // 2
                offset_y = (widget_height - scaled_image_h) // 2

                # --- Dimensionar o overlay para caber no retângulo centralizado ---
                # Isso garante que o overlay se alinhe com a área centralizada da imagem base/picking
                # Mesmo se o pixmap original do overlay tiver tamanho diferente.
                scaled_overlay_pixmap = overlay_to_draw.scaled(
                    scaled_image_w,
                    scaled_image_h,
                    Qt.AspectRatioMode.KeepAspectRatio, # Mantém proporção
                    Qt.TransformationMode.SmoothTransformation # Suaviza
                )

                # --- Desenhar o overlay dimensionado no retângulo centralizado ---
                painter.drawPixmap(offset_x, offset_y, scaled_overlay_pixmap)

                print(f"🎨 [Regiao] paintEvent: Desenhou overlay para '{self.current_region}' em ({offset_x}, {offset_y}), tamanho ({scaled_image_w}x{scaled_image_h})")
            else:
                print(f"⚠️ [Regiao] paintEvent: Dimensões da mask_image inválidas, não foi possível centralizar o overlay.")

        painter.end()

    def set_overlay_pixmaps(self, overlays_dict):
        """
        overlays_dict: {region_name: QPixmap}
        """
        self.overlay_pixmaps = overlays_dict # Nome alterado
        print(f"🔵 [Regiao] Overlays definidos: {list(overlays_dict.keys())}")

    def sizeHint(self):
        return self.mask_image.size()