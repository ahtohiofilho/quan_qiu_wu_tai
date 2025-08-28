# client/states/waiting_room.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtProperty, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QCursor
import requests


class OverlaySalaEspera(QWidget):
    """
    Widget de sobreposição (overlay) para exibir a sala de espera
    diretamente sobre o OpenGL, mantendo a barra de ícones, fundo e estrutura.
    Não substitui a janela principal.
    """

    def __init__(self, username: str, max_jogadores: int, parent=None):
        super().__init__(parent)
        self.username = username
        self.max_jogadores = max_jogadores
        self.parent_widget = parent  # Referência ao widget pai (ex: opengl_container)
        self.timer = None
        self._opacity = 0.0
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.setup_ui()
        self.iniciar_polling()

    def _get_opacity(self):
        return self._opacity

    def _set_opacity(self, opacity):
        self._opacity = opacity
        # Atualiza fundo com transparência
        self.setStyleSheet(
            f"background-color: rgba(44, 62, 80, {int(opacity * 180)}); "
            "border-radius: 15px; border: 1px solid #3498db;"
        )

    opacity = pyqtProperty(float, _get_opacity, _set_opacity)

    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        titulo = QLabel("🎮 Sala de Espera")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #ecf0f1;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Aguardando outros jogadores entrarem...")
        subtitulo.setStyleSheet("font-size: 13px; color: #bdc3c7;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo)

        # Linha separadora
        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        linha.setFrameShadow(QFrame.Shadow.Sunken)
        linha.setStyleSheet("color: #34495e;")
        layout.addWidget(linha)

        # Status: jogadores na fila
        self.label_status = QLabel("Você entrou na fila...")
        self.label_status.setStyleSheet(
            "font-size: 16px; color: #ecf0f1; background-color: #2c3e50; "
            "padding: 10px; border-radius: 8px;"
        )
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)

        # Informação do usuário
        self.label_usuario = QLabel(f"Seu nome: {self.username}")
        self.label_usuario.setStyleSheet("font-size: 13px; color: #95a5a6;")
        self.label_usuario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_usuario)

        self.setLayout(layout)

        # Estilo geral
        self.setFixedWidth(360)
        self.setFixedHeight(220)
        self.setStyleSheet("background-color: rgba(44, 62, 80, 180); border-radius: 15px; border: 1px solid #3498db;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()  # Começa oculto

    def iniciar_polling(self):
        """Inicia atualização periódica do status da fila."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_status)
        self.timer.start(1000)  # A cada 1 segundo
        self.atualizar_status()  # Primeira atualização imediata

    def atualizar_status(self):
        try:
            response = requests.get("http://localhost:5000/status", timeout=3)
            if response.status_code == 200:
                data = response.json()
                total_na_fila = data.get("total_na_fila", 0)
                self.label_status.setText(f"Jogadores na fila: {total_na_fila} / {self.max_jogadores}")
                print(f"📊 Status atual: {total_na_fila} / {self.max_jogadores}")

                if total_na_fila >= self.max_jogadores:
                    self.partida_iniciada()
        except requests.exceptions.ConnectionError:
            self.label_status.setText("❌ Erro de conexão")
        except Exception as e:
            self.label_status.setText(f"❌ Erro: {str(e)}")

    def partida_iniciada(self):
        """Chamado quando a sala está cheia. Evita chamadas duplicadas e garante transição segura."""
        print("🔵 [DEBUG] WaitingRoomOverlay.partida_iniciada: Início da execução")

        # 1. Parar o timer de atualização
        if self.timer:
            print("⏸️ [DEBUG] WaitingRoomOverlay.partida_iniciada: Parando timer de atualização")
            self.timer.stop()
        else:
            print("🟡 [DEBUG] WaitingRoomOverlay.partida_iniciada: Timer já parado ou inexistente")

        # 2. Atualizar o status visual
        print("🎨 [DEBUG] WaitingRoomOverlay.partida_iniciada: Atualizando texto do status")
        self.label_status.setText("✅ Partida iniciada! Carregando mundo...")

        # 3. Verificar se a partida já foi iniciada (evitar duplicação)
        parent = self.parent_widget
        if hasattr(parent, 'game_placeholder') and parent.game_placeholder is not None:
            print(
                "🔴 [DEBUG] WaitingRoomOverlay.partida_iniciada: game_placeholder já existe. Partida já iniciada. Ignorando.")
            self.hide()
            return
        else:
            print("🟢 [DEBUG] WaitingRoomOverlay.partida_iniciada: Nenhum game_placeholder detectado. Continuando...")

        # 4. Chamar a função da janela principal com animação
        if hasattr(parent, 'on_partida_iniciada'):
            print(
                "🔵 [DEBUG] WaitingRoomOverlay.partida_iniciada: on_partida_iniciada encontrado no parent. Iniciando fade_out")

            # Iniciar animação de saída
            self.fade_out()

            # Chamar on_partida_iniciada após a animação
            print("🟡 [DEBUG] WaitingRoomOverlay.partida_iniciada: Agendando parent.on_partida_iniciada em 300ms")
            QTimer.singleShot(300, parent.on_partida_iniciada)
        else:
            print(
                "🔴 [DEBUG] WaitingRoomOverlay.partida_iniciada: parent.on_partida_iniciada não encontrado. Escondendo overlay.")
            # Caso não exista callback, apenas esconder
            self.hide()

        print("🟢 [DEBUG] WaitingRoomOverlay.partida_iniciada: Execução concluída")

    def fade_in(self):
        """Animação de entrada suave."""
        self._opacity = 0.0
        self.show()
        self.raise_()

        anim = QPropertyAnimation(self, b"opacity")
        anim.setDuration(250)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def fade_out(self):
        """Animação de saída suave."""
        anim = QPropertyAnimation(self, b"opacity")
        anim.setDuration(200)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def showEvent(self, event):
        """Reposiciona o overlay no centro do pai ao aparecer."""
        super().showEvent(event)
        if self.parent_widget:
            x = (self.parent_widget.width() - self.width()) // 2
            y = (self.parent_widget.height() - self.height()) // 2
            self.move(x, y)
        # Inicia animação de entrada
        QTimer.singleShot(10, self.fade_in)

    def resizeEvent(self, event):
        """Reposiciona ao redimensionar."""
        super().resizeEvent(event)
        if self.isVisible() and self.parent_widget:
            x = (self.parent_widget.width() - self.width()) // 2
            y = (self.parent_widget.height() - self.height()) // 2
            self.move(x, y)