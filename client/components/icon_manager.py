# client/components/icon_manager.py
"""Componentes para gerenciar ícones interativos na barra lateral esquerda."""

import os
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor


class IconeInterativo(QLabel):
    """
    Um QLabel que exibe uma imagem e emite um sinal quando clicado.
    """
    clicado = pyqtSignal(str)  # Sinal emitido ao ser clicado, passando um identificador

    def __init__(self, icone_path, identificador, tamanho=(64, 64), parent=None):
        """
        :param icone_path: Caminho para o arquivo PNG do ícone.
        :param identificador: String única para identificar este ícone ("login", "play", "sair").
        :param tamanho: Tupla (largura, altura) para redimensionar o ícone.
        :param parent: Widget pai.
        """
        super().__init__(parent)
        self.identificador = identificador
        self.tamanho = tamanho
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estilo para feedback visual (opcional)
        self.setStyleSheet("""
            IconeInterativo {
                border: 2px solid transparent; /* Borda invisível por padrão */
                border-radius: 5px; /* Bordas arredondadas */
            }
            IconeInterativo:hover {
                border: 2px solid #3498db; /* Borda azul ao passar o mouse */
                background-color: rgba(52, 152, 219, 30); /* Fundo azul claro transparente */
            }
        """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Muda o cursor para mãozinha

        self.carregar_icone(icone_path)
        # Redimensionar o QLabel para o tamanho desejado
        self.setFixedSize(*self.tamanho)

    def carregar_icone(self, caminho):
        """
        Carrega e define a imagem do ícone.
        Inclui verificações detalhadas e logs para facilitar depuração.
        """
        print(f"[DEBUG] [IconeInterativo] Tentando carregar ícone '{self.identificador}' de: '{caminho}'")

        # --- Verificações detalhadas do caminho ---
        caminho_absoluto = os.path.abspath(caminho)
        existe = os.path.exists(caminho)
        eh_arquivo = os.path.isfile(caminho) if existe else False

        print(f"[DEBUG] [IconeInterativo] Caminho absoluto resolvido: '{caminho_absoluto}'")
        print(f"[DEBUG] [IconeInterativo] os.path.exists('{caminho}') = {existe}")
        print(f"[DEBUG] [IconeInterativo] os.path.isfile('{caminho}') = {eh_arquivo}")

        # --- Determinar se o carregamento pode prosseguir ---
        pixmap = None
        if not existe:
            print(
                f"⚠️ [IconeInterativo] O caminho '{caminho}' NÃO EXISTE. Diretório de execução pode estar incorreto. Usando placeholder.")
        elif not eh_arquivo:
            print(
                f"⚠️ [IconeInterativo] O caminho '{caminho}' EXISTE, mas NÃO É um arquivo (pode ser um diretório). Usando placeholder.")
        else:
            # Caminho existe e é um arquivo, tentar carregar com QPixmap
            print(f"[DEBUG] [IconeInterativo] Caminho válido, tentando QPixmap('{caminho}')...")
            try:
                pixmap = QPixmap(caminho)

                # Verificar se o carregamento foi bem-sucedido
                if pixmap.isNull():
                    print(f"⚠️ [IconeInterativo] QPixmap falhou ao carregar o arquivo '{caminho}'. "
                          f"O arquivo pode estar corrompido ou não ser uma imagem válida. Usando placeholder.")
                    pixmap = None  # Forçar uso do placeholder
                else:
                    print(
                        f"[DEBUG] [IconeInterativo] QPixmap carregou com sucesso. Tamanho original: {pixmap.width()}x{pixmap.height()}")

            except Exception as e:
                print(f"❌ [IconeInterativo] Erro inesperado ao carregar QPixmap de '{caminho}': {e}")
                import traceback
                traceback.print_exc()  # Imprime o stack trace completo
                pixmap = None  # Forçar uso do placeholder

        # --- Criar pixmap final (carregada ou placeholder) ---
        if pixmap is None:
            # Criar um pixmap de placeholder se a imagem não for carregada
            pixmap = QPixmap(self.tamanho[0], self.tamanho[1])
            pixmap.fill(Qt.GlobalColor.gray)  # Cor cinza para placeholder
            print(f"[DEBUG] [IconeInterativo] Placeholder cinza criado para '{self.identificador}'.")
        else:
            # Redimensionar a pixmap carregada para o tamanho desejado
            pixmap = pixmap.scaled(
                self.tamanho[0],
                self.tamanho[1],
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            print(
                f"[DEBUG] [IconeInterativo] Pixmap (carregada) redimensionada para {self.tamanho[0]}x{self.tamanho[1]}.")

        # --- Definir a pixmap (carregada ou placeholder) no QLabel ---
        self.setPixmap(pixmap)
        print(f"[DEBUG] [IconeInterativo] Pixmap definida para o ícone '{self.identificador}'.")

    def mousePressEvent(self, event):
        """Sobrescreve para emitir o sinal ao ser clicado."""
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"🖱️ Ícone '{self.identificador}' clicado.")
            self.clicado.emit(self.identificador)  # Emite o sinal com o identificador
        super().mousePressEvent(event)  # Chama o método da classe base


class GerenciadorIconesEsquerda(QWidget):
    """
    Widget que contém e organiza os ícones interativos na barra esquerda.
    """
    icone_clicado = pyqtSignal(str)  # Re-emite o sinal dos ícones filhos

    def __init__(self, caminho_recursos="client/resources", parent=None):
        """
        :param caminho_recursos: Caminho para a pasta com os ícones PNG.
        :param parent: Widget pai.
        """
        super().__init__(parent)
        self.caminho_recursos = caminho_recursos
        self.icones = {}  # Dicionário para armazenar referências aos ícones {identificador: IconeInterativo}
        self.TAMANHO_ICONE = (48, 48)

        # Layout vertical para os ícones
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Margens internas
        layout.setSpacing(20)  # Espaço entre os ícones
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # --- Criar e adicionar ícones ---
        # --- Ícone de Login com nome do usuário ---
        icone_login_path = os.path.join(self.caminho_recursos, "log-in.png")
        self.icone_login = IconeInterativo(icone_login_path, "login", tamanho=self.TAMANHO_ICONE)
        self.icone_login.clicado.connect(self._ao_clicar_icone)

        # Layout horizontal para ícone + nome
        self.login_layout = QHBoxLayout()
        self.login_layout.setContentsMargins(0, 0, 0, 0)
        self.login_layout.setSpacing(8)
        self.login_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Adicionar ícone
        self.login_layout.addWidget(self.icone_login)

        # Label para nome do usuário
        self.label_nome_usuario = QLabel()
        self.label_nome_usuario.setStyleSheet("""
            color: #ecf0f1;
            background: transparent;
            border: none;
            font-size: 14px;
            font-weight: bold;
        """)
        self.label_nome_usuario.hide()
        self.login_layout.addWidget(self.label_nome_usuario)

        # Container final
        self.login_container = QWidget()
        self.login_container.setLayout(self.login_layout)

        # Adicionar ao layout principal
        layout.addWidget(self.login_container)

        # Referência
        self.icones["login"] = self.icone_login

        # Criar um layout horizontal para o ícone + nome
        self.login_layout = QHBoxLayout()
        self.login_layout.setContentsMargins(0, 0, 0, 0)
        self.login_layout.setSpacing(8)  # Espaço entre ícone e texto
        self.login_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Adicionar ícone
        self.login_layout.addWidget(self.icone_login)

        # Adicionar label de nome (inicialmente oculto)
        self.label_nome_usuario = QLabel()
        self.label_nome_usuario.setStyleSheet("""
            color: #ecf0f1;
            background: transparent;
            border: none;
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: bold;
        """)
        self.label_nome_usuario.hide()  # Esconde por padrão
        self.login_layout.addWidget(self.label_nome_usuario)

        # Container widget para o layout horizontal
        self.login_container = QWidget()
        self.login_container.setLayout(self.login_layout)

        # Adicionar o container ao layout principal
        layout.addWidget(self.login_container)

        # Armazenar referência
        self.icones["login"] = self.icone_login  # Mantém compatibilidade

        # Ícone de Play (Mais abaixo)
        icone_play_path = os.path.join(self.caminho_recursos, "play.png")
        self.icone_play = IconeInterativo(icone_play_path, "play", tamanho=self.TAMANHO_ICONE)
        self.icone_play.clicado.connect(self._ao_clicar_icone)
        layout.addWidget(self.icone_play)
        self.icones["play"] = self.icone_play

        # Espaço elástico para empurrar o ícone de sair para baixo
        layout.addStretch()

        # Ícone de Sair (Inferior Esquerdo)
        icone_sair_path = os.path.join(self.caminho_recursos, "arrow-left.png")
        self.icone_sair = IconeInterativo(icone_sair_path, "sair", tamanho=self.TAMANHO_ICONE)
        self.icone_sair.clicado.connect(self._ao_clicar_icone)
        layout.addWidget(self.icone_sair)
        self.icones["sair"] = self.icone_sair

    def atualizar_estado_login(self, esta_logado: bool, nome_usuario: str = None):
        """Atualiza o ícone de login e mostra/esconde o nome do usuário."""
        if esta_logado and nome_usuario:
            # Trocar ícone para o de usuário logado
            caminho = os.path.join(self.caminho_recursos, "smile.png")
            self.icone_login.carregar_icone(caminho)
            # Mostrar e atualizar nome do usuário
            self.label_nome_usuario.setText(nome_usuario)
            self.label_nome_usuario.show()  # ✅ Garante que o label apareça
        else:
            # Voltar para ícone de login
            caminho = os.path.join(self.caminho_recursos, "log-in.png")
            self.icone_login.carregar_icone(caminho)
            # Esconder nome do usuário
            self.label_nome_usuario.hide()

    def _ao_clicar_icone(self, identificador):
        """Slot interno para reemitir o sinal do ícone clicado."""
        print(f"📡 GerenciadorIconesEsquerda: Ícone '{identificador}' acionado.")
        self.icone_clicado.emit(identificador)  # Re-emite o sinal para o consumidor (JanelaPrincipal)

    # Métodos para atualizar ícones, se necessário (ex: login/logout)
    def atualizar_icone(self, identificador, novo_caminho):
        """Atualiza a imagem de um ícone existente."""
        if identificador in self.icones:
            self.icones[identificador].carregar_icone(novo_caminho)
        else:
            print(f"⚠️ GerenciadorIconesEsquerda: Ícone '{identificador}' não encontrado para atualizar.")

    def remover_status_sala(self):
        """Remove o widget de status da sala da barra lateral, se existir."""
        if hasattr(self, 'widget_status_sala') and self.widget_status_sala is not None:
            layout = self.container.layout()
            if layout is not None and self.widget_status_sala in layout:
                layout.removeWidget(self.widget_status_sala)
            self.widget_status_sala.deleteLater()
            self.widget_status_sala = None
            print("🗑️ Widget de status da sala removido da barra lateral.")