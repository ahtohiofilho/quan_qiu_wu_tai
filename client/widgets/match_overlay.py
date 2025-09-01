# client/widgets/match_overlay.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class OverlayPartida(QWidget):
    """Overlay flutuante dentro da barra esquerda, exibido apenas durante a partida.
    Contém controles de ação e um seletor para alternar entre modo de mapa físico e político.
    Centralizado verticalmente, com fundo translúcido e largura ajustada à barra.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Referência ao widget pai (barra_esquerda)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(40, 40, 55, 220);
            border-radius: 12px;
            border: 1px solid #3498db;
            color: #ecf0f1;
            font-family: Arial, sans-serif;
        """)
        self.setup_ui()
        self.update_position()  # Posiciona inicialmente

    def alternar_modo_mapa(self):
        """Alterna entre modo físico e político e atualiza o ícone do botão."""
        novo_modo = "politico" if self.btn_modo_mapa.text() == "🌍" else "fisico"
        novo_icone = "🏛️" if novo_modo == "politico" else "🌍"

        self.btn_modo_mapa.setText(novo_icone)
        self.btn_modo_mapa.setToolTip(f"Modo: {'Político' if novo_modo == 'politico' else 'Físico'}")

        print(f"🔄 Modo de mapa alterado para: {novo_modo}")

        # Repassa para a janela principal
        if hasattr(self.parent_widget, 'mudar_modo_mapa'):
            self.parent_widget.mudar_modo_mapa(novo_modo)
        else:
            print("⚠️ OverlayPartida: Não foi possível encontrar 'mudar_modo_mapa' no pai.")

    def setup_ui(self):
        """Configura a interface com apenas o botão toggle para alternar entre modo físico e político."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 10, 12)  # Margens reduzidas para caber melhor na barra
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão de alternância de modo (toggle entre físico e político)
        self.btn_modo_mapa = QPushButton("🌍")  # Começa no modo físico
        self.btn_modo_mapa.setFixedSize(60, 40)
        self.btn_modo_mapa.setToolTip("Alternar modo de mapa (Físico/Político)")
        self.btn_modo_mapa.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #34495e;
                border-color: #1abc9c;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
                border-color: #16a085;
            }
        """)
        self.btn_modo_mapa.clicked.connect(self.alternar_modo_mapa)
        layout.addWidget(self.btn_modo_mapa)

        self.setLayout(layout)

    def update_position(self):
        """Atualiza posição e tamanho com base no widget pai (barra_esquerda)."""
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        width = int(parent_rect.width() * 0.85)  # 85% da largura da barra
        height = min(200, int(parent_rect.height() * 0.45))  # Máx 45% da altura

        x = (parent_rect.width() - width) // 2
        y = (parent_rect.height() - height) // 2

        self.setGeometry(x, y, width, height)