# client/main.py

import sys
import os
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QSizePolicy, QFrame, QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QSurfaceFormat, QFont
from client.components.icon_manager import GerenciadorIconesEsquerda
from client.dialogs.auth_dialog import DialogoAutenticacao
from client.widgets.waiting_room_overlay import WaitingRoomOverlay
from client.widgets.offline_setup_overlay import OfflineSetupOverlay
from client.rendering.opengl_widget import OpenGLWidget
from client.widgets.match_overlay import OverlayPartida

# --- Componente Janela Principal ---
class JanelaPrincipal(QMainWindow):
    """
    Janela principal da aplicação, contendo a UI 2D e o widget OpenGL.
    Layout: Barras Superior/Inferior (5% da altura),
            Laterais (max(320px, 15% da largura)),
            Área Central para o conteúdo OpenGL.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Global Arena - Cliente PyQt6")

        # === Estado e Controle ===
        self.usuario_logado = self._verificar_login()
        self.loop_ativo = True
        self.overlay_sala = None
        self.polling_timer = None
        self.game_placeholder = None

        # === Dimensões da Tela ===
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        bar_height = int(screen_height * 0.05)
        sidebar_width = max(320, int(screen_width * 0.15))

        print(f"🎮 Janela PyQt6 criada. Tela: {screen_width}x{screen_height}. "
              f"Barras H: {bar_height}px, Barras V: {sidebar_width}px")

        # === Layout Principal da Janela ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_window_layout = QVBoxLayout(central_widget)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.setSpacing(0)

        # === Barra Superior ===
        self.barra_superior = self._criar_barra(bar_height, is_horizontal=True, object_name="BarraSuperior")
        layout_barra_superior = QHBoxLayout(self.barra_superior)
        layout_barra_superior.setContentsMargins(10, 5, 10, 5)
        label_status = QLabel("Status: Aguardando...")
        layout_barra_superior.addWidget(label_status)
        layout_barra_superior.addStretch()

        # === Conteúdo Principal (Barra Esquerda + Área Central + Barra Direita) ===
        conteudo_principal_widget = QWidget()
        conteudo_principal_layout = QHBoxLayout(conteudo_principal_widget)
        conteudo_principal_layout.setContentsMargins(0, 0, 0, 0)
        conteudo_principal_layout.setSpacing(0)

        # --- Barra Esquerda (com transparência) ---
        self.barra_esquerda = self._criar_barra(sidebar_width, is_horizontal=False, object_name="BarraEsquerda")
        self.barra_esquerda.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.barra_esquerda.setStyleSheet("""
            #BarraEsquerda {
                background-color: rgba(25, 25, 35, 180);
                border-right: 1px solid #3498db;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)
        layout_esquerda = QVBoxLayout(self.barra_esquerda)
        layout_esquerda.setContentsMargins(0, 0, 0, 0)

        self.gerenciador_icones = GerenciadorIconesEsquerda(caminho_recursos="client/resources")
        self.gerenciador_icones.icone_clicado.connect(self._ao_clicar_icone_lateral)

        if self.usuario_logado:
            try:
                with open("session.txt", "r") as f:
                    nome_usuario = f.read().strip()
                if not nome_usuario:
                    raise ValueError("Nome vazio")
            except Exception as e:
                print(f"❌ Erro ao ler session.txt: {e}")
                nome_usuario = "Player"
            self.gerenciador_icones.atualizar_estado_login(True, nome_usuario)
        else:
            self.gerenciador_icones.atualizar_estado_login(False)

        layout_esquerda.addWidget(self.gerenciador_icones)

        # --- Área Central (OpenGL + Overlay) ---
        area_central_widget = QWidget()
        area_central_layout = QHBoxLayout(area_central_widget)
        area_central_layout.setContentsMargins(0, 0, 0, 0)
        area_central_layout.setSpacing(0)

        # Container OpenGL
        self.opengl_container = QWidget()
        container_layout = QVBoxLayout(self.opengl_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Widget OpenGL
        self.opengl_widget = OpenGLWidget()
        self.opengl_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        container_layout.addWidget(self.opengl_widget)

        # Overlay de Boas-Vindas (centralizado)
        self.overlay_widget = QWidget(self.opengl_container)
        self.overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay_widget.setStyleSheet("background-color: rgba(0, 0, 0, 120); border: none;")

        overlay_layout = QVBoxLayout(self.overlay_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(10)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Labels (mantidos como antes)
        self.label_welcome = QLabel("Welcome to")
        font_welcome = QFont()
        font_welcome.setPointSize(14)
        font_welcome.setItalic(True)
        font_welcome.setWeight(500)
        self.label_welcome.setFont(font_welcome)
        self.label_welcome.setStyleSheet("color: #aaaaaa; background: transparent; border: none;")
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_titulo = QLabel("Global Arena")
        font_titulo = QFont()
        font_titulo.setPointSize(48)
        font_titulo.setBold(True)
        font_titulo.setWeight(700)
        self.label_titulo.setFont(font_titulo)
        self.label_titulo.setStyleSheet("""
            color: white;
            background-color: transparent;
            border: none;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
        """)
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_subtitulo = QLabel("the only one for non-flat-earthers")
        font_subtitulo = QFont()
        font_subtitulo.setPointSize(16)
        font_subtitulo.setItalic(True)
        self.label_subtitulo.setFont(font_subtitulo)
        self.label_subtitulo.setStyleSheet("""
            color: #cccccc;
            background-color: transparent;
            border: none;
            font-style: italic;
        """)
        self.label_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overlay_layout.addWidget(self.label_welcome)
        overlay_layout.addWidget(self.label_titulo)
        overlay_layout.addWidget(self.label_subtitulo)

        # --- Ajuste de Tamanho e Posição do Overlay ---
        def _safe_resize_event(event):
            self.overlay_widget.setGeometry(self.opengl_container.rect())
            self.overlay_widget.raise_()
            if hasattr(self, 'overlay_sala') and self.overlay_sala:
                self._ajustar_overlay_sala()
                self.overlay_sala.raise_()
            QWidget.resizeEvent(self.opengl_container, event)

        self.opengl_container.resizeEvent = _safe_resize_event

        # Mostrar overlay imediatamente
        self.overlay_widget.setGeometry(self.opengl_container.rect())
        self.overlay_widget.raise_()
        self.overlay_widget.show()

        QTimer.singleShot(50, lambda: [
            self.overlay_widget.setGeometry(self.opengl_container.rect()),
            self.overlay_widget.raise_(),
            self.overlay_widget.show()
        ])

        # Adicionar OpenGL ao layout central
        area_central_layout.addWidget(self.opengl_container)

        # --- Barra Direita (com transparência, mesma aparência da esquerda) ---
        self.barra_direita = self._criar_barra(sidebar_width, is_horizontal=False, object_name="BarraDireita")
        self.barra_direita.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.barra_direita.setStyleSheet("""
            #BarraDireita {
                background-color: rgba(25, 25, 35, 180);
                border-left: 1px solid #3498db;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)

        layout_direita = QVBoxLayout(self.barra_direita)
        layout_direita.addStretch()
        banner_placeholder = QLabel("Banner\n300x600")
        banner_placeholder.setFixedSize(300, 600)
        banner_placeholder.setStyleSheet("""
            background-color: rgba(30, 30, 40, 200);
            color: white;
            border: 1px solid #555;
            border-radius: 8px;
            font-size: 14px;
        """)
        banner_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_direita.addWidget(banner_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_direita.addStretch()

        # --- Adicionar widgets à área central ---
        area_central_layout.addWidget(self.opengl_container)
        area_central_layout.addWidget(self.barra_direita)

        # --- Adicionar barra esquerda e área central ao conteúdo principal ---
        conteudo_principal_layout.addWidget(self.barra_esquerda)
        conteudo_principal_layout.addWidget(area_central_widget)

        # === Barra Inferior ===
        self.barra_inferior = self._criar_barra(bar_height, is_horizontal=True, object_name="BarraInferior")
        self.barra_inferior.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.barra_inferior.setStyleSheet("""
            #BarraInferior {
                background-color: rgba(25, 25, 35, 180);
                border-top: 1px solid #3498db;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)
        layout_barra_inferior = QHBoxLayout(self.barra_inferior)
        layout_barra_inferior.addWidget(QLabel("Barra Inferior"))

        # === Montagem Final da Janela ===
        main_window_layout.addWidget(self.barra_superior)
        main_window_layout.addWidget(conteudo_principal_widget)
        main_window_layout.addWidget(self.barra_inferior)

        # === Loop de Atualização (60 FPS) ===
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_logica)
        self.timer.start(16)

        # === Exibição ===
        self.show()
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        # === Debug Final ===
        print("✅ Janela exibida. Overlay forçado a aparecer.")
        print("🔍 Geometria do container:", self.opengl_container.geometry())
        print("🔍 Geometria do overlay:", self.overlay_widget.geometry())
        print("🔍 Overlay visível?", self.overlay_widget.isVisible())

        self.partida_iniciada = False

        self.overlay_partida = OverlayPartida(parent=self.barra_esquerda)
        self.overlay_partida.hide()  # Começa escondido

    def _iniciar_partida(self, modo: str, **kwargs):
        """
        Método centralizado para iniciar qualquer tipo de partida.
        Garante que flags, overlays e estado sejam tratados de forma consistente.
        """
        print(f"🟢 [DEBUG] _iniciar_partida: Iniciando partida {modo}...")

        # ✅ Evitar múltiplas chamadas (evita bugs de duplo clique)
        if hasattr(self, 'partida_iniciada') and self.partida_iniciada:
            print("🟡 [DEBUG] _iniciar_partida: Partida já iniciada. Ignorando nova chamada.")
            return

        # ✅ Parar o loop de renderização antes de alterar a UI
        self.parar_loop()
        print("⏸️ [DEBUG] Render loop parado.")

        # --- Configuração específica por modo ---
        try:
            if modo == "offline":
                fator = kwargs.get("fator", 4)
                bioma = kwargs.get("bioma", "Meadow")
                print(f"🎮 [DEBUG] Modo offline: fator={fator}, bioma='{bioma}'")
                self._configurar_modo_offline(fator, bioma)

            elif modo == "online":
                # Lógica será tratada pelo sistema de fila e polling
                print("🌐 [DEBUG] Modo online: a lógica será gerenciada pelo MatchmakingService.")
                # Aqui pode-se adicionar: entrar_na_fila(), iniciar_polling(), etc.
                pass

            else:
                print(f"❌ [ERRO] Modo desconhecido: {modo}")
                return

        except Exception as e:
            print(f"❌ Erro ao configurar modo '{modo}': {e}")
            import traceback
            traceback.print_exc()
            return

        # ✅ Esconder overlays de espera (sala, boas-vindas, etc.)
        self._esconder_overlay_sala_espera()

        # ✅ Ativar modo de jogo no OpenGL
        if hasattr(self, 'opengl_widget') and self.opengl_widget:
            self.opengl_widget.ativar_modo_jogo()
            self.opengl_widget.update()
            print("🎮 [DEBUG] OpenGLWidget ativado e atualizado.")
        else:
            print("❌ [ERRO] opengl_widget não disponível para ativação.")

        # ✅ Chamar o método de finalização (limpeza, overlay de ações, etc.)
        print("🔵 [DEBUG] _iniciar_partida: Chamando on_partida_iniciada() para finalizar transição")
        self.on_partida_iniciada()

        print("✅ Transição para partida concluída.")

    def _configurar_modo_offline(self, fator, bioma):
        try:
            from shared.world import Mundo
            self.mundo = Mundo(fator=fator, bioma=bioma)
            print(
                f"✅ Mundo criado: fator={fator}, bioma='{bioma}', províncias={len(self.mundo.planeta.geografia.nodes)}")
            self.opengl_widget.carregar_mundo(self.mundo)

            # --- 🔁 Forçar reset da câmera para enxergar o planeta ---
            self.opengl_widget.camera.resetar(fator)

            # --- 🔹 DEFINIR CIVILIZAÇÃO DO JOGADOR HUMANO ---
            civilizacoes_player = [civ for civ in self.mundo.civs if civ.player]
            if civilizacoes_player:
                import random
                civ_jogador = random.choice(civilizacoes_player)
                civ_jogador.eh_jogador_local = True
                self.civ_jogador = civ_jogador
                print(f"🎮 Jogador humano definido: {civ_jogador.nome}")

                # - 🔹 CENTRALIZAR CÂMERA NA PROVÍNCIA INICIAL (DEPOIS DO RESET) -
                if civ_jogador.assentamentos:  # <-- Agora é 'assentamentos', não 'provincias'
                    assentamento_inicial = civ_jogador.assentamentos[0]
                    self.opengl_widget.centralizar_em(assentamento_inicial.coordenadas_tile)  # <-- coordenadas_tile
                    print(f"📍 Câmera centralizada no assentamento do jogador: {assentamento_inicial.coordenadas_tile}")
                else:
                    print("⚠️ [DEBUG] Jogador não tem assentamentos para centralizar.")

        except Exception as e:
            print(f"❌ Erro ao criar mundo offline: {e}")

    def _mostrar_dialogo_modos(self):
        """Exibe um diálogo para escolher entre modo Offline e Online."""
        # Evita múltiplas aberturas do diálogo
        if hasattr(self, '_modo_dialog_aberto') and self._modo_dialog_aberto:
            return
        self._modo_dialog_aberto = True

        modo_dialog = QDialog(self)
        modo_dialog.setWindowTitle("Modo de Jogo")
        modo_dialog.setModal(True)
        modo_dialog.resize(300, 150)
        modo_dialog.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                font-family: Arial;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        label = QLabel("Selecione o modo de jogo:")
        layout.addWidget(label)

        # Botões
        btn_offline = QPushButton("🎮 Offline")
        btn_offline.clicked.connect(lambda: [
            modo_dialog.accept(),
            self._mostrar_overlay_offline()
        ])
        btn_online = QPushButton("🌐 Online")

        layout.addWidget(btn_offline)
        layout.addWidget(btn_online)

        modo_dialog.setLayout(layout)

        # Prevenir aceitação automática
        modo_dialog.accepted.connect(lambda: None)

        def escolher_offline():
            modo_dialog.reject()
            self._modo_dialog_aberto = False
            self._ir_para_tela_pre_jogo(offline=True)

        def escolher_online():
            modo_dialog.reject()
            self._modo_dialog_aberto = False
            if self.usuario_logado:
                self._entrar_na_fila()
            else:
                # Abre o diálogo de login e entra na fila após sucesso
                self._abrir_dialogo_autenticacao_completo(
                    success_callback=lambda username: self._entrar_na_fila()
                )

        # Conectar botões
        btn_offline.clicked.connect(escolher_offline)
        btn_online.clicked.connect(escolher_online)

        # Limpar flag se o diálogo for fechado de outra forma (ex: ESC)
        modo_dialog.finished.connect(lambda: setattr(self, '_modo_dialog_aberto', False))

        modo_dialog.exec()

    def atualizar_logica(self):
        """Atualiza a lógica do jogo e solicita redesenho do OpenGL."""
        if not self.loop_ativo:
            return  # Evita update() se o loop foi desativado

        try:
            if hasattr(self, 'opengl_widget') and self.opengl_widget:
                self.opengl_widget.update()
        except RuntimeError:
            # Widget foi deletado — apenas pare o loop
            self.parar_loop()

    def parar_loop(self):
        """Para o loop de atualização gráfica."""
        self.loop_ativo = False
        if self.timer:
            self.timer.stop()

    def reiniciar_loop(self):
        """Reinicia o loop de atualização gráfica (útil ao voltar ao menu)."""
        if not self.loop_ativo:
            self.loop_ativo = True
            self.timer.start(18)

    def _verificar_login(self):
        """Verifica se o usuário está logado (exemplo: arquivo session.txt existe)."""
        return os.path.exists("session.txt")

    def _criar_barra(self, tamanho, is_horizontal, object_name="Barra"):
        """Cria um widget para representar uma barra, com estilo básico."""
        barra = QFrame()
        barra.setObjectName(object_name)
        if is_horizontal:
            barra.setFixedHeight(tamanho)
        else:
            barra.setFixedWidth(tamanho)
        barra.setStyleSheet(f"""
            #{object_name} {{
                background-color: #2c3e50;
                border: 1px solid #34495e;
            }}
        """)
        return barra

    def atualizar_logica(self):
        """
        Atualiza a lógica do jogo e solicita redesenho do OpenGL.
        """
        self.opengl_widget.update()

    def _ao_clicar_icone_lateral(self, identificador):
        """Lida com os cliques nos ícones da barra lateral esquerda."""
        print(f"🖱️ JanelaPrincipal recebeu clique no ícone: {identificador}")
        if identificador == "login":
            self.on_icone_login()
        elif identificador == "play":
            self.on_icone_play()
        elif identificador == "sair":
            self.on_icone_sair()

    def on_icone_login(self):
        """Ação acionada pelo ícone de login: abre tela de login ou logout."""
        if self.usuario_logado:
            # Já logado → oferece logout
            reply = QMessageBox.question(
                self,
                "Logout",
                "Você está logado. Deseja sair da conta?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    # ✅ Remove sessão
                    if os.path.exists("session.txt"):
                        os.remove("session.txt")
                        print("🗑️ session.txt removed (logout).")
                    # ✅ Atualiza estado
                    self.usuario_logado = False
                    self.gerenciador_icones.atualizar_estado_login(False)
                    # ✅ Feedback opcional (pode ser removido para UX mais limpa)
                    # QMessageBox.information(self, "Logout", "Você saiu com sucesso.")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Falha ao remover sessão: {e}")
        else:
            # Não logado → abre o diálogo completo com login e registro
            dialog = DialogoAutenticacao(self)

            def on_login_sucesso(username: str):
                """Callback chamado após login bem-sucedido."""
                self.usuario_logado = True
                self.gerenciador_icones.atualizar_estado_login(True, username)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                # ✅ O diálogo já garante que o login foi bem-sucedido
                try:
                    with open("session.txt", "r") as f:
                        nome_usuario = f.read().strip()
                    # Atualiza UI com o nome do usuário
                    self.usuario_logado = True
                    self.gerenciador_icones.atualizar_estado_login(True, nome_usuario)
                except Exception as e:
                    print(f"❌ Erro ao ler session.txt após login: {e}")
                    # Mesmo com erro, o login foi feito — usa fallback
                    self.gerenciador_icones.atualizar_estado_login(True, "Player")

    def on_icone_play(self):
        """Action triggered by the 'Play' icon: checks server state before acting."""
        print("🔵 [DEBUG] on_icone_play: Início da execução")
        print("Action: 'Play' icon clicked. Checking state...")

        # ✅ Stop render loop before any UI changes
        self.parar_loop()
        print("⏸️ [DEBUG] on_icone_play: Render loop parado")

        try:
            # ✅ 1. Verificar se o usuário está logado
            username = self._ler_username()
            print(f"🔵 [DEBUG] on_icone_play: Username lido de session.txt: '{username}'")

            if not username:
                print("🟡 [DEBUG] on_icone_play: Nenhum usuário logado. Mostrando diálogo de modos.")
                self._mostrar_dialogo_modos()
                return

            # ✅ 2. CONSULTAR ESTADO ANTES DE LIMPAR
            print("🔵 [DEBUG] on_icone_play: Consultando estado do jogador no servidor...")
            try:
                response = requests.post(
                    "http://localhost:5000/jogo/estado",
                    json={"username": username},
                    timeout=3
                )
                print(f"🟢 [DEBUG] on_icone_play: Resposta de /jogo/estado: {response.status_code} - {response.text}")

                if response.status_code == 200:
                    data = response.json()
                    print(f"🟢 [DEBUG] on_icone_play: Estado recebido: {data}")

                    if data.get("em_partida"):
                        print("⚠️ Jogador já está em partida. Mostrando placeholder...")
                        self.mostrar_tela_jogo()
                        return
                    elif data.get("em_fila"):
                        print("⚠️ Jogador já está na fila. Reexibindo overlay...")
                        # Opcional: reconectar ao estado da fila
                        # self._reconectar_a_fila(data)
                        pass
                else:
                    print(f"🟡 [DEBUG] on_icone_play: /jogo/estado retornou status {response.status_code}")
            except requests.exceptions.ConnectionError:
                print("🔴 [DEBUG] on_icone_play: Falha de conexão com o servidor. Assumindo estado limpo.")
            except requests.exceptions.Timeout:
                print("🔴 [DEBUG] on_icone_play: Tempo de resposta excedido. Assumindo estado limpo.")
            except requests.exceptions.RequestException as e:
                print(f"🔴 [DEBUG] on_icone_play: Falha de rede ao consultar estado: {e}")
            except Exception as e:
                print(f"🔴 [DEBUG] on_icone_play: Erro ao processar resposta de /jogo/estado: {e}")

            # ✅ 3. SE LIVRE, LIMPAR ESTADO E CONTINUAR
            print("🔵 [DEBUG] on_icone_play: Limpando estado do usuário no servidor...")
            try:
                response = requests.post(
                    "http://localhost:5000/jogo/limpar_usuario",
                    json={"username": username},
                    timeout=3
                )
                print(
                    f"🧹 Estado do usuário '{username}' limpo no servidor. Resposta: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                print("🟠 [DEBUG] on_icone_play: Servidor offline. Continuando sem limpeza.")
            except requests.exceptions.Timeout:
                print("🟠 [DEBUG] on_icone_play: Timeout ao limpar estado. Continuando.")
            except Exception as e:
                print(f"⚠️ Falha ao limpar estado no servidor: {e}")

            # ✅ 4. MOSTRAR DIÁLOGO DE MODOS
            print("🟢 [DEBUG] on_icone_play: Mostrando diálogo de escolha de modo (offline/online)")
            self._mostrar_dialogo_modos()

        except Exception as e:
            print(f"❌ Erro inesperado em on_icone_play: {e}")
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {e}")
            self._mostrar_dialogo_modos()

        print("🟢 [DEBUG] on_icone_play: Execução concluída")

    def _iniciar_offline(self, escolha, dialog):
        escolha[0] = "offline"
        dialog.accept()

    def _iniciar_online(self, escolha, dialog):
        escolha[0] = "online"
        dialog.accept()

        # Verifica login
        if not self.usuario_logado:
            print("Usuário não logado. Abrindo diálogo de autenticação...")
            self._abrir_dialogo_autenticacao_completo(success_callback=self._on_login_sucesso_pre_jogo)
        else:
            self._ir_para_tela_pre_jogo(offline=False)

    def _on_login_sucesso_pre_jogo(self, username: str):
        """Callback chamado após login bem-sucedido no fluxo de 'play online'."""
        print(f"✅ Login bem-sucedido. Iniciando pré-jogo online para {username}.")
        self._ir_para_tela_pre_jogo(offline=False)

    def _ir_para_tela_pre_jogo(self, offline: bool):
        if offline:
            self._mostrar_overlay_offline()  # ✅ Mostra o overlay de configuração
        else:
            self._entrar_na_fila()

    def on_icone_sair(self):
        """Action triggered by the 'Exit' icon: shows contextual dialog based on current state."""
        print("Action: 'Exit' icon clicked.")

        # ✅ Stop render loop (safe to call always)
        self.parar_loop()

        username = self._ler_username()
        if not username:
            # Se não está logado, fecha direto
            self.close()
            return

        # 🔥 Caso 1: Jogador está em partida ativa → diálogo avançado
        if self.partida_iniciada:
            self._mostrar_dialogo_saida_partida(username)
            return

        # 🔹 Caso 2: Não está em partida, mas está em sala de espera → perguntar antes de sair
        if hasattr(self, 'overlay_sala') and self.overlay_sala is not None:
            reply = QMessageBox.question(
                self,
                "Sair da Sala de Espera",
                "Você está em uma sala de espera. Sair agora cancelará sua participação.\n\n"
                "Deseja realmente sair?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return  # Cancela o fechamento

        # ✅ Limpar estado no servidor (em todos os casos)
        self._limpar_estado_servidor(username)

        # ✅ Limpeza local
        self._limpeza_local()

        # ✅ Fechar o programa
        self.close()

    def _limpar_estado_servidor(self, username: str):
        """Limpa o estado do jogador no servidor."""
        try:
            response = requests.post(
                "http://localhost:5000/jogo/limpar_usuario",
                json={"username": username},
                timeout=3
            )
            print(f"🧹 Estado do usuário '{username}' limpo no servidor ao sair. {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Falha ao limpar estado ao sair: {e}")

    def _limpeza_local(self):
        """Remove overlays, para timers, limpa o estado do OpenGL e restaura UI ao voltar ao menu."""
        print("🧹 [DEBUG] _limpeza_local: Iniciando limpeza completa...")

        # 1. Esconder overlay da sala de espera (se existir)
        try:
            if hasattr(self, 'overlay_sala') and self.overlay_sala is not None:
                print("🔵 [DEBUG] _limpeza_local: Escondendo overlay da sala de espera")
                self._esconder_overlay_sala_espera()
            else:
                print("🟡 [DEBUG] _limpeza_local: overlay_sala já removido ou inexistente")
        except Exception as e:
            print(f"⚠️ Falha ao remover overlay da sala: {e}")

        # 2. Parar e limpar polling_timer
        try:
            if hasattr(self, 'polling_timer') and self.polling_timer:
                self.polling_timer.stop()
                self.polling_timer.deleteLater()
                self.polling_timer = None
                print("⏸️ Polling de status da sala interrompido.")
            else:
                print("🟡 [DEBUG] _limpeza_local: polling_timer já parado ou inexistente")
        except Exception as e:
            print(f"⚠️ Falha ao parar polling: {e}")

        # 3. Limpar o mundo do OpenGLWidget (planeta, VAOs, VBOs)
        try:
            if hasattr(self, 'opengl_widget') and self.opengl_widget is not None:
                print("🧹 [DEBUG] _limpeza_local: Limpando mundo do OpenGLWidget")
                self.opengl_widget.limpar_mundo()  # Remove geometria, desativa modo jogo
            else:
                print("🟡 [DEBUG] _limpeza_local: opengl_widget não encontrado ou já destruído")
        except Exception as e:
            print(f"⚠️ Falha ao limpar opengl_widget: {e}")

        # 4. Esconder overlay de ações da partida (se existir)
        try:
            if hasattr(self, 'overlay_partida') and self.overlay_partida is not None:
                self.overlay_partida.hide()
                # ✅ Resetar exibição do overlay
                if hasattr(self.overlay_partida, 'label_turno'):
                    self.overlay_partida.label_turno.setText("Turno: 0")
                if hasattr(self.overlay_partida, 'label_pop'):
                    self.overlay_partida.label_pop.setText("Pop: 0")
                print("✅ [DEBUG] _limpeza_local: overlay_partida escondido e resetado.")
            else:
                print("🟡 [DEBUG] _limpeza_local: overlay_partida já removido ou inexistente")
        except Exception as e:
            print(f"⚠️ Falha ao esconder overlay_partida: {e}")

        # 5. Restaurar overlay de boas-vindas (se não estiver em modo jogo)
        try:
            if hasattr(self, 'overlay_widget') and self.overlay_widget is not None:
                # Mostrar apenas se NÃO estamos em uma partida
                if not (hasattr(self, 'partida_iniciada') and self.partida_iniciada):
                    self.overlay_widget.show()
                    self.overlay_widget.raise_()
                    print("✅ [DEBUG] _limpeza_local: Overlay de boas-vindas restaurado")
                else:
                    print("🟡 [DEBUG] _limpeza_local: Partida ainda ativa, não restaura overlay")
            else:
                print("🟡 [DEBUG] _limpeza_local: overlay_widget não encontrado")
        except Exception as e:
            print(f"⚠️ Falha ao restaurar overlay de boas-vindas: {e}")

        # 6. Resetar estado de partida
        self.partida_iniciada = False
        self.mundo = None  # ✅ Nova linha
        self.civ_jogador = None  # ✅ Nova linha
        print("✅ [DEBUG] _limpeza_local: Estado de partida resetado (partida_iniciada = False)")
        print("✅ [DEBUG] _limpeza_local: Referências ao mundo e jogador local limpas.")

        print("✅ [DEBUG] _limpeza_local: Limpeza concluída com sucesso.")

    def _mostrar_dialogo_saida_partida(self, username: str):
        """Mostra diálogo com Cancel, Main Menu, Quit quando em partida."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Sair do Jogo")
        dialog.setModal(True)
        dialog.setFixedSize(320, 150)
        dialog.setStyleSheet("""
            QDialog { background-color: #2c3e50; font-family: Arial; }
            QLabel { color: #ecf0f1; font-size: 14px; }
            QPushButton {
                background-color: #3498db; color: white; border: none;
                padding: 8px 16px; border-radius: 6px; font-size: 13px;
                min-width: 90px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton#quit { background-color: #e74c3c; }
            QPushButton#quit:hover { background-color: #c0392b; }
        """)

        layout = QVBoxLayout()
        label = QLabel("O que você gostaria de fazer?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_menu = QPushButton("Main Menu")
        btn_quit = QPushButton("Quit")
        btn_quit.setObjectName("quit")

        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_menu)
        button_layout.addWidget(btn_quit)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        # Ações
        btn_cancel.clicked.connect(dialog.reject)
        btn_menu.clicked.connect(lambda: self._sair_para_menu(dialog, username))
        btn_quit.clicked.connect(lambda: self._sair_do_jogo(dialog, username))

        dialog.exec()

    def _sair_para_menu(self, dialog, username: str):
        """Volta ao menu principal, limpa estado, mas não fecha o jogo."""
        dialog.accept()

        self._limpar_estado_servidor(username)
        self._limpeza_local()

        self.partida_iniciada = False  # ✅ Resetar flag

        # Restaurar overlay inicial
        if hasattr(self, 'overlay_widget') and self.overlay_widget:
            self.overlay_widget.show()
            self.overlay_widget.raise_()

        print("✅ Retornou ao menu principal.")

    def _sair_do_jogo(self, dialog, username: str):
        """Fecha o aplicativo após limpar estado."""
        dialog.accept()

        self._limpar_estado_servidor(username)
        self._limpeza_local()

        self.close()

    def _abrir_dialogo_autenticacao_completo(self, success_callback=None):
        """Abre o diálogo completo de autenticação (login + registro)."""
        dialog = DialogoAutenticacao(parent=self)

        def on_login_sucesso(username: str):
            with open("session.txt", "w") as f:
                f.write(username)
            self.usuario_logado = True
            self.gerenciador_icones.atualizar_estado_login(True, username)
            if success_callback:
                success_callback(username)
            dialog.accept()  # Fecha o diálogo

        def tentar_login():
            username = dialog.username_login.text().strip()
            password = dialog.senha_login.text()
            if not username or not password:
                QMessageBox.warning(dialog, "Erro", "Usuário e senha são obrigatórios.")
                return
            try:
                response = requests.post("http://localhost:5000/auth/login",
                                         json={"username": username, "password": password})
                data = response.json()
                if response.status_code == 200 and data.get("success"):
                    on_login_sucesso(username)
                else:
                    QMessageBox.critical(dialog, "Erro", data.get("message", "Login falhou."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(dialog, "Erro", "Não foi possível conectar ao servidor.")
            except Exception as e:
                QMessageBox.critical(dialog, "Erro", f"Erro: {str(e)}")

        def tentar_registro():
            username = dialog.username_registro.text().strip()
            password = dialog.senha_registro.text()
            confirmar = dialog.confirmar_senha.text()
            if not username or not password or not confirmar:
                QMessageBox.warning(dialog, "Erro", "Todos os campos são obrigatórios.")
                return
            if password != confirmar:
                QMessageBox.warning(dialog, "Erro", "As senhas não coincidem.")
                return
            if len(password) < 6:
                QMessageBox.warning(dialog, "Erro", "A senha deve ter pelo menos 6 caracteres.")
                return
            try:
                response = requests.post("http://localhost:5000/auth/registrar",
                                         json={"username": username, "password": password})
                data = response.json()
                if response.status_code == 200 and data.get("success"):
                    QMessageBox.information(dialog, "Sucesso", "Conta criada com sucesso! Faça login.")
                    # Preenche o campo de login e muda para aba de login
                    dialog.username_login.setText(username)
                    dialog.abas.setCurrentIndex(0)
                else:
                    QMessageBox.critical(dialog, "Erro", data.get("message", "Falha no registro."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(dialog, "Erro", "Não foi possível conectar ao servidor.")
            except Exception as e:
                QMessageBox.critical(dialog, "Erro", f"Erro: {str(e)}")

        # 🔁 Conecta os botões do QDialogButtonBox ao comportamento correto
        # Remover conexão anterior (se houver)
        try:
            dialog.buttons.accepted.disconnect()
        except TypeError:
            pass  # Já desconectado

        # Conecta "OK" ao comportamento da aba atual
        dialog.buttons.accepted.connect(
            lambda: tentar_login() if dialog.abas.currentIndex() == 0 else tentar_registro()
        )

        # "Cancel" já chama reject() → fecha o diálogo
        dialog.exec()

    def _abrir_tela_login(self):
        """Abre um diálogo de login com campos de usuário e senha."""

        dialog = QDialog(self)
        dialog.setWindowTitle("Entrar")
        dialog.setModal(True)
        dialog.resize(300, 120)

        layout = QFormLayout()

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Usuário:", username_input)
        layout.addRow("Senha:", password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        def tentar_login():
            username = username_input.text().strip()
            password = password_input.text()

            if not username or not password:
                QMessageBox.warning(dialog, "Erro", "Usuário e senha são obrigatórios.")
                return

            # Enviar requisição ao backend Flask
            try:
                response = requests.post(
                    "http://localhost:5000/auth/login",
                    json={"username": username, "password": password}
                )
                data = response.json()

                if response.status_code == 200 and data.get("success"):
                    # Login bem-sucedido
                    with open("session.txt", "w") as f:
                        f.write(username)
                    self.usuario_logado = True
                    # Atualiza UI: ícone + nome
                    self.gerenciador_icones.atualizar_estado_login(True, username)
                    QMessageBox.information(dialog, "Sucesso", f"Bem-vindo, {username}!")
                    dialog.accept()
                else:
                    QMessageBox.critical(dialog, "Erro", data.get("message", "Login falhou."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(dialog, "Erro", "Não foi possível conectar ao servidor.")
            except Exception as e:
                QMessageBox.critical(dialog, "Erro", f"Erro inesperado: {e}")

        buttons.accepted.connect(tentar_login)
        buttons.rejected.connect(dialog.reject)

        dialog.exec()

    def _entrar_na_fila(self):
        """Tenta entrar na fila de matchmaking e mostra a tela de espera como overlay.
        Garante limpeza proativa de estado anterior (servidor e cliente).
        """
        print("📞 Chamando /jogo/entrar...")

        # ✅ Evita múltiplas execuções simultâneas
        if hasattr(self, 'entrando_na_fila') and self.entrando_na_fila:
            print("⚠️ Já está entrando na fila. Operação ignorada.")
            return
        self.entrando_na_fila = True

        username = None
        try:
            # 1. Ler o username
            with open("session.txt", "r") as f:
                username = f.read().strip()
            if not username:
                raise FileNotFoundError("Arquivo de sessão vazio.")

            # 2. ✅ Limpeza proativa no servidor: força saída e limpa estado
            try:
                requests.post(
                    "http://localhost:5000/jogo/limpar_usuario",
                    json={"username": username},
                    timeout=3
                )
                print(f"🧹 Estado do usuário '{username}' limpo no servidor.")
            except Exception as e:
                print(f"⚠️ Falha ao limpar estado no servidor (servidor offline?): {e}")
                # Continua mesmo assim — pode ser um teste local

            # 3. ✅ Limpeza local: parar polling e remover overlays
            if hasattr(self, 'polling_timer') and self.polling_timer:
                self.polling_timer.stop()
                self.polling_timer.deleteLater()
                self.polling_timer = None

            # 4. ✅ Forçar remoção do overlay existente
            if hasattr(self, 'overlay_sala') and self.overlay_sala is not None:
                self._esconder_overlay_sala_espera()
            self.overlay_sala = None  # Garante que será recriado

            # 5. ✅ Entrar na fila
            response = requests.post(
                "http://localhost:5000/jogo/entrar",
                json={"modo": "online", "username": username},
                timeout=5
            )
            data = response.json()

            if data.get("success"):
                max_jogadores = data.get("max_jogadores")

                # 6. ✅ Mostrar overlay da sala de espera
                self._mostrar_overlay_sala_espera(username, max_jogadores)

                # 7. ✅ Iniciar polling para atualizar status
                self._iniciar_polling_sala()

                print(f"✅ {username} entrou na fila. Overlay exibido.")
            else:
                QMessageBox.critical(self, "Erro", data.get("message", "Falha ao entrar na fila."))

        except FileNotFoundError:
            QMessageBox.critical(self, "Erro", "Você não está logado.")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar ao servidor.")
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Erro", "Tempo de resposta excedido.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {e}")
            print(f"❌ Erro em _entrar_na_fila: {e}")
        finally:
            self.entrando_na_fila = False

    def on_partida_iniciada(self):
        """Chamado quando a partida começa (online ou offline).
        Realiza limpeza de UI, para polling, mostra overlay de ações
        e marca o estado de partida ativa.
        A criação do mundo e ativação do OpenGL devem ser feitas antes.
        """
        print("🔵 [DEBUG] on_partida_iniciada: Início da execução")

        # ✅ Evitar duplicação
        if hasattr(self, 'partida_iniciada') and self.partida_iniciada:
            print("🟡 [DEBUG] on_partida_iniciada: Já foi chamado. Ignorando.")
            return
        self.partida_iniciada = True
        print("🟢 [DEBUG] on_partida_iniciada: Flag 'partida_iniciada' definido como True")

        print("🎮 Partida iniciada: removendo overlays, status e parando polling...")

        # 1. Remover widget de status da barra lateral
        try:
            if hasattr(self, 'gerenciador_icones') and self.gerenciador_icones:
                print("🔵 [DEBUG] on_partida_iniciada: Removendo widget de status da barra lateral")
                self.gerenciador_icones.remover_status_sala()
                print("🗑️ Widget de status da sala removido.")
            else:
                print("🟡 [DEBUG] on_partida_iniciada: gerenciador_icones não encontrado")
        except Exception as e:
            print(f"⚠️ Falha ao remover status da sala: {e}")

        # 2. Esconder overlay da sala de espera
        try:
            if hasattr(self, 'overlay_sala') and self.overlay_sala is not None:
                print("🔵 [DEBUG] on_partida_iniciada: Removendo overlay da sala de espera")
                if hasattr(self.overlay_sala, 'fade_out'):
                    self.overlay_sala.fade_out()
                    from PyQt6.QtCore import QTimer
                    QTimer.singleShot(300, self._esconder_overlay_sala_espera)
                else:
                    self._esconder_overlay_sala_espera()
            else:
                print("🟡 [DEBUG] on_partida_iniciada: overlay_sala não encontrado")
        except Exception as e:
            print(f"⚠️ Falha ao esconder overlay da sala: {e}")

        # 3. Parar polling
        try:
            if hasattr(self, 'polling_timer') and self.polling_timer:
                self.polling_timer.stop()
                self.polling_timer.deleteLater()
                self.polling_timer = None
                print("⏸️ Polling de status da sala interrompido.")
            else:
                print("🟡 [DEBUG] on_partida_iniciada: polling_timer já parado")
        except Exception as e:
            print(f"⚠️ Falha ao parar polling: {e}")

        # 4. Ativar modo de jogo no OpenGLWidget
        try:
            if hasattr(self, 'opengl_widget') and self.opengl_widget:
                self.opengl_widget.ativar_modo_jogo()
                self.opengl_widget.update()
                print("🔵 [DEBUG] OpenGLWidget ativado e atualizado.")
            else:
                print("⚠️ [WARN] opengl_widget não encontrado ao ativar modo de jogo.")
        except Exception as e:
            print(f"⚠️ Falha ao ativar OpenGLWidget: {e}")

        # 5. ✅ CRIAR/MOSTRAR OVERLAY DE AÇÕES NA BARRA ESQUERDA
        try:
            from client.widgets.match_overlay import OverlayPartida
            if not hasattr(self, 'overlay_partida'):
                self.overlay_partida = OverlayPartida(parent=self.barra_esquerda)
                self.overlay_partida.hide()
                print("🟢 [DEBUG] OverlayPartida criado e anexado à barra_esquerda.")
            else:
                self.overlay_partida.update_position()

            self.overlay_partida.show()
            self.overlay_partida.raise_()
            print("✅ Overlay de ações de partida exibido e elevado na barra esquerda.")

            # 🔗 Conectar o mundo ao overlay
            self.overlay_partida.conectar_mundo(self.mundo)
            print("🔗 OverlayPartida conectado ao mundo.")

            # ✅ Conectar resizeEvent para ajuste automático
            if not hasattr(self.barra_esquerda, '_original_resize'):
                self.barra_esquerda._original_resize = self.barra_esquerda.resizeEvent

                def _new_resize(event):
                    self.barra_esquerda._original_resize(event)
                    if hasattr(self, 'overlay_partida'):
                        self.overlay_partida.update_position()

                self.barra_esquerda.resizeEvent = _new_resize

        except ImportError as e:
            print(f"❌ Falha ao importar OverlayPartida: {e}")
            print(
                "💡 Verifique se o arquivo 'client/widgets/match_overlay.py' existe e contém a classe 'OverlayPartida'.")
        except Exception as e:
            print(f"❌ Falha ao criar ou exibir OverlayPartida: {e}")
            import traceback
            traceback.print_exc()

        # 6. Finalização
        print("✅ Transição para partida iniciada com sucesso.")
        print("🟢 [DEBUG] on_partida_iniciada: Execução concluída")

    def mudar_modo_mapa(self, modo: str):
        """
        Recebe o comando do OverlayPartida e repassa ao OpenGLWidget.
        Este método precisa estar aqui porque o OverlayPartida usa 'parent_widget' como referência.
        """
        print(f"🔁 [DEBUG] JanelaPrincipal.mudar_modo_mapa chamado com modo='{modo}'")

        if hasattr(self, 'opengl_widget') and self.opengl_widget:
            if modo in ["fisico", "politico"]:
                self.opengl_widget.mudar_modo_mapa(modo)
            else:
                print(f"❌ Modo desconhecido: {modo}")
        else:
            print("❌ [ERRO] opengl_widget não disponível em JanelaPrincipal")

    def _mostrar_overlay_sala_espera(self, username: str, max_jogadores: int):
        """
        Mostra o overlay da sala de espera como sobreposição flutuante sobre o OpenGL,
        substituindo o 'Welcome to Global Arena', sem afetar o layout do OpenGL.
        """
        print("🔵 [DEBUG] _mostrar_overlay_sala_espera: Início da execução")
        print(
            f"🟢 [DEBUG] _mostrar_overlay_sala_espera: Tentando mostrar overlay para {username} | max_jogadores: {max_jogadores}")

        # 1. Se já existe um overlay da sala, remova-o corretamente
        if self.overlay_sala is not None:
            print(
                "🟡 [DEBUG] _mostrar_overlay_sala_espera: overlay_sala já existe. Chamando _esconder_overlay_sala_espera()")
            self._esconder_overlay_sala_espera()
        else:
            print("🟢 [DEBUG] _mostrar_overlay_sala_espera: Nenhum overlay existente. Continuando...")

        # 2. Esconder o overlay de boas-vindas
        if self.overlay_widget:
            self.overlay_widget.hide()
            print("🎨 [DEBUG] _mostrar_overlay_sala_espera: overlay_widget (boas-vindas) escondido")
        else:
            print("🟡 [DEBUG] _mostrar_overlay_sala_espera: overlay_widget não encontrado")

        # 3. Criar o novo overlay da sala de espera
        try:
            print("🔵 [DEBUG] _mostrar_overlay_sala_espera: Criando nova instância de WaitingRoomOverlay")
            self.overlay_sala = WaitingRoomOverlay(username, max_jogadores, parent=self.opengl_container)
            print("🟢 [DEBUG] _mostrar_overlay_sala_espera: WaitingRoomOverlay criado com sucesso")
        except Exception as e:
            print(f"❌ Falha ao criar WaitingRoomOverlay: {e}")
            if self.overlay_widget:
                self.overlay_widget.show()  # Restaura se falhar
            return

        # 4. Adicionar como widget filho direto (sem usar layout) → evita interferência no OpenGL
        self.overlay_sala.setParent(self.opengl_container)
        print("🔵 [DEBUG] _mostrar_overlay_sala_espera: overlay_sala definido como filho de opengl_container")

        self.overlay_sala.hide()  # Inicialmente oculto para ajustar posição primeiro
        print("🟡 [DEBUG] _mostrar_overlay_sala_espera: overlay_sala inicialmente oculto para ajuste de posição")

        # 5. Ajustar posição e tamanho com base no container (será refinado após renderização)
        print("🔵 [DEBUG] _mostrar_overlay_sala_espera: Ajustando posição inicial do overlay")
        self._ajustar_overlay_sala()

        # 6. Exibir o overlay
        self.overlay_sala.show()
        self.overlay_sala.raise_()  # Garante que fique na frente
        print("🟢 [DEBUG] _mostrar_overlay_sala_espera: overlay_sala exibido e trazido para frente (raise_)")

        # 7. Conectar o botão Cancelar com a lógica de saída
        def on_cancel():
            print(f"🔵 [DEBUG] on_cancel: {username} clicou em Cancelar")
            try:
                import requests
                response = requests.post(
                    "http://localhost:5000/jogo/sair",
                    json={"username": username},
                    timeout=3
                )
                print(f"📤 {username} saiu da fila via cancelamento. Resposta: {response.status_code}")
            except Exception as e:
                print(f"❌ Falha ao sair da fila: {e}")
            finally:
                # Sempre esconder o overlay após tentar sair
                print("🔵 [DEBUG] on_cancel: Chamando _esconder_overlay_sala_espera()")
                self._esconder_overlay_sala_espera()

        # Conectar o callback ao botão Cancelar
        self.overlay_sala.connect_cancel(on_cancel)
        print("🟢 [DEBUG] _mostrar_overlay_sala_espera: Callback de cancelamento conectado")

        # 8. 👉 Garantir posicionamento pós-renderização (evita geometria 0x0)
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(30, self._ajustar_overlay_sala)
        print("🔵 [DEBUG] _mostrar_overlay_sala_espera: QTimer.singleShot(30) agendado para _ajustar_overlay_sala")

        QTimer.singleShot(60, lambda: self.overlay_sala.raise_() if self.overlay_sala else None)
        print("🔵 [DEBUG] _mostrar_overlay_sala_espera: QTimer.singleShot(60) agendado para garantir raise_()")

        print("🟢 [DEBUG] _mostrar_overlay_sala_espera: Execução concluída")

    def _esconder_overlay_sala_espera(self):
        """Esconde o overlay da sala de espera e restaura o estado inicial."""
        print("🔵 [DEBUG] _esconder_overlay_sala_espera: Início da execução")

        # 1. Parar polling
        if hasattr(self, 'polling_timer') and self.polling_timer:
            self.polling_timer.stop()
            self.polling_timer = None
            print("🟡 [DEBUG] _esconder_overlay_sala_espera: polling_timer já parado ou inexistente")

        # 2. Remover overlay da sala
        if hasattr(self, 'overlay_sala') and self.overlay_sala:
            self.overlay_sala.setParent(None)
            self.overlay_sala.deleteLater()
            self.overlay_sala = None
            print("🎨 [DEBUG] _esconder_overlay_sala_espera: overlay_sala já removido ou inexistente")

        # 3. ✅ Mostrar overlay_widget (boas-vindas) só se NÃO estiver em modo jogo
        if hasattr(self, 'opengl_widget') and not self.opengl_widget.modulo_jogo:
            if hasattr(self, 'overlay_widget') and self.overlay_widget:
                self.overlay_widget.show()
                self.overlay_widget.raise_()
                print("🎨 [DEBUG] _esconder_overlay_sala_espera: overlay_widget (boas-vindas) restaurado")
        else:
            # ✅ Se estiver em modo jogo, NÃO mostre o overlay de boas-vindas
            if hasattr(self, 'overlay_widget') and self.overlay_widget:
                self.overlay_widget.hide()
                print("🎨 [DEBUG] _esconder_overlay_sala_espera: overlay_widget escondido (modo jogo ativo)")

        print("🟢 [DEBUG] _esconder_overlay_sala_espera: Execução concluída")

    def _ajustar_overlay_sala(self):
        """Ajusta posição e tamanho do overlay da sala de espera, garantindo centralização e responsividade.
        Protegido contra chamadas prematuras (ex: geometria 0x0)."""
        if not self.overlay_sala or not self.opengl_container:
            return

        container_rect = self.opengl_container.rect()

        # ✅ Proteção contra chamadas prematuras (tamanho inválido)
        if container_rect.width() < 10 or container_rect.height() < 10:
            print("⚠️ _ajustar_overlay_sala adiado: container ainda não tem dimensões válidas.")
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(20, self._ajustar_overlay_sala)  # Tenta novamente em breve
            return

        # ✅ Calcular dimensões responsivas
        max_width = 500
        min_width = 300
        padding_horizontal = 60
        target_width = min(max_width, container_rect.width() - padding_horizontal)
        width = max(min_width, target_width)  # Garante largura mínima

        height = 300  # Altura fixa suficiente para o conteúdo

        # ✅ Centralizar
        x = (container_rect.width() - width) // 2
        y = (container_rect.height() - height) // 2

        # ✅ Aplicar geometria
        self.overlay_sala.setGeometry(x, y, width, height)
        self.overlay_sala.raise_()  # Garante que fique na frente

        print(f"🎨 Overlay ajustado: ({x}, {y}, {width}x{height}) dentro de {container_rect.size()}")

    def _iniciar_polling_sala(self):
        """Inicia o polling para atualizar o status da sala de espera a cada 1 segundo."""
        from PyQt6.QtCore import QTimer

        print("🔵 [DEBUG] _iniciar_polling_sala: Iniciando ou reiniciando polling")

        # 1. Parar qualquer timer anterior
        if hasattr(self, 'polling_timer') and self.polling_timer:
            print("⏸️ [DEBUG] _iniciar_polling_sala: Parando polling_timer existente")
            self.polling_timer.stop()
            self.polling_timer.deleteLater()
            self.polling_timer = None

        # 2. Criar novo timer
        self.polling_timer = QTimer(self)

        # 3. Conectar ao novo método de atualização
        self.polling_timer.timeout.connect(self._atualizar_status_sala)

        # 4. Iniciar polling
        self.polling_timer.start(1000)  # A cada 1 segundo
        print("🟢 [DEBUG] _iniciar_polling_sala: polling_timer iniciado (1s)")

        # 5. Atualização imediata
        self._atualizar_status_sala()
        print("🟢 [DEBUG] _iniciar_polling_sala: Primeira atualização de status disparada")

    def _atualizar_status_sala(self):
        """Atualiza o status da sala com base na sala do jogador."""
        try:
            username = self._ler_username()
            if not username:
                print("🟡 [DEBUG] _atualizar_status_sala: Nenhum usuário logado. Ignorando.")
                return

            print(f"🔵 [DEBUG] _atualizar_status_sala: Consultando /jogo/minha_sala para {username}")
            response = requests.post(
                "http://localhost:5000/jogo/minha_sala",
                json={"username": username},
                timeout=3
            )
            if response.status_code == 200:
                data = response.json()
                print(f"🟢 [DEBUG] _atualizar_status_sala: Estado recebido: {data}")

                if data.get("em_fila"):
                    jogadores = data["jogadores_na_sala"]
                    vagas = data["vagas"]
                    esta_cheia = data["esta_cheia"]

                    # Atualiza o overlay da sala de espera
                    if hasattr(self, 'overlay_sala') and self.overlay_sala is not None:
                        print(f"🎨 [DEBUG] _atualizar_status_sala: Atualizando overlay para {len(jogadores)}/{vagas}")
                        self.overlay_sala.atualizar_status(len(jogadores), vagas)
                    else:
                        print("🟡 [DEBUG] _atualizar_status_sala: overlay_sala não encontrado")

                    # Se a sala encheu, inicia a partida
                    if esta_cheia:
                        print(
                            f"✅ [DEBUG] _atualizar_status_sala: Sala cheia detectada ({len(jogadores)}/{vagas}). Iniciando partida.")
                        self._esconder_overlay_sala_espera()
                        if hasattr(self, 'polling_timer') and self.polling_timer:
                            self.polling_timer.stop()
                            self.polling_timer.deleteLater()
                            self.polling_timer = None
                            print("⏸️ [DEBUG] _atualizar_status_sala: polling_timer parado")
                        self.on_partida_iniciada()
                else:
                    # Jogador não está mais na fila
                    print("🟡 [DEBUG] _atualizar_status_sala: Jogador não está na fila. Escondendo overlay.")
                    self._esconder_overlay_sala_espera()
            else:
                print(f"🔴 [DEBUG] _atualizar_status_sala: /jogo/minha_sala retornou status {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("🔴 [DEBUG] _atualizar_status_sala: Falha de conexão com o servidor.")
        except requests.exceptions.Timeout:
            print("🔴 [DEBUG] _atualizar_status_sala: Tempo de resposta excedido.")
        except requests.exceptions.RequestException as e:
            print(f"🔴 [DEBUG] _atualizar_status_sala: Erro de rede: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado em _atualizar_status_sala: {e}")

    def sair_da_partida(self):
        """Sai da partida e volta para o menu principal."""
        if self.game_placeholder:
            self.game_placeholder.setParent(None)
            self.game_placeholder.deleteLater()
            self.game_placeholder = None

        # Restaurar overlay de boas-vindas
        if self.overlay_widget:
            self.overlay_widget.show()
            self.overlay_widget.raise_()

        print("✅ Retornou ao menu principal.")

    def _ler_username(self) -> str:
        """Lê o username do arquivo session.txt. Retorna string vazia se não encontrado."""
        try:
            with open("session.txt", "r", encoding="utf-8") as f:
                username = f.read().strip()
            if username:
                return username
            else:
                print("⚠️ Arquivo session.txt encontrado, mas vazio.")
                return ""
        except FileNotFoundError:
            print("⚠️ Arquivo session.txt não encontrado.")
            return ""
        except Exception as e:
            print(f"❌ Erro ao ler session.txt: {e}")
            return ""

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Ajustar overlay de boas-vindas
        if hasattr(self, 'overlay_widget') and self.overlay_widget:
            self.overlay_widget.setGeometry(self.opengl_container.rect())
            self.overlay_widget.raise_()

        # Ajustar overlay da sala de espera (se existir)
        if hasattr(self, 'overlay_sala') and self.overlay_sala:
            self._ajustar_overlay_sala()  # Este método já existe
            self.overlay_sala.raise_()

        # Ajustar barra direita (se for flutuante)
        if hasattr(self, 'barra_direita') and self.barra_direita.parent() == self.opengl_container:
            w = self.barra_direita.width()
            h = self.opengl_container.height()
            self.barra_direita.setGeometry(self.opengl_container.width() - w, 0, w, h)
            self.barra_direita.raise_()

        # Forçar atualização do OpenGL
        if hasattr(self, 'opengl_widget'):
            self.opengl_widget.update()

    def _mostrar_overlay_offline(self):
        """Mostra o overlay de configuração offline sobre o OpenGL."""
        print("🔵 [DEBUG] _mostrar_overlay_offline: Exibindo overlay de configuração offline")

        # ✅ Esconder overlay de boas-vindas ANTES de mostrar o offline
        if hasattr(self, 'overlay_widget') and self.overlay_widget:
            self.overlay_widget.hide()

        # Criar ou reutilizar overlay
        if not hasattr(self, 'offline_overlay'):
            self.offline_overlay = OfflineSetupOverlay(parent=self.opengl_container)
            self.offline_overlay.setParent(self.opengl_container)

            # 🔥 CONECTAR O SINAL AQUI, logo após a criação
            self.offline_overlay.on_start.connect(self.on_offline_setup_confirmed)
            print("✅ [DEBUG] Sinal 'on_start' conectado a 'on_offline_setup_confirmed'")
        else:
            self.offline_overlay.show()

        self.offline_overlay.raise_()
        self.offline_overlay.show()

    def on_offline_setup_confirmed(self, fator, bioma):
        """Configuração confirmada. Inicia a partida offline."""
        print(f"🟢 [DEBUG] on_offline_setup_confirmed: Iniciando partida offline | fator={fator}, bioma='{bioma}'")
        # ❌ REMOVA: self.on_partida_iniciada()
        # ✅ APENAS inicia a partida
        self._iniciar_partida("offline", fator=fator, bioma=bioma)

    def on_offline_setup_canceled(self):
        """Chamado ao cancelar. Restaura o overlay de boas-vindas."""
        print("🟡 [DEBUG] Modo offline cancelado. Restaurando overlay de boas-vindas.")

        # Esconder o overlay offline
        if hasattr(self, 'offline_overlay') and self.offline_overlay:
            self.offline_overlay.hide()

        # Mostrar e trazer para frente o overlay de boas-vindas
        if hasattr(self, 'overlay_widget') and self.overlay_widget:
            self.overlay_widget.show()
            self.overlay_widget.raise_()

        # Opcional: forçar update do OpenGL (para garantir render)
        if hasattr(self, 'opengl_widget'):
            self.opengl_widget.update()


# --- Ponto de Entrada da Aplicação ---
def main():
    print("🎮 Inicializando cliente gráfico com PyQt6...")

    # Configurar o formato OpenGL padrão globalmente
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setDepthBufferSize(24)  # ✅ Ativado: necessário para 3D
    fmt.setStencilBufferSize(8)  # ✅ Adicionado: útil para efeitos futuros
    fmt.setSamples(4)  # ✅ Ativado: 4x MSAA para suavização
    fmt.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    fmt.setAlphaBufferSize(8)
    fmt.setRedBufferSize(8)
    fmt.setGreenBufferSize(8)
    fmt.setBlueBufferSize(8)

    QSurfaceFormat.setDefaultFormat(fmt)

    app = QApplication(sys.argv)

    try:
        janela = JanelaPrincipal()
        janela.show()  # Garante que a janela será exibida
        print("✅ Janela principal exibida.")
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ Erro ao criar/iniciar a janela: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 🔥 Ativar suporte a alto DPI ANTES de criar QApplication
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # (Opcional) Para testar o ícone de login logado
    # with open("session.txt", "w") as f:
    #     f.write("usuario_teste_logado")

    main()  # Chama a função principal