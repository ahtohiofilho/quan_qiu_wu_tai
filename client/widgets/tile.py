# client/widgets/tile.py
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor


class TileOverlay(QWidget):
    """
    Overlay flutuante para exibir a textura do bioma do tile e máscaras regionais ao passar o mouse.
    - Imagem centralizada com escala responsiva
    - Botão '✕' redondo no canto superior direito
    - Widget Regiao sobreposto à imagem para mostrar regiões ao passar o mouse
    - Centralizado fisicamente no widget de referência (OpenGLWidget)
    - Fecha com clique fora, no botão ou em ESC
    """
    closed = pyqtSignal()

    def __init__(self, mundo, parent=None):
        super().__init__(parent)
        self.mundo = mundo  # Referência ao mundo atual
        self.region_widget = None # Widget Regiao para máscaras
        self.image_label = QLabel("...") # QLabel para a imagem do bioma
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.Popup |           # Fecha com clique fora
            Qt.WindowType.FramelessWindowHint  # Sem bordas
        )

        from client.utils.scaling import scale

        # === Layout principal (grid para posicionamento preciso) ===
        layout = QGridLayout(self)
        layout.setContentsMargins(scale(16), scale(16), scale(16), scale(16))
        layout.setSpacing(0)

        # --- Label da imagem ---
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: transparent;")

        # --- Botão fechar: apenas '✕' em círculo ---
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(scale(30), scale(30))
        self.btn_close.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(200, 50, 50, 200);
                color: white;
                border-radius: {scale(15)}px;
                font-size: {int(scale(18))}px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba(230, 70, 70, 220);
            }}
        """)
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.clicked.connect(self.close)

        # Adiciona widgets ao grid
        layout.addWidget(self.image_label, 0, 0)
        layout.addWidget(
            self.btn_close,
            0, 0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.setLayout(layout)

        # Estilo do fundo do overlay
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            border-radius: 16px;
        """)

        # Widget de referência para centralização
        self.reference_widget = None

    def set_reference_widget(self, widget):
        """Define o widget de referência (ex: OpenGLWidget) para centralização."""
        self.reference_widget = widget

    def carregar_imagem(self, caminho_imagem, formato="hex_up"):
        from client.utils.scaling import scale
        from client.widgets.region import Regiao

        if not os.path.exists(caminho_imagem):
            print(f"❌ Textura não encontrada: {caminho_imagem}")
            return

        pixmap = QPixmap(caminho_imagem)
        if pixmap.isNull():
            print("❌ QPixmap inválido.")
            return

        # --- Obter dimensões do widget de referência ---
        ref = self.reference_widget or self.parent()
        if not ref:
            max_w, max_h = 800, 600
        else:
            rect = ref.rect()
            max_w, max_h = rect.width(), rect.height()

        # === 🔽 LIMITES BASEADOS NA TELA ===
        target_size = int(min(max_w, max_h) * 1.0)
        MAX_SIZE_ALLOWED = int(min(max_w, max_h) * 0.85)
        MAX_SIZE_HARD = scale(700)
        target_size = min(target_size, MAX_SIZE_ALLOWED, MAX_SIZE_HARD)

        scaled_pixmap = pixmap.scaled(
            target_size,
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        self.setMinimumSize(
            scaled_pixmap.width() + scale(32),
            scaled_pixmap.height() + scale(32)
        )

        # ======= INTEGRAÇÃO DA REGIAO (color picking 2D para hover) =======
        # As cores no picking_path são usadas *internamente* pelo Regiao para detectar regiões.
        # O mapa de overlays define *o que é exibido* quando uma região é detectada (hover).

        # --- Picking path (arquivo invisível para detectar regiões) ---
        picking_path = f"assets/picking/{formato}.png"

        # --- Mapa de cor para as regiões (deve bater com as cores do arquivo de picking) ---
        region_color_map = {
            (255, 0, 0): "center",
            (0, 255, 0): "top",
            (255, 0, 255): "bottom",
            (127, 127, 127): "left",
            (127, 0, 127): "right",
            (1, 11, 111): "topleft",
            (0, 0, 255): "topright",
            (0, 255, 255): "bottomleft",
            (255, 255, 0): "bottomright"
        }

        # --- Overlays corretos para o formato atual (visíveis ao passar o mouse) ---
        # Supõe que mundo.ref.overlay_paths[formato] é um dicionário
        # mapeando nomes de regiões para caminhos de arquivos de overlay.
        try:
            overlay_pixmaps = {
                reg: QPixmap(path) for reg, path in self.mundo.ref.overlay_paths[formato].items()
            }
        except (AttributeError, KeyError) as e:
            print(f"⚠️ Erro ao carregar overlays para formato '{formato}': {e}. Usando dicionário vazio.")
            overlay_pixmaps = {}

        # Remove o widget anterior se existir (evita leaks e sobreposição)
        if self.region_widget:
            self.region_widget.setParent(None)
            self.region_widget.deleteLater()
            self.region_widget = None

        # Cria o novo widget Regiao sobre a image_label (tamanho igual à imagem exibida)
        # O Regiao usa picking_path e region_color_map internamente para color picking.
        # Ele exibe os pixmaps de overlay_pixmaps conforme a região detectada (hover).
        self.region_widget = Regiao(picking_path, region_color_map, parent=self.image_label)
        self.region_widget.set_overlay_pixmaps(overlay_pixmaps) # <-- Define os overlays visíveis
        self.region_widget.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())

        # Garantir que o Regiao receba eventos de mouse (hover)
        # self.region_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # Opcional, já é False por padrão
        # self.region_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True) # Opcional, já é True no Regiao

        self.region_widget.show()

    def show_centered(self):
        """Exibe o overlay com diagnóstico detalhado de posicionamento."""
        from PyQt6.QtWidgets import QApplication

        # --- 1. Obter janela principal ---
        app = QApplication.instance()
        window = app.activeWindow()
        if not window:
            print("❌ [DEBUG - SHOW] Nenhuma janela ativa encontrada.")
            return
        else:
            print(f"✅ [DEBUG - SHOW] Janela ativa: {window}")

        # --- 2. Obter geometria da área disponível (sem barra de tarefas) ---
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()
        print(f"📏 [DEBUG - SHOW] availableGeometry(): {screen_rect}")

        center_x = screen_rect.center().x()
        center_y = screen_rect.center().y()
        print(f"🎯 [DEBUG - SHOW] Centro absoluto da tela: ({center_x}, {center_y})")

        # --- 3. Tamanho do overlay ---
        self.adjustSize()
        w, h = self.width(), self.height()
        print(f"🖼️ [DEBUG - SHOW] Tamanho calculado do overlay: {w}x{h}")

        # --- 4. Posição final ---
        x = center_x - w // 2
        y = center_y - h // 2
        print(f"📌 [DEBUG - SHOW] Posição final calculada: ({x}, {y})")

        # --- 5. Informações adicionais para depuração visual ---
        print(f"🔍 [DEBUG - SHOW] Altura total da tela física: {screen.geometry().height()}")
        print(f"🔍 [DEBUG - SHOW] Margem superior (barra de tarefas?): {screen.geometry().top()}")
        print(f"🔍 [DEBUG - SHOW] Margem inferior estimada: {screen.geometry().bottom() - screen_rect.bottom()}")

        # --- 6. Aplicar posição ---
        self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()
        print(f"✅ [DEBUG - SHOW] Overlay mostrado em ({x}, {y}), tamanho {w}x{h}")

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        """Fecha o overlay ao pressionar ESC."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)