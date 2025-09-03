# client/components/icon_manager.py
"""Componentes para gerenciar ícones interativos na barra lateral esquerda."""

import os
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor

# --- Sistema de Escala para DPI ---
from client.utils.scaling import scale

class IconeInterativo(QLabel):
    """
    Um QLabel que exibe uma imagem e emite um sinal quando clicado.
    """
    clicado = pyqtSignal(str)  # Sinal emitido ao ser clicado, passando um identificador

    def __init__(self, icone_path, identificador, tamanho_base=(64, 64), parent=None):
        """
        :param icone_path: Caminho para o arquivo PNG do ícone.
        :param identificador: String única ("login", "play", "sair").
        :param tamanho_base: Tamanho base em pixels (será escalonado por DPI).
        :param parent: Widget pai.
        """
        super().__init__(parent)
        self.identificador = identificador
        self.tamanho_base = tamanho_base
        self.tamanho = (scale(tamanho_base[0]), scale(tamanho_base[1]))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estilo para feedback visual
        self.setStyleSheet("""
            IconeInterativo {
                border: 2px solid transparent;
                border-radius: 5px;
            }
            IconeInterativo:hover {
                border: 2px solid #3498db;
                background-color: rgba(52, 152, 219, 30);
            }
        """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.carregar_icone(icone_path)
        self.setFixedSize(*self.tamanho)

    def carregar_icone(self, caminho):
        """Carrega e escala a imagem com suporte a placeholder."""
        print(f"[DEBUG] [IconeInterativo] Carregando ícone '{self.identificador}' de: '{caminho}'")

        pixmap = None
        if caminho and os.path.isfile(caminho):
            try:
                pixmap = QPixmap(caminho)
                if pixmap.isNull():
                    print(f"⚠️ Falha ao carregar QPixmap de '{caminho}'. Usando placeholder.")
                    pixmap = None
                else:
                    print(f"[DEBUG] [IconeInterativo] Carregado: {pixmap.width()}x{pixmap.height()}")
            except Exception as e:
                print(f"❌ Erro ao carregar ícone '{caminho}': {e}")
        else:
            print(f"⚠️ Arquivo não encontrado: '{caminho}'. Usando placeholder.")

        if pixmap is None:
            # Placeholder
            pixmap = QPixmap(self.tamanho[0], self.tamanho[1])
            pixmap.fill(Qt.GlobalColor.gray)
            print(f"[DEBUG] [IconeInterativo] Placeholder criado para '{self.identificador}'.")
        else:
            # Escala com proporção
            pixmap = pixmap.scaled(
                self.tamanho[0],
                self.tamanho[1],
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.setPixmap(pixmap)
        print(f"[DEBUG] [IconeInterativo] Pixmap definida para '{self.identificador}'.")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"🖱️ Ícone '{self.identificador}' clicado.")
            self.clicado.emit(self.identificador)
        super().mousePressEvent(event)


class GerenciadorIconesEsquerda(QWidget):
    """
    Widget que contém e organiza os ícones interativos na barra esquerda.
    """
    icone_clicado = pyqtSignal(str)

    def __init__(self, caminho_recursos="client/resources", parent=None):
        super().__init__(parent)
        self.caminho_recursos = caminho_recursos
        self.icones = {}
        self.TAMANHO_ICONE_BASE = (36, 36)  # Base para escala DPI

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            scale(10), scale(10), scale(10), scale(10)
        )
        layout.setSpacing(scale(20))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # --- Ícone de Login + Nome ---
        self.icone_login = IconeInterativo(
            os.path.join(self.caminho_recursos, "log-in.png"),
            "login",
            tamanho_base=self.TAMANHO_ICONE_BASE
        )
        self.icone_login.clicado.connect(self._ao_clicar_icone)

        self.label_nome_usuario = QLabel()
        self.label_nome_usuario.setStyleSheet("""
            color: #ecf0f1;
            background: transparent;
            border: none;
            font-size: """ + str(scale(14)) + """px;
            font-weight: bold;
        """)
        self.label_nome_usuario.hide()

        # Layout horizontal único
        self.login_layout = QHBoxLayout()
        self.login_layout.setContentsMargins(0, 0, 0, 0)
        self.login_layout.setSpacing(scale(8))
        self.login_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.login_layout.addWidget(self.icone_login)
        self.login_layout.addWidget(self.label_nome_usuario)

        self.login_container = QWidget()
        self.login_container.setLayout(self.login_layout)
        layout.addWidget(self.login_container)

        self.icones["login"] = self.icone_login

        # --- Ícone de Play ---
        self.icone_play = IconeInterativo(
            os.path.join(self.caminho_recursos, "play.png"),
            "play",
            tamanho_base=self.TAMANHO_ICONE_BASE
        )
        self.icone_play.clicado.connect(self._ao_clicar_icone)
        layout.addWidget(self.icone_play)
        self.icones["play"] = self.icone_play

        # --- Espaço para empurrar o ícone de sair para baixo ---
        layout.addStretch()

        # --- Ícone de Sair ---
        self.icone_sair = IconeInterativo(
            os.path.join(self.caminho_recursos, "arrow-left.png"),
            "sair",
            tamanho_base=self.TAMANHO_ICONE_BASE
        )
        self.icone_sair.clicado.connect(self._ao_clicar_icone)
        layout.addWidget(self.icone_sair)
        self.icones["sair"] = self.icone_sair

    def atualizar_estado_login(self, esta_logado: bool, nome_usuario: str = None):
        if esta_logado and nome_usuario:
            caminho = os.path.join(self.caminho_recursos, "smile.png")
            self.icone_login.carregar_icone(caminho)
            self.label_nome_usuario.setText(nome_usuario)
            self.label_nome_usuario.show()
        else:
            caminho = os.path.join(self.caminho_recursos, "log-in.png")
            self.icone_login.carregar_icone(caminho)
            self.label_nome_usuario.hide()

    def _ao_clicar_icone(self, identificador):
        print(f"📡 GerenciadorIconesEsquerda: Ícone '{identificador}' acionado.")
        self.icone_clicado.emit(identificador)

    def atualizar_icone(self, identificador, novo_caminho):
        if identificador in self.icones:
            self.icones[identificador].carregar_icone(novo_caminho)
        else:
            print(f"⚠️ Ícone '{identificador}' não encontrado.")

    def remover_status_sala(self):
        if hasattr(self, 'widget_status_sala') and self.widget_status_sala is not None:
            layout = self.layout()
            if layout and self.widget_status_sala in layout:
                layout.removeWidget(self.widget_status_sala)
            self.widget_status_sala.deleteLater()
            self.widget_status_sala = None
            print("🗑️ Widget de status da sala removido da barra lateral.")