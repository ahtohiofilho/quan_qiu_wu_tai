# client/rendering/shader.py
import OpenGL.GL as gl
from typing import Dict, Optional
import ctypes


class ShaderProgram:
    """
    Wrapper para programas de shader OpenGL.
    Compila vertex/fragment shaders e gerencia o programa linkado.
    """

    def __init__(self, vertex_source: str, fragment_source: str):
        self.program_id = None
        self.vertex_source = vertex_source
        self.fragment_source = fragment_source
        self._uniform_locations: Dict[str, int] = {}
        self._compile_and_link()

    def _compile_shader(self, source: str, shader_type) -> int:
        shader = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)

        success = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
        if not success:
            log = gl.glGetShaderInfoLog(shader).decode('utf-8')
            raise RuntimeError(f"Erro ao compilar shader ({shader_type}):\n{log}")

        return shader

    def _compile_and_link(self):
        """Compila e linka os shaders."""
        try:
            vertex_shader = self._compile_shader(self.vertex_source, gl.GL_VERTEX_SHADER)
            fragment_shader = self._compile_shader(self.fragment_source, gl.GL_FRAGMENT_SHADER)

            self.program_id = gl.glCreateProgram()
            gl.glAttachShader(self.program_id, vertex_shader)
            gl.glAttachShader(self.program_id, fragment_shader)
            gl.glLinkProgram(self.program_id)

            # Verifica link
            success = gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS)
            if not success:
                log = gl.glGetProgramInfoLog(self.program_id).decode('utf-8')
                raise RuntimeError(f"Erro ao linkar shader program:\n{log}")

            # Limpa shaders intermediários
            gl.glDeleteShader(vertex_shader)
            gl.glDeleteShader(fragment_shader)

            print("✅ Shader program criado com sucesso.")

        except Exception as e:
            print(f"❌ Falha ao criar shader program: {e}")
            self.program_id = None
            if vertex_shader:
                gl.glDeleteShader(vertex_shader)
            if fragment_shader:
                gl.glDeleteShader(fragment_shader)

    def usar(self):
        """Ativa o programa de shader."""
        if self.program_id:
            gl.glUseProgram(self.program_id)
        else:
            raise RuntimeError("Tentando usar shader inválido.")

    def obter_localizacao_uniform(self, nome: str) -> int:
        """Cache da localização de uniforms."""
        if nome not in self._uniform_locations:
            loc = gl.glGetUniformLocation(self.program_id, nome)
            if loc == -1:
                print(f"⚠️ Uniform '{nome}' não encontrado no shader.")
            self._uniform_locations[nome] = loc
        return self._uniform_locations[nome]

    def set_uniform_mat4(self, nome: str, mat4):
        """Envia uma matriz 4x4 para o shader."""
        loc = self.obter_localizacao_uniform(nome)
        if loc != -1:
            gl.glUniformMatrix4fv(loc, 1, False, mat4)

    def set_uniform_int(self, nome: str, valor: int):
        """Envia um inteiro para o shader."""
        loc = self.obter_localizacao_uniform(nome)
        if loc != -1:
            gl.glUniform1i(loc, valor)

    def limpar(self):
        """Desativa o programa."""
        gl.glUseProgram(0)

    def deletar(self):
        """Libera o recurso de GPU."""
        if self.program_id:
            gl.glDeleteProgram(self.program_id)
            self.program_id = None