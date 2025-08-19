# client/main.py

import sys
import os  # Para verificar o arquivo de sessão
import OpenGL.GL as gl
import ctypes

import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QSizePolicy, QFrame, QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QSurfaceFormat, QFont
from components.icon_manager import GerenciadorIconesEsquerda
from dialogs.auth_dialog import DialogoAutenticacao


# --- Componente OpenGL ---
class MeuOpenGLWidget(QOpenGLWidget):
    """
    Widget responsável pela renderização OpenGL Moderna.
    """

    def __init__(self):
        super().__init__()
        self.shader_program = None
        self.VAO = None
        self.VBO = None
        # Permitir que o widget receba foco de teclado
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initializeGL(self):
        """
        Inicializado uma vez quando o contexto OpenGL é criado.
        Aqui compilamos shaders, criamos VAOs, VBOs etc.
        """
        print("Inicializando contexto OpenGL...")
        # Define a cor de fundo padrão como PRETO PURO
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)

        # --- Compilar Shaders para o Triângulo ---
        vertex_shader_source = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aColor;
        out vec3 ourColor;
        void main()
        {
            gl_Position = vec4(aPos, 1.0);
            ourColor = aColor;
        }
        """

        fragment_shader_source = """
        #version 330 core
        in vec3 ourColor;
        out vec4 FragColor;
        void main()
        {
            FragColor = vec4(ourColor, 1.0f);
        }
        """

        # --- Compilação e Linkagem de Shaders ---
        try:
            # Compilação do Vertex Shader
            vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
            gl.glShaderSource(vertex_shader, vertex_shader_source)
            gl.glCompileShader(vertex_shader)
            # Verificação de erros no vertex shader
            success = gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)
            if not success:
                info_log = gl.glGetShaderInfoLog(vertex_shader)
                raise RuntimeError(f"Erro ao compilar Vertex Shader:\n{info_log.decode('utf-8')}")

            # Compilação do Fragment Shader
            fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
            gl.glShaderSource(fragment_shader, fragment_shader_source)
            gl.glCompileShader(fragment_shader)
            # Verificação de erros no fragment shader
            success = gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS)
            if not success:
                info_log = gl.glGetShaderInfoLog(fragment_shader)
                raise RuntimeError(f"Erro ao compilar Fragment Shader:\n{info_log.decode('utf-8')}")

            # Linkagem do Programa Shader
            self.shader_program = gl.glCreateProgram()
            gl.glAttachShader(self.shader_program, vertex_shader)
            gl.glAttachShader(self.shader_program, fragment_shader)
            gl.glLinkProgram(self.shader_program)
            # Verificação de erros no link
            success = gl.glGetProgramiv(self.shader_program, gl.GL_LINK_STATUS)
            if not success:
                info_log = gl.glGetProgramInfoLog(self.shader_program)
                raise RuntimeError(f"Erro ao linkar Programa Shader:\n{info_log.decode('utf-8')}")

            # Deletar os shaders já linkados
            gl.glDeleteShader(vertex_shader)
            gl.glDeleteShader(fragment_shader)

        except RuntimeError as e:
            print(f"❌ Erro na inicialização dos shaders: {e}")
            self.shader_program = None  # Indica falha
            return  # Aborta a inicialização da geometria se shaders falharem

        # --- Configurar VAO e VBO para um triângulo ---
        try:
            # Dados do triângulo (Posição XYZ + Cor RGB)
            triangle_data = [
                0.0, 0.5, 0.0, 1.0, 0.0, 0.0,  # Vértice 0: Topo (Vermelho)
                -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,  # Vértice 1: Esquerda (Verde)
                0.5, -0.5, 0.0, 0.0, 0.0, 1.0  # Vértice 2: Direita (Azul)
            ]
            triangle_data = (gl.GLfloat * len(triangle_data))(*triangle_data)

            # Gerar e vincular VAO
            self.VAO = gl.glGenVertexArrays(1)
            gl.glBindVertexArray(self.VAO)

            # Gerar e vincular VBO
            self.VBO = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.VBO)
            gl.glBufferData(gl.GL_ARRAY_BUFFER, ctypes.sizeof(triangle_data), triangle_data, gl.GL_STATIC_DRAW)

            # Definir atributos de vértice
            stride = 6 * ctypes.sizeof(gl.GLfloat)
            # Posição (location = 0)
            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(0))
            gl.glEnableVertexAttribArray(0)
            # Cor (location = 1)
            gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride,
                                     ctypes.c_void_p(3 * ctypes.sizeof(gl.GLfloat)))
            gl.glEnableVertexAttribArray(1)

            # Desvincular VAO/VBO
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glBindVertexArray(0)

            print("✅ Shaders compilados e geometria do triângulo configurada.")

        except Exception as e:
            print(f"❌ Erro ao configurar geometria do triângulo: {e}")
            # Limpar shaders em caso de falha na geometria
            if self.shader_program:
                gl.glDeleteProgram(self.shader_program)
                self.shader_program = None
            self.VAO = None
            self.VBO = None

    def resizeGL(self, w, h):
        """
        Chamado sempre que o widget é redimensionado.
        """
        print(f"Redimensionando OpenGL para {w}x{h}")
        gl.glViewport(0, 0, w, h)
        # TODO: Atualizar matriz de projeção se necessário

    def paintGL(self):
        """
        Chamado sempre que a cena OpenGL precisa ser redesenhada.
        """
        # Limpa o buffer com a cor definida em initializeGL
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

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

        # --- Verificar estado de login ANTES de criar os ícones ---
        self.usuario_logado = self._verificar_login()

        # --- Obter dimensões da tela para cálculos ---
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # --- Calcular dimensões das barras ---
        bar_height = int(screen_height * 0.05)
        sidebar_width = max(320, int(screen_width * 0.15))

        print(f"🎮 Janela PyQt6 criada. Tela: {screen_width}x{screen_height}. "
              f"Barras H: {bar_height}px, Barras V: {sidebar_width}px")

        # --- Configuração do Layout Central ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_window_layout = QVBoxLayout(central_widget)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.setSpacing(0)

        # --- Barra Superior ---
        self.barra_superior = self._criar_barra(bar_height, is_horizontal=True, object_name="BarraSuperior")
        layout_barra_superior = QHBoxLayout(self.barra_superior)
        layout_barra_superior.setContentsMargins(10, 5, 10, 5)
        label_status = QLabel("Status: Aguardando...")
        layout_barra_superior.addWidget(label_status)
        layout_barra_superior.addStretch()

        # --- Conteúdo Principal ---
        conteudo_principal_widget = QWidget()
        conteudo_principal_layout = QHBoxLayout(conteudo_principal_widget)
        conteudo_principal_layout.setContentsMargins(0, 0, 0, 0)
        conteudo_principal_layout.setSpacing(0)

        # --- Barra Esquerda com Ícones Interativos ---
        self.barra_esquerda = self._criar_barra(sidebar_width, is_horizontal=False, object_name="BarraEsquerda")

        # Criar gerenciador de ícones
        self.gerenciador_icones = GerenciadorIconesEsquerda(caminho_recursos="client/resources")

        # Atualizar ícone e nome de login com base no estado
        if self.usuario_logado:
            try:
                with open("session.txt", "r") as f:
                    nome_usuario = f.read().strip()
            except Exception as e:
                print(f"❌ Erro ao ler session.txt: {e}")
                nome_usuario = "Usuário"
            self.gerenciador_icones.atualizar_estado_login(True, nome_usuario)

        # Conectar sinal de clique
        self.gerenciador_icones.icone_clicado.connect(self._ao_clicar_icone_lateral)

        # Layout da barra esquerda
        layout_esquerda = QVBoxLayout(self.barra_esquerda)
        layout_esquerda.setContentsMargins(0, 0, 0, 0)
        layout_esquerda.addWidget(self.gerenciador_icones)

        # --- Área Central (OpenGL + Barra Direita) ---
        area_central_widget = QWidget()
        area_central_layout = QHBoxLayout(area_central_widget)
        area_central_layout.setContentsMargins(0, 0, 0, 0)
        area_central_layout.setSpacing(0)

        # --- Criar o Container para OpenGL e Overlay do Título ---
        self.opengl_container = QWidget()
        container_layout = QVBoxLayout(self.opengl_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # --- Widget OpenGL ---
        self.opengl_widget = MeuOpenGLWidget()
        self.opengl_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # --- Criar o Overlay Widget para o Título ---
        self.overlay_widget = QWidget(self.opengl_container)
        self.overlay_widget.setWindowFlags(Qt.WindowType.Widget)
        self.overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay_widget.setStyleSheet("background: transparent; border: none;")

        # --- Layout do Overlay para o Título e Subtítulo ---
        overlay_layout = QVBoxLayout(self.overlay_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(10)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Label: "Welcome to" ---
        self.label_welcome = QLabel("Welcome to")
        font_welcome = QFont()
        font_welcome.setPointSize(14)
        font_welcome.setItalic(True)
        font_welcome.setWeight(500)
        self.label_welcome.setFont(font_welcome)
        self.label_welcome.setStyleSheet("color: #aaaaaa; background: transparent; border: none;")
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Label: "Global Arena" ---
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

        # --- Label: Subtítulo ---
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

        # --- Adicionar ao layout na ordem correta ---
        overlay_layout.addWidget(self.label_welcome)
        overlay_layout.addWidget(self.label_titulo)
        overlay_layout.addWidget(self.label_subtitulo)

        # --- Adicionar Widgets ao Container OpenGL ---
        container_layout.addWidget(self.opengl_widget)

        # --- Correção robusta do resizeEvent ---
        def _safe_resize_event(event):
            self.overlay_widget.setGeometry(self.opengl_container.rect())
            self.overlay_widget.raise_()
            QWidget.resizeEvent(self.opengl_container, event)

        self.opengl_container.resizeEvent = _safe_resize_event

        # --- FORÇAR O OVERLAY A APARECER IMEDIATAMENTE ---
        self.overlay_widget.setGeometry(self.opengl_container.rect())
        self.overlay_widget.raise_()
        self.overlay_widget.show()

        # --- Fallback pós-show: Garante posicionamento após renderização inicial ---
        QTimer.singleShot(50, lambda: [
            self.overlay_widget.setGeometry(self.opengl_container.rect()),
            self.overlay_widget.raise_(),
            self.overlay_widget.show()
        ])

        # --- Barra Direita ---
        self.barra_direita = self._criar_barra(sidebar_width, is_horizontal=False, object_name="BarraDireita")
        layout_direita = QVBoxLayout(self.barra_direita)
        layout_direita.addStretch()
        banner_placeholder = QLabel("Banner\n300x600")
        banner_placeholder.setFixedSize(300, 600)
        banner_placeholder.setStyleSheet("background-color: #333; color: white; border: 1px solid gray;")
        banner_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_direita.addWidget(banner_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_direita.addStretch()

        # --- Adicionar widgets à área central ---
        area_central_layout.addWidget(self.opengl_container)
        area_central_layout.addWidget(self.barra_direita)

        # --- Adicionar widgets ao conteúdo principal ---
        conteudo_principal_layout.addWidget(self.barra_esquerda)
        conteudo_principal_layout.addWidget(area_central_widget)

        # --- Barra Inferior ---
        self.barra_inferior = self._criar_barra(bar_height, is_horizontal=True, object_name="BarraInferior")
        layout_barra_inferior = QHBoxLayout(self.barra_inferior)
        layout_barra_inferior.addWidget(QLabel("Barra Inferior"))

        # --- Adicionar todos os componentes ao layout da janela ---
        main_window_layout.addWidget(self.barra_superior)
        main_window_layout.addWidget(conteudo_principal_widget)
        main_window_layout.addWidget(self.barra_inferior)

        # --- Timer para o Loop Principal ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_logica)
        self.timer.start(16)  # ~60 FPS

        # --- Mostrar e aplicar fullscreen ---
        self.show()
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        # --- Debug final ---
        print("✅ Janela exibida. Overlay forçado a aparecer.")
        print("🔍 Geometria do container:", self.opengl_container.geometry())
        print("🔍 Geometria do overlay:", self.overlay_widget.geometry())
        print("🔍 Overlay visível?", self.overlay_widget.isVisible())

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
                "Você está logado. Deseja sair?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.remove("session.txt")
                    self.usuario_logado = False
                    self.gerenciador_icones.atualizar_estado_login(False)
                    QMessageBox.information(self, "Logout", "Você saiu com sucesso.")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Falha ao remover sessão: {e}")
        else:
            # Não logado → abre o novo diálogo com Login/Registro
            dialog = DialogoAutenticacao(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Após login bem-sucedido, atualiza UI
                try:
                    with open("session.txt", "r") as f:
                        nome_usuario = f.read().strip()
                    self.usuario_logado = True
                    self.gerenciador_icones.atualizar_estado_login(True, nome_usuario)
                except Exception as e:
                    print(f"❌ Erro ao ler session.txt: {e}")

    def on_icone_play(self):
        """Ação acionada pelo ícone de play: oferece modo offline ou online."""
        print("Ação: Ícone 'Play' clicado. Oferecendo modos de jogo...")

        modo_dialog = QDialog(self)
        modo_dialog.setWindowTitle("Modo de Jogo")
        modo_dialog.setModal(True)
        modo_dialog.resize(300, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Escolha o modo de jogo:"))

        btn_offline = QPushButton("Offline")
        btn_online = QPushButton("Online")

        layout.addWidget(btn_offline)
        layout.addWidget(btn_online)

        modo_dialog.setLayout(layout)

        # Vamos controlar o fechamento manualmente
        modo_dialog.accepted.connect(lambda: None)  # Desativar aceitação automática

        def escolher_offline():
            modo_dialog.reject()  # Fecha sem aceitar (para não disparar lógica de online)
            self._ir_para_tela_pre_jogo(offline=True)

        def escolher_online():
            modo_dialog.reject()  # Fecha o diálogo de modo, mas mantém o controle
            if self.usuario_logado:
                self._ir_para_tela_pre_jogo(offline=False)
            else:
                # Abre o diálogo completo (login + registro)
                self._abrir_dialogo_autenticacao_completo(
                    success_callback=lambda u: self._ir_para_tela_pre_jogo(offline=False))

        btn_offline.clicked.connect(escolher_offline)
        btn_online.clicked.connect(escolher_online)

        modo_dialog.exec()

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
        """Redireciona para a tela de pré-jogo (futura implementação)."""
        modo = "Offline" if offline else "Online"
        QMessageBox.information(self, "Pré-Jogo",
                                f"Iniciando modo {modo}...\n(Tela de pré-jogo será implementada em breve.)")
        # Futuro: Trocar para widget de pré-jogo
        # Ex: self.setCentralWidget(TelaPreJogo(offline=offline, parent=self))

    def on_icone_sair(self):
        """Ação acionada pelo ícone de sair."""
        print("Ação: Ícone 'Sair' clicado. Fechando aplicação...")
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


# --- Ponto de Entrada da Aplicação ---
def main():
    print("🎮 Inicializando cliente gráfico com PyQt6...")
    app = QApplication(sys.argv)

    # Configurar o formato OpenGL padrão globalmente
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    # fmt.setDepthBufferSize(24)
    # fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    try:
        janela = JanelaPrincipal()
        # janela.show() # show() já é chamado dentro de __init__
        print("✅ Janela principal exibida em fullscreen.")
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ Erro ao criar/iniciar a janela: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Cria um arquivo session.txt de placeholder para testar o ícone "logado"
    # with open("session.txt", "w") as f:
    #     f.write("usuario_teste_logado")
    main()