# client/rendering/camera.py
from pyglm import glm

class Camera:
    """
    Câmera orbital 3D para visualização de planetas.
    Permite rotação (orbit), zoom e atualização da matriz de view/projection.
    """

    def __init__(self):
        # Posição inicial: olhando para a origem
        self.center = glm.vec3(0.0, 0.0, 0.0)  # Ponto central (planeta)
        self.distance = 5.0                   # Distância do centro
        self.theta = 0.0                      # Rotação horizontal (Y)
        self.phi = glm.radians(10.0)          # Rotação vertical (X), evita singularity

        self.fov = 45.0                       # Campo de visão
        self.aspect = 1.0                     # Será atualizado com o resize
        self.near = 0.1
        self.far = 100.0

        # Limites
        self.min_distance = 2.0
        self.max_distance = 20.0

    def orbit(self, dtheta: float, dphi: float, dzoom: float = 0.0):
        """
        Atualiza a câmera com variações em theta, phi e zoom.
        Args:
            dtheta: variação em rotação horizontal (mouse x)
            dphi: variação em rotação vertical (mouse y)
            dzoom: variação de zoom (scroll)
        """
        self.theta += dtheta
        self.phi = glm.clamp(self.phi + dphi, 0.01, glm.pi() - 0.01)  # Evita polos

        # Atualiza distância com zoom
        self.distance = glm.clamp(self.distance + dzoom, self.min_distance, self.max_distance)

    def update_position(self):
        """
        Atualiza a posição da câmera com base em theta, phi e distância.
        """
        # Coordenadas esféricas → cartesianas
        x = self.distance * glm.sin(self.phi) * glm.cos(self.theta)
        y = self.distance * glm.cos(self.phi)
        z = self.distance * glm.sin(self.phi) * glm.sin(self.theta)

        self.position = glm.vec3(x, y, z) + self.center

    def view_matrix(self):
        """
        Retorna a matriz de view (modelo de câmera).
        Chamado em paintGL.
        """
        self.update_position()
        return glm.lookAt(self.position, self.center, glm.vec3(0.0, 1.0, 0.0))

    def projection_matrix(self):
        """
        Retorna a matriz de projeção perspectiva.
        """
        return glm.perspective(self.fov, self.aspect, self.near, self.far)

    def set_aspect(self, aspect: float):
        """
        Atualiza o aspect ratio (largura/altura da janela).
        Chamado em resizeGL.
        """
        self.aspect = aspect

    def resetar(self, fator: float):
        """Reposiciona a câmera para enxergar todo o planeta.
        A câmera é colocada a 4× o raio do planeta do centro.
        """
        # Raio do planeta: fator / (2 * sin(π/5))
        raio_planeta = fator / (2 * glm.sin(glm.pi() / 5))

        # Distância do centro: 4× o raio (3× acima da superfície)
        self.distance = 3.0 * raio_planeta

        # Ângulos iniciais
        self.theta = 0.0
        self.phi = glm.radians(30.0)  # Evita olhar diretamente de cima

        # Atualiza posição
        self.update_position()