# client/widgets/match_overlay.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class OverlayPartida(QWidget):
    """Overlay flutuante dentro da barra esquerda, exibido apenas durante a partida.
    Contém controles de ação e um seletor para alternar entre modo de mapa físico e político.
    Centralizado verticalmente, com fundo translúcido e largura ajustada à barra.
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
        """)
        self.setup_ui()
        self.update_position()  # Posiciona inicialmente

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

        # Se chegou aqui, não encontrou ninguém com o método
        print("⚠️ OverlayPartida: 'mudar_modo_mapa' não encontrado em nenhum ancestral.")

    def setup_ui(self):
        """Configura a interface com apenas o botão toggle para alternar entre modo físico e político."""
        from client.utils.scaling import scale, scale_font  # Importa as funções de escala

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            scale(10), scale(12), scale(10), scale(12)
        )
        layout.setSpacing(scale(6))
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão de alternância de modo (toggle entre físico e político)
        self.btn_modo_mapa = QPushButton("🌍")  # Começa no modo físico
        self.btn_modo_mapa.setFixedSize(scale(60), scale(40))
        self.btn_modo_mapa.setToolTip("Alternar modo de mapa (Físico/Político)")

        # Estilo com valores escalonados via f-string
        estilo = f"""
            QPushButton {{
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: {scale(8)}px;
                font-size: {scale_font(18)}px;
                font-weight: bold;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #34495e;
                border-color: #1abc9c;
            }}
            QPushButton:pressed {{
                background-color: #1abc9c;
                border-color: #16a085;
            }}
        """
        self.btn_modo_mapa.setStyleSheet(estilo)
        self.btn_modo_mapa.clicked.connect(self.alternar_modo_mapa)
        layout.addWidget(self.btn_modo_mapa)

        self.setLayout(layout)

    def update_position(self):
        """Atualiza posição e tamanho com base no widget pai (barra_esquerda),
        respeitando os limites de 320px e 15% da largura da tela.
        """
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        parent_width = parent_rect.width()
        parent_height = parent_rect.height()

        # --- Calcular largura do overlay: 85% da largura da barra ---
        width = int(parent_width * 0.85)

        # --- Calcular altura: até 45% da altura da barra, com limite mínimo e máximo (com escala) ---
        from client.utils.scaling import scale

        max_height = scale(200)  # Altura máxima escalonada (ex: 200 → 300 em 150% DPI)
        min_height = scale(80)  # Altura mínima (para não sumir)
        height = min(max_height, int(parent_height * 0.45))
        height = max(min_height, height)

        # --- Centralizar no pai ---
        x = (parent_width - width) // 2
        y = (parent_height - height) // 2

        # --- Aplicar geometria ---
        self.setGeometry(x, y, width, height)

        # Opcional: forçar atualização de layout interno, se necessário
        self.setFixedWidth(width)
        self.setFixedHeight(height)