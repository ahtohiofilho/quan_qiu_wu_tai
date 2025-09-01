#client/widgets/match_overlay.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class OverlayPartida(QWidget):
    """Overlay flutuante dentro da barra esquerda, exibido apenas durante a partida.
    Centralizado verticalmente, com fundo translúcido e largura quase total da barra."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(40, 40, 55, 200);
            border-radius: 12px;
            border: 1px solid #3498db;
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Exemplo: título
        titulo = QLabel("Ações")
        titulo.setStyleSheet("color: #ecf0f1; font-weight: bold; font-size: 14px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Aqui você adiciona os botões/ícones de ação da partida
        # Ex: botão de construir, atacar, etc.
        # Exemplo:
        # btn_construir = QPushButton("🏗️ Construir")
        # layout.addWidget(btn_construir)

    def update_position(self):
        """Atualiza posição e tamanho com base no pai (barra_esquerda)"""
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        width = int(parent_rect.width() * 0.85)  # 85% da largura da barra
        height = min(200, parent_rect.height() * 0.5)  # Máx 50% da altura

        x = (parent_rect.width() - width) // 2
        y = (parent_rect.height() - height) // 2

        self.setGeometry(x, y, width, height)