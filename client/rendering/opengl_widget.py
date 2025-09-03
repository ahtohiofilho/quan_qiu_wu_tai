# client/rendering/opengl_widget.py
import OpenGL.GL as gl
import ctypes
import numpy as np
from pyglm import glm
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from client.rendering.camera import Camera


class MeuOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        # --- Estado de Renderização ---
        self.modulo_jogo = False  # Ativa renderização do planeta
        self.mundo = None  # Referência ao mundo atual
        self._geometria_necessaria = False  # Flag: geometria precisa ser criada em paintGL
        self.modo_renderizacao = "fisico"  # Modo de visualização do mapa ('fisico' ou 'politico')

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
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Para eventos de teclado/mouse

        # --- Debug e Estado Interno ---
        # Pronto para expansão (ex: modo de depuração, FPS, etc)

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

    def paintGL(self):
        """Renderiza o frame atual.
        - Modo jogo: renderiza o planeta com MVP e câmera orbital
            → Escolhe entre modo físico ou político com base em self.modo_renderizacao
        - Modo espera: apenas limpa o fundo (overlay está por cima)
        """
        # === 1. Limpar buffers ===
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # === 2. Modo Jogo: Renderizar o planeta ===
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
                view = self.camera.view_matrix()
                proj = self.camera.projection_matrix()
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
                # Fundo vermelho para indicar falha
                gl.glClearColor(0.2, 0.0, 0.0, 1.0)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # === 3. Modo Espera ou Estado Inválido ===
        else:
            # Apenas limpa com fundo escuro — o overlay está por cima
            gl.glClearColor(0.1, 0.1, 0.1, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

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
            view = self.camera.view_matrix()
            proj = self.camera.projection_matrix()
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
        """Renderiza o planeta no modo político:
        - Oceano, mar, costa → cinza escuro
        - Territórios de civilizações → cor da civilização (RGB convertido)
        - Terra sem dono → cinza claro
        """
        print("🎨 [DEBUG] Iniciando renderização POLÍTICA do planeta")

        # === 1. Validar estado ===
        if not self.mundo or not self.mundo.planeta or not self.shader_program:
            print("❌ [DEBUG] _renderizar_planeta_politico: Dados insuficientes (mundo, planeta ou shader)")
            return

        # === 2. Atualizar câmera ===
        if self.width() > 0 and self.height() > 0:
            self.camera.set_aspect(self.width() / self.height())
            print(f"🔧 [DEBUG] Aspecto da câmera atualizado: {self.width()}x{self.height()} → {self.camera.aspect:.3f}")
        else:
            print("⚠️ [DEBUG] Tamanho inválido para atualizar câmera")
            return

        # === 3. Calcular MVP ===
        try:
            view = self.camera.view_matrix()
            proj = self.camera.projection_matrix()
            model = glm.mat4(1.0)
            mvp = proj * view * model
            print(f"📐 [DEBUG] MVP calculado. Posição da câmera: ({view[3][0]:.2f}, {view[3][1]:.2f}, {view[3][2]:.2f})")
        except Exception as e:
            print(f"❌ [DEBUG] Falha ao calcular MVP: {e}")
            return

        # === 4. Ativar shader e configurar para modo político ===
        try:
            self.shader_program.usar()
            self.shader_program.set_uniform_mat4("MVP", glm.value_ptr(mvp))  # compatível com shader
            self.shader_program.set_uniform_bool("modo_politico", True)  # 🔵 Ativa modo uniforme
            print("✅ [DEBUG] Shader ativado, MVP enviado, modo político ativo")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao usar shader ou enviar uniform: {e}")
            return

        # === 5. Referências ===
        G = self.mundo.planeta.geografia
        desenhadas = set()  # Polígonos já renderizados

        # === 6. Desenhar OCEANOS (prioridade alta) ===
        cor_oceano = (0.2, 0.2, 0.2)
        self.shader_program.set_uniform_vec3("cor_uniforme", cor_oceano)
        print("🌊 [DEBUG] Renderizando oceanos, mares e costas...")

        for coords, dados in G.nodes(data=True):
            bioma = dados.get("bioma")
            if bioma in ["Ocean", "Sea", "Coast"] and coords in self.vaos:
                try:
                    gl.glBindVertexArray(self.vaos[coords])
                    num_vertices = len(self.mundo.planeta.poligonos[coords])
                    gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, num_vertices)
                    desenhadas.add(coords)
                except Exception as e:
                    print(f"❌ [DEBUG] Erro ao renderizar oceano {coords}: {e}")

        # === 7. Desenhar CIVILIZAÇÕES (tem prioridade sobre terra neutra) ===
        print(f"🏛️ [DEBUG] Renderizando territórios de {len(self.mundo.civs)} civilizações...")
        for civ in self.mundo.civs:
            try:
                # Converter cor de (0-255) para (0.0-1.0)
                r, g, b = civ.cor
                cor_civ = (r / 255.0, g / 255.0, b / 255.0)
                self.shader_program.set_uniform_vec3("cor_uniforme", cor_civ)

                print(f"   → Renderizando {len(civ.provincias)} províncias de {civ.nome} com cor {cor_civ}")

                for provincia in civ.provincias:
                    coords = provincia.coordenadas
                    if coords in self.vaos and coords not in desenhadas:
                        try:
                            gl.glBindVertexArray(self.vaos[coords])
                            num_vertices = len(self.mundo.planeta.poligonos[coords])
                            gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, num_vertices)
                            desenhadas.add(coords)
                        except Exception as e:
                            print(f"❌ [DEBUG] Erro ao renderizar província {coords} de {civ.nome}: {e}")
            except Exception as e:
                print(f"❌ [DEBUG] Erro ao processar civilização {civ.nome}: {e}")

        # === 8. Desenhar TERRA NEUTRA (apenas o que sobrou) ===
        cor_neutra = (0.6, 0.6, 0.6)
        self.shader_program.set_uniform_vec3("cor_uniforme", cor_neutra)
        print("🟨 [DEBUG] Renderizando terra neutra...")

        for coords in G.nodes:
            if coords in desenhadas or coords not in self.vaos:
                continue
            try:
                node_data = G.nodes[coords]
                bioma = node_data.get("bioma")
                if bioma not in ["Ocean", "Sea", "Coast"]:  # Apenas terra
                    gl.glBindVertexArray(self.vaos[coords])
                    num_vertices = len(self.mundo.planeta.poligonos[coords])
                    gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, num_vertices)
                    desenhadas.add(coords)
            except Exception as e:
                print(f"❌ [DEBUG] Erro ao renderizar terra neutra {coords}: {e}")

        # === 9. Limpeza final ===
        gl.glBindVertexArray(0)
        self.shader_program.limpar()
        print("✅ [DEBUG] Renderização POLÍTICA concluída com sucesso")

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
        self.mundo = mundo
        self.modulo_jogo = True
        self.vaos.clear()
        self.vbos.clear()
        self._geometria_necessaria = True
        self.camera.resetar(mundo.planeta.fator)
        self.update()
        print(f"🌍 Mundo carregado. Geometria será criada em paintGL.")

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