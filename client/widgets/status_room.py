# client/widgets/status_room.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
import requests


class WidgetStatusSalaEspera(QWidget):
    """
    Widget compacto para exibir status da sala de espera
    diretamente na barra esquerda, entre 'Play' e 'Sair'.
    """

    def __init__(self, username: str, max_jogadores: int, parent=None):
        super().__init__(parent)
        self.username = username
        self.max_jogadores = max_jogadores
        self.parent_widget = parent
        self.timer = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 10, 12, 10)

        # Fundo arredondado
        self.setStyleSheet("""
            background-color: #34495e;
            border-radius: 10px;
            border: 1px solid #3498db;
        """)
        self.setFixedHeight(110)

        # Título
        self.titulo = QLabel("🎮 Sala de Espera")
        self.titulo.setStyleSheet("font-size: 13px; font-weight: bold; color: #ecf0f1;")
        layout.addWidget(self.titulo)

        # Status: jogadores
        self.label_status = QLabel(f"Jogadores: 1 / {self.max_jogadores}")
        self.label_status.setStyleSheet("font-size: 12px; color: #bdc3c7;")
        layout.addWidget(self.label_status)

        # Usuário
        self.label_usuario = QLabel(f"Você: {self.username}")
        self.label_usuario.setStyleSheet("font-size: 11px; color: #95a5a6;")
        layout.addWidget(self.label_usuario)

        # Botão Cancelar
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_cancelar.setFixedHeight(25)
        self.btn_cancelar.clicked.connect(self.on_cancelar)
        layout.addWidget(self.btn_cancelar)

        self.setLayout(layout)

    def atualizar_status(self, total_na_fila: int):
        """Atualiza o contador de jogadores."""
        self.label_status.setText(f"Jogadores: {total_na_fila} / {self.max_jogadores}")

    def on_cancelar(self):
        """Chamado ao clicar em Cancelar."""
        try:
            with open("session.txt", "r") as f:
                username = f.read().strip()
            requests.post("http://localhost:5000/jogo/sair", json={"username": username})
        except:
            pass
        finally:
            if self.parent_widget:
                self.parent_widget.remover_status_sala()  # Método que vamos adicionar