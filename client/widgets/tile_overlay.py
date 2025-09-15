# client/widgets/tile_overlay.py
import os
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
        """Carrega e dimensiona a textura com base no tamanho do widget de referência."""
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
        target_size = int(min(max_w, max_h) * 0.9)
        MAX_SIZE = scale(1024)
        target_size = min(target_size, MAX_SIZE)

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

    def show_centered(self):
        """Exibe o overlay centralizado no centro do widget de referência."""
        if not self.reference_widget:
            print("❌ [TileOverlay] Nenhum widget de referência definido para centralizar.")
            return

        self.adjustSize()
        w, h = self.width(), self.height()

        global_center = self.reference_widget.mapToGlobal(self.reference_widget.rect().center())
        x = global_center.x() - w // 2
        y = global_center.y() - h // 2

        self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        """Fecha o overlay ao pressionar ESC."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)