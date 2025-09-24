# client/rendering/opengl_widget.py
import OpenGL.GL as gl
import ctypes
import numpy as np
from pyglm import glm
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeyEvent
from client.rendering.camera import Camera
from client.picking.color_picking import ColorPicking
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from client.main import JanelaPrincipal


class OpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.parent_widget: Optional['JanelaPrincipal'] = None

        # --- Estado de Renderização ---
        self.modulo_jogo = False  # Ativa renderização do planeta
        self.mundo = None  # Referência ao mundo atual
        self._geometria_necessaria = False  # Flag: geometria precisa ser criada em paintGL
        self.modo_renderizacao = "fisico"  # Modo de visualização ('fisico' ou 'politico')

        # --- Recursos OpenGL ---
        self.shader_program = None  # Programa de shader ativo
        self.VAO = None  # VAO temporário (triângulo de teste)
        self.VBO = None  # VBO temporário (triângulo de teste)

        # --- Geometria do Planeta ---
        self.vaos = {}  # {coord: vao} – um VAO por polígono
        self.vbos = {}  # {coord: vbo} – um VBO por polígono

        # --- Câmera 3D ---
        self.camera = Camera()  # Câmera orbital (posição, rotação, zoom)

        # --- Entrada do Usuário ---
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Aceita foco para teclado/mouse
        self.setMouseTracking(True)  # Permite detectar movimento sem clicar
        self.last_mouse_pos = None  # Para calcular delta do mouse

        # Teclas pressionadas (para movimento contínuo)
        self.keys_pressed = set()

        # Timer para processamento contínuo das teclas
        self.timer_keyboard = QTimer(self)
        self.timer_keyboard.timeout.connect(self._atualizar_camera_por_tecla)
        self.timer_keyboard.start(16)  # ~60 FPS

        # --- Sistema de Interação 3D ---
        self.color_picking = ColorPicking()  # Sistema de seleção via color picking

    def mousePressEvent(self, event):
        from PyQt6.QtCore import Qt

        pos = event.position()
        x, y = pos.x(), pos.y()
        self.last_mouse_pos = (x, y)

        # --- Ative para depurar ---
        DEBUG = False  # 🔁 Mude para True durante testes

        parent_widget = getattr(self, 'parent_widget', None)
        if not parent_widget:
            if DEBUG:
                print("❌ [DEBUG] parent_widget não encontrado!")
            super().mousePressEvent(event)
            return
        if DEBUG:
            print("✅ [DEBUG] parent_widget encontrado.")

        # === Picking: detectar tile clicado ===
        try:
            self.makeCurrent()
            coords = self.color_picking.detectar_tile(self, x, y)
            if DEBUG and coords:
                print(f"🎯 [DEBUG] Tile detectado: {coords}")
        except Exception as e:
            if DEBUG:
                print(f"❌ [DEBUG] Erro no picking: {e}")
            coords = None
        finally:
            self.doneCurrent()

        # === Distribuir por botão ===
        if event.button() == Qt.MouseButton.LeftButton:
            if DEBUG:
                print("🟢 [DEBUG] Botão ESQUERDO pressionado.")
            if coords:
                self.on_left_click(coords)
            else:
                # Clique fora do mapa: fecha overlay
                container = getattr(parent_widget, 'opengl_container', parent_widget)
                if hasattr(container, 'tile_overlay'):
                    container.tile_overlay.hide()
                    if DEBUG:
                        print("CloseOperation: Fechando overlay por clique fora.")

        elif event.button() == Qt.MouseButton.RightButton:
            if DEBUG:
                print("🔵 [DEBUG] Botão DIREITO pressionado.")
            if coords:
                self.on_right_click(coords)
            else:
                if DEBUG:
                    print("🟥 [DEBUG] Nenhum tile detectado com botão direito.")

        # Propagar evento para suportar arraste
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return  # ignore repeats
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def _atualizar_camera_por_tecla(self):
        """Aplica rotação com base nas teclas pressionadas."""
        sensibilidade = 0.03  # Rad/tecla

        dtheta = 0.0
        dphi = 0.0
        dzoom = 0.0

        if Qt.Key.Key_Left in self.keys_pressed:
            dtheta += sensibilidade
        if Qt.Key.Key_Right in self.keys_pressed:
            dtheta -= sensibilidade
        if Qt.Key.Key_Up in self.keys_pressed:
            dphi -= sensibilidade
        if Qt.Key.Key_Down in self.keys_pressed:
            dphi += sensibilidade

        # Zoom opcional com Page Up / Page Down
        if Qt.Key.Key_PageUp in self.keys_pressed:
            dzoom -= 0.5
        if Qt.Key.Key_PageDown in self.keys_pressed:
            dzoom += 0.5

        if dtheta != 0 or dphi != 0 or dzoom != 0:
            self.camera.orbit(dtheta, dphi, dzoom)
            self.update()  # ✅ Força redraw quando houver mudança

    def on_left_click(self, coords):
        """Mostra a textura do bioma ao clicar com botão esquerdo."""
        if not self.mundo or not self.mundo.planeta:
            return

        node_data = self.mundo.planeta.geografia.nodes.get(coords, {})
        if not node_data:
            return

        bioma = node_data.get("bioma", "Unknown").lower().strip()
        formato = node_data.get("formato", "hex_up")  # <-- NOVO! Pega direto do nó

        caminho_imagem = f"assets/solid_colors/biomes/{bioma}_{formato}.png"

        import os
        if not os.path.exists(caminho_imagem):
            caminho_imagem = "assets/textures/biomes/fallback.png"
            if not os.path.exists(caminho_imagem):
                return

        container = getattr(self.parent(), 'opengl_container', self.parent())
        if not hasattr(container, 'tile_overlay'):
            from client.widgets.tile import TileOverlay
            container.tile_overlay = TileOverlay(self.mundo, parent=container)

            def fechar():
                container.tile_overlay.hide()

            container.tile_overlay.btn_close.clicked.connect(fechar)
            container.tile_overlay.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)

        overlay = container.tile_overlay
        overlay.carregar_imagem(caminho_imagem, formato=formato)  # <-- Passe formato!
        overlay.set_reference_widget(self)
        overlay.show_centered()

    def on_right_click(self, coords):
        """Lida com clique direito: navegação (centralização)."""
        self.centralizar_em(coords)

    def mudar_modo_mapa(self, modo: str):
        if modo in ["fisico", "politico"]:
            self.modo_renderizacao = modo
            self.update()
            print(f"✅ [DEBUG] Modo alterado para '{modo}' e update() chamado")
        else:
            print(f"❌ [DEBUG] Modo inválido: {modo}")

    def definir_modo_renderizacao(self, modo: str):
        """Muda o modo de renderização: 'fisico' ou 'politico'"""
        if modo not in ["fisico", "politico"]:
            return
        self.modo_renderizacao = modo
        self.update()  # força redesenhar

    def wheelEvent(self, event):
        # Normaliza o delta do scroll (~±120 por "click")
        dzoom = -event.angleDelta().y() / 120 * 0.5
        self.camera.orbit(0, 0, dzoom)
        self.update()

    def initializeGL(self):
        """Configuração inicial do contexto OpenGL.
        - Define estado padrão do pipeline
        - Compila shaders
        - Configura geometria inicial (temporária ou do planeta)
        """
        # === 1. Estado inicial do OpenGL ===
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        gl.glEnable(gl.GL_DEPTH_TEST)  # Teste de profundidade
        gl.glDepthFunc(gl.GL_LESS)  # Z-test padrão
        gl.glEnable(gl.GL_BLEND)  # Blend para transparência
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        #gl.glEnable(gl.GL_CULL_FACE)  # Otimização: cull back-face
        #gl.glCullFace(gl.GL_BACK)

        print("🎮 Inicializando OpenGL...")

        # === 2. Compilar Shader Program ===
        try:
            with open("client/shaders/basic.vert", "r") as f:
                vertex_source = f.read()
            with open("client/shaders/basic.frag", "r") as f:
                fragment_source = f.read()

            from client.rendering.shader import ShaderProgram
            self.shader_program = ShaderProgram(vertex_source, fragment_source)

            if not self.shader_program.program_id:
                raise RuntimeError("Falha ao criar o programa de shader")

        except Exception as e:
            print(f"❌ Erro ao compilar shaders: {e}")
            self.shader_program = None
            return

        # === 3. Configurar Geometria Inicial ===
        try:
            # Se já temos um mundo carregado (ex: durante hot-reload), renderizamos ele
            if hasattr(self, 'mundo') and self.mundo:
                self._criar_geometria_planeta()
            else:
                # Caso contrário, usamos um triângulo temporário para teste
                self._criar_geometria_triangulo()

            print("✅ OpenGL inicializado com sucesso: shaders e geometria prontos.")
        except Exception as e:
            print(f"❌ Erro ao configurar geometria: {e}")
            self.shader_program = None
            self.VAO = None
            self.VBO = None

    def _criar_geometria_triangulo(self):
        vertices = np.array([
            -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
             0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0,
        ], dtype=np.float32)

        self.VAO = gl.glGenVertexArrays(1)
        self.VBO = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.VAO)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.VBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        stride = 6 * 4  # 3 pos + 3 cor
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, None)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(3 * 4))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def resizeGL(self, w: int, h: int):
        """Atualiza viewport e aspecto da câmera."""
        if h > 0:
            self.camera.set_aspect(w / h)
        gl.glViewport(0, 0, w, h)

        # Sincronizar com o sistema de picking
        self.color_picking.resize(w, h)

    def paintGL(self):
        """Renderiza o frame atual.
        - Modo jogo: renderiza o planeta com MVP e câmera orbital
            → Escolhe entre modo físico ou político com base em self.modo_renderizacao
        - Modo espera: apenas limpa o fundo (overlay está por cima)
        """
        # === 1. DEFINIR COR DE FUNDO ANTES DE QUALQUER COISA ===
        if self.modulo_jogo and self.mundo:
            # Durante a partida: fundo preto
            gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        else:
            # Tela de espera / sem mundo: fundo cinza escuro
            gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        # === 2. LIMPAR BUFFERS (com a cor já definida) ===
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # === 3. MODO JOGO: Renderizar o planeta ===
        if self.modulo_jogo and self.mundo and self.shader_program and self.shader_program.program_id:
            try:
                print(f"🔧 [DEBUG] paintGL: Iniciando renderização. Modo='{self.modo_renderizacao}'")

                # --- Atualizar câmera ---
                if self.width() > 0 and self.height() > 0:
                    self.camera.set_aspect(self.width() / self.height())
                else:
                    print("⚠️ [DEBUG] Tamanho inválido para atualizar câmera")
                    return

                # --- Calcular MVP ---
                view = self.camera.get_view_matrix()
                proj = self.camera.get_projection_matrix()
                model = glm.mat4(1.0)
                mvp = proj * view * model

                # --- Ativar shader e enviar uniforms ---
                self.shader_program.usar()
                self.shader_program.set_uniform_mat4("MVP", glm.value_ptr(mvp))

                # --- Criar geometria, se necessário ---
                if self._geometria_necessaria:
                    print("🔧 [DEBUG] Criando geometria do planeta...")
                    self._criar_geometria_planeta()
                    self._geometria_necessaria = False
                    print(f"✅ Geometria criada: {len(self.vaos)} polígonos")

                # --- 🔁 ROTEAMENTO DE RENDERIZAÇÃO ---
                if self.modo_renderizacao == "fisico":
                    # Desativar modo político no shader
                    if hasattr(self.shader_program, 'set_uniform_bool'):
                        self.shader_program.set_uniform_bool("modo_politico", False)
                    self._renderizar_planeta_fisico()

                elif self.modo_renderizacao == "politico":
                    # Ativar modo político no shader
                    if hasattr(self.shader_program, 'set_uniform_bool'):
                        self.shader_program.set_uniform_bool("modo_politico", True)
                    else:
                        print("❌ [DEBUG] set_uniform_bool não disponível no shader_program")
                    self._renderizar_planeta_politico()

                else:
                    print(f"⚠️ [DEBUG] Modo desconhecido: '{self.modo_renderizacao}'. Usando 'fisico' como fallback.")
                    if hasattr(self.shader_program, 'set_uniform_bool'):
                        self.shader_program.set_uniform_bool("modo_politico", False)
                    self._renderizar_planeta_fisico()

                # --- Limpeza final ---
                self.shader_program.limpar()

            except Exception as e:
                print(f"❌ Erro crítico em paintGL: {e}")
                import traceback
                traceback.print_exc()
                # Em caso de erro, usa fundo vermelho de alerta
                gl.glClearColor(0.2, 0.0, 0.0, 1.0)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # === 4. NÃO FAZER NADA NO ELSE ===
        # Já fizemos glClear com a cor certa acima, então não precisa repetir

    def _renderizar_planeta_fisico(self):
        """Renderiza o planeta no modo físico, usando cores por vértice (biomas, altitude, etc)."""
        print("🎨 [DEBUG] Iniciando renderização FÍSICA do planeta")

        # === 1. Atualizar câmera ===
        if self.width() > 0 and self.height() > 0:
            self.camera.set_aspect(self.width() / self.height())
            print(f"🔧 [DEBUG] Aspecto da câmera atualizado: {self.width()}x{self.height()} → {self.camera.aspect:.3f}")
        else:
            print("⚠️ [DEBUG] Tamanho inválido para atualizar câmera")
            return

        # === 2. Calcular MVP ===
        try:
            view = self.camera.get_view_matrix()
            proj = self.camera.get_projection_matrix()
            model = glm.mat4(1.0)
            mvp = proj * view * model
            print(f"📐 [DEBUG] MVP calculado. Posição da câmera: ({view[3][0]:.2f}, {view[3][1]:.2f}, {view[3][2]:.2f})")
        except Exception as e:
            print(f"❌ [DEBUG] Falha ao calcular MVP: {e}")
            return

        # === 3. Ativar shader e configurar para modo físico ===
        try:
            self.shader_program.usar()
            self.shader_program.set_uniform_mat4("MVP", glm.value_ptr(mvp))
            self.shader_program.set_uniform_bool("modo_politico", False)  # 🔵 Modo físico ativo
            print("✅ [DEBUG] Shader ativado, MVP enviado, modo físico definido")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao usar shader ou enviar uniform: {e}")
            return

        # === 4. Validar geometria ===
        if not self.vaos:
            print("❌ [DEBUG] self.vaos está vazio! Nenhum VAO para desenhar.")
            return

        print(f"📊 [DEBUG] Renderizando {len(self.vaos)} polígonos no modo físico...")

        # === 5. Iterar e desenhar cada polígono ===
        for i, (coords, vao) in enumerate(self.vaos.items()):
            try:
                # Log detalhado apenas para os primeiros polígonos
                if i < 5:
                    num_vertices = len(self.mundo.planeta.poligonos[coords])
                    print(f"   → Polígono {coords}: VAO={vao}, vértices={num_vertices}")
                elif i == 5:
                    print("   → (mais polígonos...)")

                gl.glBindVertexArray(vao)
                num_vertices = len(self.mundo.planeta.poligonos[coords])
                gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, num_vertices)

            except Exception as e:
                print(f"❌ [DEBUG] Erro ao renderizar polígono {coords}: {e}")
                continue  # Tenta o próximo

        # === 6. Limpeza final ===
        gl.glBindVertexArray(0)
        self.shader_program.limpar()
        print("✅ [DEBUG] Renderização FÍSICA concluída com sucesso")

    def _renderizar_planeta_politico(self):
        print("🎨 [DEBUG] Iniciando renderização POLÍTICA do planeta (modo placeholder)")
        if not self.mundo or not self.mundo.planeta or not self.shader_program:
            print("❌ [DEBUG] Dados insuficientes para renderização política")
            return

        # Atualizar câmera
        if self.width() > 0 and self.height() > 0:
            self.camera.set_aspect(self.width() / self.height())

        G = self.mundo.planeta.geografia
        desenhadas = set()

        # === 1. Renderizar oceanos, mares e costas ===
        print("🌊 [DEBUG] Renderizando oceanos, mares e costas...")
        for coords, dados in G.nodes(data=True):
            bioma = dados.get("bioma")
            if bioma in ["Ocean", "Sea", "Coast"] and coords in self.vaos:
                try:
                    self.shader_program.set_uniform_vec3("cor_uniforme", (0.2, 0.2, 0.3))  # Azul escuro acinzentado
                    gl.glBindVertexArray(self.vaos[coords])
                    num_vertices = len(self.mundo.planeta.poligonos[coords])
                    gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, num_vertices)
                    desenhadas.add(coords)
                except Exception as e:
                    print(f"❌ [DEBUG] Erro ao renderizar oceano {coords}: {e}")

        # === 2. Renderizar terra NEUTRA (sem dono) ===
        print("🟨 [DEBUG] Renderizando terra neutra...")
        cor_neutra = (0.6, 0.6, 0.6)
        self.shader_program.set_uniform_vec3("cor_uniforme", cor_neutra)
        for coords in G.nodes:
            if coords in desenhadas or coords not in self.vaos:
                continue
            try:
                node_data = G.nodes[coords]
                bioma = node_data.get("bioma")
                if bioma not in ["Ocean", "Sea", "Coast"]:
                    gl.glBindVertexArray(self.vaos[coords])
                    num_vertices = len(self.mundo.planeta.poligonos[coords])
                    gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, num_vertices)
                    desenhadas.add(coords)
            except Exception as e:
                print(f"❌ [DEBUG] Erro ao renderizar terra neutra {coords}: {e}")

        # === 3. CIVILIZAÇÕES: PLACEHOLDER (sem cor por tile) ===
        print("🟡 [DEBUG] Renderização política: CIVILIZAÇÕES em modo placeholder (sem cor por tile)")
        # Futuro: desenhar bandeiras ou marcadores nos assentamentos
        # Por enquanto: nada aqui

        # === 4. Limpeza final ===
        gl.glBindVertexArray(0)
        self.shader_program.limpar()
        print("✅ [DEBUG] Renderização POLÍTICA concluída (placeholder ativo)")

    def _criar_geometria_planeta(self):
        """Gera VAOs/VBOs para todos os polígonos do planeta."""
        self.vaos.clear()
        self.vbos.clear()

        print("🔧 [DEBUG] Iniciando _criar_geometria_planeta")
        if not self.mundo or not self.mundo.planeta:
            print("❌ [DEBUG] Erro: self.mundo ou self.mundo.planeta é None")
            return

        planeta = self.mundo.planeta
        print(f"🔧 [DEBUG] Criando geometria para {len(planeta.poligonos)} polígonos")

        for coords, vertices_3d in planeta.poligonos.items():
            node_data = planeta.geografia.nodes[coords]
            cor_bioma = [c / 255.0 for c in node_data.get('cor_bioma', [128, 128, 128])]

            # Converter vértices para array NumPy
            vertex_data = []
            for v in vertices_3d:
                vertex_data.extend(v)  # v é [x, y, z]
                vertex_data.extend(cor_bioma)

            vertex_array = np.array(vertex_data, dtype=np.float32)

            # Gerar VAO e VBO
            vao = gl.glGenVertexArrays(1)
            vbo = gl.glGenBuffers(1)

            # ✅ Bind completo: VAO → VBO → atributos → desvincular
            gl.glBindVertexArray(vao)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
            gl.glBufferData(
                gl.GL_ARRAY_BUFFER,
                vertex_array.nbytes,
                vertex_array,
                gl.GL_STATIC_DRAW
            )

            stride = 6 * 4  # pos(3) + cor(3) = 6 floats

            # Layout: posição (0), cor (1)
            gl.glEnableVertexAttribArray(0)
            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, None)

            gl.glEnableVertexAttribArray(1)
            gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(3 * 4))

            # ✅ Desvincular VBO antes do VAO
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glBindVertexArray(0)

            self.vaos[coords] = vao
            self.vbos[coords] = vbo

        print(f"✅ Geometria do planeta criada: {len(self.vaos)} polígonos")

    def carregar_mundo(self, mundo):
        """
        Carrega um novo mundo e prepara o OpenGL para renderizá-lo.
        Reseta estado visual e força recriação da geometria.
        """
        self.mundo = mundo
        self.modulo_jogo = True
        self.vaos.clear()
        self.vbos.clear()
        self._geometria_necessaria = True

        # ✅ Resetar câmera com base no fator do novo mundo
        self.camera.resetar(mundo.planeta.fator)

        # ✅ Sincronizar modo de renderização com o mundo
        self.modo_renderizacao = mundo.modo_renderizacao

        # ✅ Forçar redraw
        self.update()

        print(f"🌍 Mundo carregado. Modo: {self.modo_renderizacao}, Geometria será criada em paintGL.")

    def ativar_modo_jogo(self):
        self.modulo_jogo = True
        self.update()

    def limpar_mundo(self):
        """Limpa o mundo atual, remove geometria OpenGL e para de renderizar o planeta."""
        self.mundo = None
        self.modulo_jogo = False  # Desativa modo jogo
        self.vaos.clear()
        self.vbos.clear()
        self._geometria_necessaria = True  # Força recriação futura, se necessário
        self.update()  # Atualiza a tela (chama paintGL)
        print("🧹 Mundo limpo: geometria OpenGL removida e modo jogo desativado.")

    def centralizar_em(self, coords):
        """
        Reposiciona a câmera para olhar diretamente para um hexágono.
        - Mantém o centro orbital em (0,0,0)
        - Usa a mesma distância definida em `resetar()`
        - Ajusta theta e phi para focar no tile
        """
        if not hasattr(self, 'mundo') or not self.mundo:
            print(f"❌ [centralizar_em] Mundo não carregado. Não é possível centralizar em {coords}")
            return

        planeta = self.mundo.planeta

        if coords not in planeta.poligonos:
            print(f"❌ [centralizar_em] Coordenada {coords} não encontrada em poligonos.")
            return

        vertices = planeta.poligonos[coords]
        if len(vertices) == 0:
            print(f"❌ [centralizar_em] Polígono {coords} sem vértices.")
            return

        # === 1. Calcular centro 3D do hexágono ===
        centro = [sum(v[i] for v in vertices) / len(vertices) for i in range(3)]
        cx, cy, cz = float(centro[0]), float(centro[1]), float(centro[2])

        # Normalizar para direção unitária
        norm = (cx ** 2 + cy ** 2 + cz ** 2) ** 0.5
        if norm == 0:
            print("❌ [centralizar_em] Norma zero, impossível calcular direção.")
            return

        dx, dy, dz = cx / norm, cy / norm, cz / norm

        # === 2. Calcular theta e phi ===
        import math
        theta = math.atan2(dz, dx)  # Rotação horizontal
        phi = math.acos(dy)  # Rotação vertical

        # === 3. Calcular distância igual à do `resetar()` ===
        fator = self.mundo.planeta.fator
        raio_planeta = fator / (2 * math.sin(math.pi / 5))  # mesma fórmula de resetar()
        distance = 4.0 * raio_planeta  # mesma distância

        # === 4. Aplicar na câmera ===
        camera = self.camera
        camera.center = glm.vec3(0.0, 0.0, 0.0)  # orbita ainda é no centro do planeta
        distance = self.camera.distance
        camera.theta = theta
        camera.phi = phi
        camera.update_position()
        self.update()

        print(f"📍 Câmera reposicionada para olhar {coords}")
        print(f"   → distância={distance:.2f}, theta={math.degrees(theta):.1f}°, phi={math.degrees(phi):.1f}°")

    def __del__(self):
        if hasattr(self, 'timer_keyboard'):
            self.timer_keyboard.stop()