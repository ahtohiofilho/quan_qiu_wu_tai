# client/widgets/waiting_room_overlay.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class WaitingRoomOverlay(QWidget):
    """
    Overlay flutuante para exibir a sala de espera no centro da área principal,
    entre as barras laterais, substituindo o 'Welcome to Global Arena'.
    """

    def __init__(self, username: str, max_jogadores: int, parent=None):
        super().__init__(parent)
        self.username = username
        self.max_jogadores = max_jogadores
        self.setup_ui()

    def setup_ui(self):
        # Fundo translúcido escuro
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layout principal com centralização vertical
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ✅ Adicionar stretch acima para centralizar
        layout.addStretch()

        # --- TÍTULO: Waiting Room ---
        self.label_titulo = QLabel("Waiting Room")
        font_titulo = QFont()
        font_titulo.setPointSize(20)
        font_titulo.setBold(True)
        self.label_titulo.setFont(font_titulo)
        self.label_titulo.setStyleSheet("color: #3498db;")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_titulo)

        # --- SUBTÍTULO: Players: X / 4 ---
        self.label_subtitulo = QLabel(f"Players: 1 / {self.max_jogadores}")
        font_sub = QFont()
        font_sub.setPointSize(14)
        self.label_subtitulo.setFont(font_sub)
        self.label_subtitulo.setStyleSheet("color: #ecf0f1;")
        self.label_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_subtitulo)

        # --- CAIXA: Nome do jogador ---
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            background-color: #2c3e50;
            border: 2px solid #3498db;
            border-radius: 16px;
            padding: 20px;
        """)
        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)

        # ✅ REMOVIDO: self.label_icon = QLabel("🎮") → Não queremos o emoji

        self.label_user = QLabel(f"You: {self.username}")
        self.label_user.setStyleSheet("font-size: 14px; color: #bdc3c7;")
        self.label_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.label_user)

        self.content_frame.setLayout(content_layout)
        layout.addWidget(self.content_frame)

        # --- BOTÃO CANCEL ---
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_cancel.setFixedHeight(35)
        layout.addWidget(self.btn_cancel)

        # ✅ Adicionar stretch abaixo para centralizar
        layout.addStretch()

    def atualizar_status(self, total_na_fila: int):
        """Atualiza o subtítulo com o número de jogadores na fila."""
        self.label_subtitulo.setText(f"Players: {total_na_fila} / {self.max_jogadores}")

    def connect_cancel(self, callback):
        """Conecta o botão Cancelar a uma função."""
        if callable(callback):
            self.btn_cancel.clicked.connect(callback)