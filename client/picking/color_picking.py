# client/picking/color_picking.py

from pyglm import glm
from OpenGL.GL import (
    # --- Framebuffer ---
    glGenFramebuffers, glBindFramebuffer, glDeleteFramebuffers,
    glCheckFramebufferStatus, GL_FRAMEBUFFER, GL_FRAMEBUFFER_COMPLETE,
    GL_COLOR_ATTACHMENT0, glFramebufferTexture2D,
    glFramebufferRenderbuffer,  # 👈 também precisa se você usa
    glBindRenderbuffer, glRenderbufferStorage,  # 👈 idem
    GL_RENDERBUFFER, GL_DEPTH_ATTACHMENT, GL_DEPTH_COMPONENT24,  # 👈 adicionados aqui

    # --- Textures ---
    glGenTextures, glBindTexture, glTexImage2D, glTexParameteri,
    GL_TEXTURE_2D, GL_RGB, GL_UNSIGNED_BYTE, GL_LINEAR, GL_CLAMP_TO_EDGE,
    GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,

    # --- Reading pixels ---
    glReadPixels, GL_READ_FRAMEBUFFER,

    # --- Clearing and drawing ---
    glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,

    # --- Rendering pipeline ---
    glUseProgram, glGetUniformLocation, glUniformMatrix4fv, glUniform3f,
    glBindVertexArray, glDrawArrays,

    # --- State control ---
    glDisable, GL_BLEND, glColorMask, glEnable, glGetError,

    # --- Cleanup ---
    glDeleteTextures,
)


