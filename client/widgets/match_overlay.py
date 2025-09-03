# client/widgets/match_overlay.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from client.utils.scaling import scale, scale_font  # Importa as funções de escala


class OverlayPartida(QWidget):
    """
    Overlay flutuante dentro da barra esquerda, exibido apenas durante a partida.
    Contém:
    - Botão para avançar o turno
    - Exibição de turno e população
    - Botão para alternar modo de mapa (físico/político)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Referência ao widget pai (barra_esquerda)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(40, 40, 55, 220);
            border-radius: 12px;
            border: 1px solid #3498db;
            color: #ecf0f1;
            font-family: Arial, sans-serif;
            font-size: 13px;
        """)
        self.setup_ui()
        self.update_position()

    def setup_ui(self):
        """Configura a interface com botões e labels."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(scale(15), scale(15), scale(15), scale(15))
        layout.setSpacing(scale(12))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Título ---
        titulo = QLabel("🕹️ Ações da Partida")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # --- Display de Turno ---
        self.label_turno = QLabel("Turno: 0")
        self.label_turno.setStyleSheet("font-size: 14px; color: #cccccc; font-weight: bold;")
        self.label_turno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_turno)

        # --- Display de População ---
        self.label_pop = QLabel("População: 0")
        self.label_pop.setStyleSheet("font-size: 13px; color: #aaaaaa;")
        self.label_pop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_pop)

        # --- Botão de Avançar Turno ---
        self.botao_turno = QPushButton("⏭️ Avançar Turno")
        self.botao_turno.setStyleSheet(self._estilo_botao("#4CAF50", "#45a049", "#3d8b40"))
        self.botao_turno.clicked.connect(self.on_avancar_turno)
        layout.addWidget(self.botao_turno)

        # --- Botão de Modo de Mapa ---
        self.btn_modo_mapa = QPushButton("🌍")  # Começa no modo físico
        self.btn_modo_mapa.setFixedSize(scale(60), scale(40))
        self.btn_modo_mapa.setToolTip("Alternar modo de mapa (Físico/Político)")
        self.btn_modo_mapa.setStyleSheet(self._estilo_botao("#2c3e50", "#34495e", "#1abc9c"))
        self.btn_modo_mapa.clicked.connect(self.alternar_modo_mapa)
        layout.addWidget(self.btn_modo_mapa, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _estilo_botao(self, bg, hover, pressed):
        """Retorna string de estilo para botões com cores personalizadas."""
        return f"""
            QPushButton {{
                background-color: {bg};
                color: white;
                border: 1px solid #3498db;
                border-radius: {scale(8)}px;
                padding: {scale(8)}px;
                font-size: {scale_font(13)}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover};
                border-color: #1abc9c;
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """

    def on_avancar_turno(self):
        """Avança o turno no mundo atual."""
        print("🟢 [OverlayPartida] Botão 'Avançar Turno' clicado.")

        # Buscar JanelaPrincipal subindo na hierarquia
        janela_principal = self._obter_janela_principal()
        if not janela_principal:
            print("❌ [OverlayPartida] JanelaPrincipal não encontrada.")
            return

        if not hasattr(janela_principal, 'mundo') or not janela_principal.mundo:
            print("⚠️ [OverlayPartida] Mundo não disponível.")
            return

        mundo = janela_principal.mundo

        # Avança o turno
        try:
            mundo.turno.avancar(mundo)
            self.atualizar_display(mundo)
            print(f"✅ Turno {mundo.turno.numero} avançado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao avançar turno: {e}")

    def atualizar_display(self, mundo):
        """Atualiza os labels de turno e população."""
        self.label_turno.setText(f"Turno: {mundo.turno.numero}")
        h, m, t = mundo.get_populacao_global()
        pop_formatada = self._formatar_numero(t)
        homens_formatado = self._formatar_numero(h)
        mulheres_formatado = self._formatar_numero(m)
        self.label_pop.setText(f"Pop: {pop_formatada} (H={homens_formatado}, M={mulheres_formatado})")

    def conectar_mundo(self, mundo):
        """Conecta o overlay a um mundo e atualiza o display inicial."""
        self.atualizar_display(mundo)

    def alternar_modo_mapa(self):
        """Alterna entre modo físico e político e atualiza o ícone do botão."""
        novo_modo = "politico" if self.btn_modo_mapa.text() == "🌍" else "fisico"
        novo_icone = "🏛️" if novo_modo == "politico" else "🌍"

        self.btn_modo_mapa.setText(novo_icone)
        self.btn_modo_mapa.setToolTip(f"Modo: {'Político' if novo_modo == 'politico' else 'Físico'}")
        print(f"🔄 Modo de mapa alterado para: {novo_modo}")

        # === NAVEGAR PELA HIERARQUIA ATÉ A JANELA PRINCIPAL ===
        widget_atual = self.parent_widget
        while widget_atual is not None:
            if hasattr(widget_atual, 'mudar_modo_mapa'):
                widget_atual.mudar_modo_mapa(novo_modo)
                return
            widget_atual = widget_atual.parent()

        print("⚠️ OverlayPartida: 'mudar_modo_mapa' não encontrado em nenhum ancestral.")

    def update_position(self):
        """Atualiza posição e tamanho com base no widget pai (barra_esquerda)."""
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        parent_width = parent_rect.width()
        parent_height = parent_rect.height()

        # Largura: 85% da barra
        width = int(parent_width * 0.85)

        # Altura: até 50% da altura da barra, com limites
        max_height = scale(300)
        min_height = scale(120)
        height = min(max_height, int(parent_height * 0.5))
        height = max(min_height, height)

        # Centralizar verticalmente
        x = (parent_width - width) // 2
        y = (parent_height - height) // 2

        self.setGeometry(x, y, width, height)
        self.setFixedWidth(width)
        self.setFixedHeight(height)

    def _obter_janela_principal(self):
        """Obtém a instância de JanelaPrincipal subindo na hierarquia."""
        widget_atual = self.parent_widget
        while widget_atual is not None:
            if hasattr(widget_atual, 'mudar_modo_mapa'):  # Assumindo que é único da JanelaPrincipal
                return widget_atual
            widget_atual = widget_atual.parent()
        return None

    def _formatar_numero(self, valor: int) -> str:
        """
        Formata número grande com sufixos: K (mil), M (milhão), B (bilhão), T (trilhão)
        Ex: 1500 → "1.5k", 2300000 → "2.3m"
        """
        if valor < 1000:
            return str(valor)
        elif valor < 1_000_000:
            return f"{valor / 1000:.1f}k"
        elif valor < 1_000_000_000:
            return f"{valor / 1_000_000:.1f}m"
        elif valor < 1_000_000_000_000:
            return f"{valor / 1_000_000_000:.1f}b"
        else:
            return f"{valor / 1_000_000_000_000:.1f}t"