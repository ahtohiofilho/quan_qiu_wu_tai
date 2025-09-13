# client/widgets/tile_overlay.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot
from client.utils.scaling import scale, scale_font


class TileOverlay(QWidget):
    """
    Overlay flutuante centralizado que exibe informações sobre um tile clicado.
    Aparece no centro da área OpenGL, com fundo translúcido e estilo minimalista.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setup_ui()
        self.hide()  # Começa oculto

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(scale(20), scale(15), scale(20), scale(15))
        layout.setSpacing(scale(10))

        # Título destacado
        self.label_title = QLabel("Informações do Tile")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet(f"""
            font-size: {scale_font(16)}px;
            font-weight: bold;
            color: white;
            margin-bottom: {scale(8)}px;
        """)
        layout.addWidget(self.label_title)

        # Conteúdo principal (placeholder dinâmico)
        self.label_info = QLabel("Bioma: Savana\nAltitude: 85m\nPopulação: 850")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setStyleSheet(f"""
            font-size: {scale_font(13)}px;
            color: #e0e0e0;
            background-color: rgba(40, 40, 60, 180);
            padding: {scale(12)}px;
            border-radius: {scale(8)}px;
            border: 1px solid rgba(255, 255, 255, 30);
        """)
        layout.addWidget(self.label_info)

        # Botão de fechar no canto superior direito
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(scale(28), scale(28))
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 0, 0, 180);
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        self.btn_close.clicked.connect(self.hide)

        # Layout para o botão de fechar
        close_layout = QVBoxLayout()
        close_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        close_layout.addWidget(self.btn_close)
        layout.addLayout(close_layout)

        self.setLayout(layout)

        # Estilo geral: fundo escuro translúcido
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            border-radius: 16px;
        """)

    @pyqtSlot(dict)
    def atualizar_info(self, dados_tile):
        """
        Atualiza as informações exibidas com base nos dados do tile.
        :param dados_tile: dict com chaves como 'bioma', 'altitude', 'populacao'
        """
        bioma = dados_tile.get("bioma", "Desconhecido")
        altitude = f"{dados_tile.get('altitude', '?')}m"
        populacao = f"{dados_tile.get('populacao', 0):,}".replace(",", ".") + " hab."

        info_text = f"<b>{bioma}</b><br>Altitude: {altitude}<br>População: {populacao}"
        self.label_info.setText(info_text)

    def show_centered(self):
        """
        Exibe o overlay centralizado dentro do widget pai (opengl_container).
        """
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        width = scale(320)
        height = scale(200)
        x = (parent_rect.width() - width) // 2
        y = (parent_rect.height() - height) // 2

        self.setGeometry(x, y, width, height)
        self.show()
        self.raise_()