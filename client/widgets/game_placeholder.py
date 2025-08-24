# client/widgets/game_placeholder.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class GamePlaceholder(QWidget):
    """Tela temporária que simula o jogo em andamento."""
    def __init__(self, username: str, parent=None):
        super().__init__(parent)
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Fundo escuro
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # Título
        titulo = QLabel("🌍 Partida em Andamento")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Informações
        info = QLabel(f"Jogador: {self.username}\nModo: Online\nMundo: Global Sphere")
        info.setStyleSheet("font-size: 18px; margin-bottom: 30px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão para sair
        btn_sair = QPushButton("🚪 Sair da Partida")
        btn_sair.setStyleSheet("""
            QPushButton {
                background-color: #d22d72;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ff3c8e;
            }
        """)
        btn_sair.clicked.connect(self.on_sair)

        layout.addWidget(titulo)
        layout.addWidget(info)
        layout.addWidget(btn_sair)

    def on_sair(self):
        """Chamado quando o jogador clica em 'Sair'."""
        if hasattr(self.parent(), 'sair_da_partida'):
            self.parent().sair_da_partida()
        else:
            self.hide()