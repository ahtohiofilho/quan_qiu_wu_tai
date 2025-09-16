# client/widgets/tile_overlay.py
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor


class TileOverlay(QWidget):
    """
    Overlay flutuante para exibir a textura do bioma do tile.
    - Imagem centralizada com escala responsiva
    - Botão '✕' redondo no canto superior direito
    - Centralizado fisicamente no widget de referência (OpenGLWidget)
    - Fecha com clique fora, no botão ou em ESC
    """
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.image_label = QLabel("...")
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

    def carregar_textura(self, caminho_imagem):
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

        from client.utils.scaling import scale

        # === 🔽 LIMITES BASEADOS NA TELA ===
        # Use 75% do menor lado, mas impõe limite rígido
        target_size = int(min(max_w, max_h) * 1.0)

        # ✅ Novo: limite máximo com margem segura
        MAX_SIZE_ALLOWED = int(min(max_w, max_h) * 0.85)  # Nunca mais que 85%
        MAX_SIZE_HARD = scale(700)  # Limite absoluto físico (para telas pequenas)

        target_size = min(target_size, MAX_SIZE_ALLOWED, MAX_SIZE_HARD)

        # Redimensiona mantendo proporção
        scaled_pixmap = pixmap.scaled(
            target_size,
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        # Ajusta tamanho mínimo do overlay
        self.setMinimumSize(
            scaled_pixmap.width() + scale(32),
            scaled_pixmap.height() + scale(32)
        )

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