# client/states/waiting_room.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer
import requests


class TelaSalaEspera(QWidget):
    def __init__(self, username: str, max_jogadores: int, parent=None):
        super().__init__(parent)
        self.username = username
        self.max_jogadores = max_jogadores
        self.parent_window = parent
        self.timer = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        titulo = QLabel("🎮 Sala de Espera")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #ecf0f1;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Aguardando outros jogadores entrarem...")
        subtitulo.setStyleSheet("font-size: 14px; color: #bdc3c7;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo)

        # Linha separadora
        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        linha.setFrameShadow(QFrame.Shadow.Sunken)
        linha.setStyleSheet("color: #34495e;")
        layout.addWidget(linha)

        # Contador de jogadores
        self.label_status = QLabel("Você entrou na fila...")
        self.label_status.setStyleSheet("font-size: 16px; color: #ecf0f1; background-color: #2c3e50; padding: 10px; border-radius: 8px;")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)

        # Informação do seu nome
        self.label_usuario = QLabel(f"Seu nome: {self.username}")
        self.label_usuario.setStyleSheet("font-size: 13px; color: #95a5a6;")
        self.label_usuario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_usuario)

        self.setLayout(layout)

        # Iniciar polling para atualizar o status
        self.iniciar_polling()

    def iniciar_polling(self):
        """Inicia o polling para verificar o status da fila a cada 1 segundo."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_status)
        self.timer.start(1000)  # A cada 1 segundo
        self.atualizar_status()  # Primeira atualização imediata

    def atualizar_status(self):
        try:
            response = requests.get("http://localhost:5000/status")
            if response.status_code == 200:
                data = response.json()
                total_na_fila = data.get("total_na_fila", 0)

                # ✅ Atualiza o texto da tela
                self.label_status.setText(f"Jogadores na fila: {total_na_fila} / {self.max_jogadores}")

                # ✅ Mantém o log para depuração
                print(f"📊 Status atual: {total_na_fila} / {self.max_jogadores}")

                # ✅ Verifica se a partida está cheia
                if total_na_fila >= self.max_jogadores:
                    self.partida_iniciada()

        except requests.exceptions.ConnectionError:
            self.label_status.setText("❌ Erro de conexão com o servidor")
        except Exception as e:
            self.label_status.setText(f"❌ Erro: {str(e)}")

    def partida_iniciada(self):
        """Chamado quando a sala está cheia. Para o timer e notifica o pai."""
        if self.timer:
            self.timer.stop()

        # Aqui você pode tocar um som, mostrar animação, etc.
        self.label_status.setText("✅ Partida iniciada! Carregando mundo...")

        # Notifica a janela principal para mudar de tela
        if self.parent_window:
            self.parent_window.on_partida_iniciada()