class ColorPicking:
    """
    Sistema de detecção de objetos 3D via color picking.
    Usa um FBO off-screen onde cada objeto é renderizado com uma cor única.
    """

    def __init__(self):
        self.fbo = None
        self.texture = None
        self.width = 800
        self.height = 600
        self._inicializado = False
        self.picking_shader = None

    def _criar_shader_picking(self):
        """Compila um shader dedicado para color picking."""
        from client.rendering.shader import ShaderProgram
        import os

        print("🔧 [PICKING] Compilando shader de picking...")

        try:
            vert_path = "client/shaders/basic.vert"
            frag_path = "client/shaders/picking.frag"

            # ✅ Verificar existência dos arquivos
            if not os.path.exists(vert_path):
                raise FileNotFoundError(f"Vertex shader não encontrado: {vert_path}")
            if not os.path.exists(frag_path):
                raise FileNotFoundError(f"Fragment shader não encontrado: {frag_path}")

            # ✅ Ler conteúdo dos shaders
            with open(vert_path, "r", encoding='utf-8') as f:
                vertex_src = f.read()
            with open(frag_path, "r", encoding='utf-8') as f:
                fragment_src = f.read()

            # ✅ Verificar se os shaders não estão vazios
            if not vertex_src.strip():
                raise ValueError("Vertex shader está vazio")
            if not fragment_src.strip():
                raise ValueError("Fragment shader está vazio")

            print(f"📖 [PICKING] Shaders carregados: {len(vertex_src)} chars vert, {len(fragment_src)} chars frag")

            # ✅ Compilar shader
            self.picking_shader = ShaderProgram(vertex_src, fragment_src)

            if not self.picking_shader or not self.picking_shader.program_id:
                raise RuntimeError("Falha ao compilar shader de picking - programa inválido")

            # ✅ Verificar uniforms essenciais
            essential_uniforms = ["MVP", "picking_color"]
            missing_uniforms = []

            for uniform in essential_uniforms:
                loc = self.picking_shader.obter_localizacao_uniform(uniform)
                if loc == -1:
                    missing_uniforms.append(uniform)

            if missing_uniforms:
                raise RuntimeError(f"Uniforms essenciais não encontrados: {missing_uniforms}")

            print("✅ [PICKING] Shader de picking compilado com sucesso.")
            print(f"   → Program ID: {self.picking_shader.program_id}")
            print(f"   → Uniforms encontrados: MVP, picking_color")

            return True

        except FileNotFoundError as e:
            print(f"❌ [PICKING] Arquivo de shader não encontrado: {e}")
            self.picking_shader = None
            return False

        except ValueError as e:
            print(f"❌ [PICKING] Erro de conteúdo: {e}")
            self.picking_shader = None
            return False

        except RuntimeError as e:
            print(f"❌ [PICKING] Erro de compilação/linking: {e}")
            self.picking_shader = None
            return False

        except Exception as e:
            print(f"❌ [PICKING] Erro inesperado ao criar shader: {e}")
            import traceback
            traceback.print_exc()
            self.picking_shader = None
            return False

    def resize(self, width: int, height: int):
        """Atualiza tamanho do framebuffer se necessário."""
        if self.width == width and self.height == height:
            return
        print(f"🔄 [PICKING] Redimensionando FBO: {self.width}x{self.height} -> {width}x{height}")
        self.width = width
        self.height = height
        self._descartar_recursos()

    def _setup_fbo(self):
        """Cria FBO, textura de cor e renderbuffer de profundidade."""
        from OpenGL.GL import (
            glGenFramebuffers, glBindFramebuffer, glDeleteRenderbuffers,
            glGenTextures, glBindTexture, glTexImage2D, glTexParameteri,
            glFramebufferTexture2D, glCheckFramebufferStatus,
            GL_FRAMEBUFFER, GL_FRAMEBUFFER_COMPLETE, GL_COLOR_ATTACHMENT0,
            GL_TEXTURE_2D, GL_RGB, GL_UNSIGNED_BYTE, GL_LINEAR, GL_CLAMP_TO_EDGE,
            GL_RENDERBUFFER, glGenRenderbuffers, glBindRenderbuffer,
            glRenderbufferStorage, glFramebufferRenderbuffer
        )

        if self._inicializado:
            print("✅ [PICKING] FBO já inicializado")
            return True

        print("🔄 [PICKING] Inicializando FBO com depth buffer...")

        try:
            # --- 1. Gerar FBO ---
            self.fbo = glGenFramebuffers(1)
            self.texture = glGenTextures(1)
            self.depth_rb = glGenRenderbuffers(1)  # Novo: buffer de profundidade

            print(f"🆔 [PICKING] Recursos gerados → FBO: {self.fbo}, Texture: {self.texture}, Depth RB: {self.depth_rb}")

            if self.fbo == 0 or self.texture == 0 or self.depth_rb == 0:
                raise RuntimeError("Falha ao gerar recursos do FBO")

            # --- 2. Configurar textura de cor ---
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,  # Formato interno: RGB (sem alpha)
                self.width,
                self.height,
                0,
                GL_RGB,  # Formato dos dados
                GL_UNSIGNED_BYTE,  # Tipo
                None  # Dados iniciais: nenhum
            )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # --- 3. Anexar textura ao FBO ---
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
            glFramebufferTexture2D(
                GL_FRAMEBUFFER,
                GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D,
                self.texture,
                0
            )

            # --- 4. Criar e anexar renderbuffer de profundidade ---
            glBindRenderbuffer(GL_RENDERBUFFER, self.depth_rb)
            glRenderbufferStorage(
                GL_RENDERBUFFER,
                GL_DEPTH_COMPONENT24,  # 24 bits de precisão → ideal
                self.width,
                self.height
            )
            glFramebufferRenderbuffer(
                GL_FRAMEBUFFER,
                GL_DEPTH_ATTACHMENT,
                GL_RENDERBUFFER,
                self.depth_rb
            )

            # --- 5. Validar FBO completo ---
            status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
            if status != GL_FRAMEBUFFER_COMPLETE:
                error_msg = {
                    0: "GL_FRAMEBUFFER_UNDEFINED",
                    1280: "GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT",
                    1281: "GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT",
                    1282: "GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER",
                    1283: "GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER",
                    1285: "GL_FRAMEBUFFER_INCOMPLETE_FORMATS",
                    1286: "GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS"
                }.get(status, f"Erro desconhecido: {status:x}")
                raise RuntimeError(f"FBO de picking não está completo! {error_msg}")

            # --- 6. Limpar estado OpenGL ---
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glBindRenderbuffer(GL_RENDERBUFFER, 0)
            glBindTexture(GL_TEXTURE_2D, 0)

            self._inicializado = True
            print(f"✅ [PICKING] FBO criado com sucesso: {self.width}x{self.height} + depth buffer")
            return True

        except Exception as e:
            print(f"❌ [PICKING] Falha ao configurar FBO: {e}")
            self._cleanup()
            return False

    def _id_para_cor(self, idx: int):
        """Converte ID inteiro → RGB (máx 16777215)."""
        r = (idx >> 16) & 0xFF
        g = (idx >> 8) & 0xFF
        b = idx & 0xFF
        return r, g, b

    def _cor_para_id(self, r: int, g: int, b: int) -> int:
        """Converte RGB → ID inteiro."""
        return (r << 16) + (g << 8) + b

    def renderizar(self, widget):
        """
        Renderiza todos os tiles com cores únicas em um FBO,
        usando Z-buffer para garantir que apenas o tile mais visível seja detectado.
        """
        # === 1. Verificações iniciais ===
        if not widget.mundo or not widget.mundo.planeta:
            print("❌ [PICKING] Mundo não carregado para renderização")
            return

        if not hasattr(widget, 'vaos') or not widget.vaos:
            print("❌ [PICKING] VAOs não disponíveis")
            return

        if not self._setup_fbo():
            print("❌ [PICKING] Falha ao configurar FBO")
            return

        print("🎨 [PICKING] Iniciando renderização de picking...")

        # === 2. Compilar shader, se necessário ===
        if self.picking_shader is None and not self._criar_shader_picking():
            print("❌ [PICKING] Shader de picking falhou")
            return

        # === 3. Bind FBO e limpar buffers (COR + PROFUNDIDADE!) ===
        from OpenGL.GL import (
            glBindFramebuffer, glViewport, glClearColor, glClear,
            GL_FRAMEBUFFER, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
            glEnable, GL_DEPTH_TEST, glDepthFunc, GL_LESS,
            glDisable, GL_BLEND, GL_CULL_FACE
        )

        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # ✅ Limpa profundidade!

        # === 4. Configurar estado OpenGL ===
        self.picking_shader.usar()

        glDisable(GL_BLEND)  # Evita blend indesejado
        glDisable(GL_CULL_FACE)  # Garante que todos os lados sejam desenhados
        glEnable(GL_DEPTH_TEST)  # ✅ ATIVA TESTE DE PROFUNDIDADE
        glDepthFunc(GL_LESS)  # ✅ Menor valor de Z vence

        # === 5. Calcular e enviar MVP ===
        try:
            proj = widget.camera.get_projection_matrix()
            view = widget.camera.get_view_matrix()
            model = glm.mat4(1.0)
            mvp = proj * view * model

            loc_mvp = self.picking_shader.obter_localizacao_uniform("MVP")
            if loc_mvp != -1:
                self.picking_shader.set_uniform_mat4("MVP", glm.value_ptr(mvp))
            else:
                print("⚠️ [PICKING] Uniform 'MVP' não encontrado!")
        except Exception as e:
            print(f"❌ [PICKING] Erro ao calcular MVP: {e}")
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            self.picking_shader.limpar()
            return

        # === 6. Iterar e desenhar cada tile com cor única ===
        G = widget.mundo.planeta.geografia
        tiles_renderizados = 0

        for idx, coords in enumerate(G.nodes):
            if coords not in widget.vaos or coords not in widget.mundo.planeta.poligonos:
                continue

            try:
                # Gerar cor única (evitar preto puro)
                r, g, b = self._id_para_cor(idx + 1)
                self.picking_shader.set_uniform_vec3("picking_color", (r / 255.0, g / 255.0, b / 255.0))

                # Desenhar
                from OpenGL.GL import glBindVertexArray, glDrawArrays, GL_TRIANGLE_FAN
                glBindVertexArray(widget.vaos[coords])
                num_vertices = len(widget.mundo.planeta.poligonos[coords])
                glDrawArrays(GL_TRIANGLE_FAN, 0, num_vertices)

                tiles_renderizados += 1

            except Exception as e:
                print(f"⚠️ [PICKING] Falha ao renderizar tile {coords}: {e}")
                continue

        # === 7. Limpeza final ===
        from OpenGL.GL import glBindVertexArray
        glBindVertexArray(0)
        self.picking_shader.limpar()

        # Restaurar framebuffer padrão
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Restaurar viewport original
        if hasattr(widget, 'width') and hasattr(widget, 'height'):
            glViewport(0, 0, widget.width(), widget.height())

        print(f"✅ [PICKING] Renderização concluída: {tiles_renderizados}/{len(G.nodes)} tiles.")

    def detectar_tile(self, widget, x: int, y: int):
        """
        Executa todo pipeline de color picking.
        Retorna: coordenadas do tile clicado (q, r) ou None.
        """
        # ✅ Verificações iniciais
        if not widget.mundo or not widget.mundo.planeta:
            print("❌ [PICKING] Mundo não carregado")
            return None

        if not hasattr(widget, 'width') or not hasattr(widget, 'height'):
            print("❌ [PICKING] Widget não possui dimensões")
            return None

        # ✅ Atualizar tamanho do FBO primeiro
        self.resize(widget.width(), widget.height())

        # ✅ Garantir que o FBO está configurado ANTES de tentar usar
        if not self._setup_fbo():
            print("❌ [PICKING] Falha ao configurar FBO. Abortando.")
            return None

        # ✅ Verificar se o shader de picking está compilado
        if self.picking_shader is None:
            if not self._criar_shader_picking():
                print("❌ [PICKING] Shader de picking não disponível")
                return None

        # ✅ Renderizar cena de picking
        try:
            self.renderizar(widget)
        except Exception as e:
            print(f"❌ [PICKING] Erro durante renderização: {e}")
            return None

        # ✅ Forçar conclusão da renderização
        from OpenGL.GL import glFinish
        glFinish()

        # ✅ Converter coordenada Y para sistema OpenGL (origem inferior)
        viewport_y = self.height - int(y) - 1
        x = int(x)

        # ✅ Ler pixel do framebuffer de picking (CORRIGIDO)
        from OpenGL.GL import glBindFramebuffer, GL_READ_FRAMEBUFFER, glReadPixels, GL_RGB, GL_UNSIGNED_BYTE
        try:
            glBindFramebuffer(GL_READ_FRAMEBUFFER, self.fbo)

            # ✅ CORREÇÃO: Usar numpy array para leitura confiável
            import numpy as np
            pixel_data = np.zeros((1, 1, 3), dtype=np.uint8)
            glReadPixels(x, viewport_y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, pixel_data)

            glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)

            # ✅ Extrair valores RGB do numpy array
            r, g, b = pixel_data[0, 0]

        except Exception as e:
            print(f"❌ [PICKING] Erro ao ler pixel: {e}")
            return None

        # ✅ Fundo (preto) = sem seleção
        if r == 0 and g == 0 and b == 0:
            print("⚫ [PICKING] Pixel preto detectado (fundo)")
            return None

        # ✅ Converter cor → ID → coordenadas
        idx = self._cor_para_id(r, g, b) - 1  # -1 por causa do +1 no _id_para_cor
        nodes_list = list(widget.mundo.planeta.geografia.nodes)

        if 0 <= idx < len(nodes_list):
            coords = nodes_list[idx]
            print(f"🎯 [PICKING] Tile detectado: {coords} (RGB={r},{g},{b}, ID={idx + 1})")
            return coords
        else:
            print(f"⚠️ [PICKING] Índice fora do intervalo: {idx} (tamanho={len(nodes_list)}, RGB={r},{g},{b})")
            # Debug: listar alguns nodes para verificar a ordem
            if len(nodes_list) > 0:
                print(f"   → Primeiros nodes: {nodes_list[:5]}")
                print(f"   → Últimos nodes: {nodes_list[-5:]}")
            return None

    def _descartar_recursos(self):
        """Libera FBO/textura se existirem."""
        self._cleanup()

    def _cleanup(self):
        """Libera recursos da GPU."""
        from OpenGL.GL import glDeleteFramebuffers, glDeleteTextures
        if self.fbo:
            glDeleteFramebuffers(1, [self.fbo])
            self.fbo = None
        if self.texture:
            glDeleteTextures(1, [self.texture])
            self.texture = None
        self._inicializado = False

    def __del__(self):
        self._cleanup()