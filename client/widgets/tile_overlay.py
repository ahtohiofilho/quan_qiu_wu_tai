# client/widgets/tile_overlay.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSlot
from client.utils.scaling import scale, scale_font


class TileOverlay(QWidget):
    """
    Overlay flutuante centralizado que exibe informações sobre um tile clicado.
    Mostra apenas:
    - Bioma
    - Placa (com letra grega)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setup_ui()
        self.hide()  # Começa oculto

    @staticmethod
    def _rgb_tuple_to_hex(rgb):
        """
        Converte uma tupla RGB (r, g, b) com valores 0-255 para string hex "#RRGGBB"
        :param rgb: tuple(int, int, int)
        :return: str como "#7FFF00"
        """
        if isinstance(rgb, str):
            return rgb.lstrip('#')  # Já é string → remover '#' se tiver
        try:
            r, g, b = rgb
            return f"{int(r):02X}{int(g):02X}{int(b):02X}"
        except (TypeError, ValueError, AttributeError):
            print(f"❌ Falha ao converter cor: {rgb}")
            return "FFFFFF"  # fallback branco

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(scale(20), scale(15), scale(20), scale(15))
        layout.setSpacing(scale(10))

        # Título (opcional — pode ser removido depois)
        self.label_title = QLabel("Informações do Tile")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet(f"""
            font-size: {scale_font(16)}px;
            font-weight: bold;
            color: white;
            margin-bottom: {scale(8)}px;
        """)
        layout.addWidget(self.label_title)

        # Conteúdo principal
        self.label_info = QLabel("Carregando...")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setStyleSheet(f"""
            font-size: {scale_font(13)}px;
            color: #e0e0e0;
            background-color: rgba(40, 40, 60, 180);
            padding: {scale(12)}px;
            border-radius: {scale(8)}px;
            border: 1px solid rgba(255, 255, 255, 30);
        """)
        layout.addWidget(self.label_info)

        # Botão de fechar (canto superior direito)
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(scale(28), scale(28))
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 0, 0, 180);
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        self.btn_close.clicked.connect(self.hide)

        # Layout do botão de fechar
        close_layout = QVBoxLayout()
        close_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        close_layout.addWidget(self.btn_close)
        layout.addLayout(close_layout)

        self.setLayout(layout)

        # Fundo translúcido
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            border-radius: 16px;
        """)

    @pyqtSlot(dict)
    def atualizar_info(self, dados_tile, assentamentos=None):
        """
        Updates the overlay with:
        - Biome
        - Plate (with Greek letter)
        - List of settlements (if any), including:
            - Civilization name
            - Population
            - Parcel type (e.g. 'Central', 'Southeast')

        :param dados_tile: dict with keys 'bioma', 'placa', 'letra_grega'
        :param assentamentos: list of settlement dicts with keys:
                             {'civilizacao': Civ, 'populacao': int, 'tipo_parcela': str}
        """
        # Basic tile data
        bioma = dados_tile.get("bioma", "Unknown").title()
        placa = dados_tile.get("placa")
        letra_grega = dados_tile.get("letra_grega")

        if placa and letra_grega:
            placa_str = f"{placa} ({letra_grega})"
        elif placa:
            placa_str = placa
        else:
            placa_str = "None"

        info_lines = [
            f"<b>{bioma}</b>",
            f"Plate: {placa_str}"
        ]

        # Add settlements if present
        if assentamentos and len(assentamentos) > 0:
            info_lines.append("<hr style='border: 1px solid #555;'>")  # Divider
            for ass in assentamentos:
                civ_nome = ass["civilizacao"].nome
                pop_total = ass["populacao"]
                tipo_parcela = ass["tipo_parcela"]  # e.g. "Central", "Southeast"
                raw_cor = ass["civilizacao"].cor
                cor_hex = self._rgb_tuple_to_hex(raw_cor)
                marker = f"<span style='color:#{cor_hex};'>●</span>"
                formatted_pop = f"{pop_total:,}"  # Add thousand separators
                info_lines.append(
                    f"{marker} <b>{civ_nome}</b>: {formatted_pop} pop ({tipo_parcela})"
                )

        self.label_info.setText("<br>".join(info_lines))

    def show_centered(self):
        """
        Centraliza o overlay dentro do widget pai (ex: opengl_container).
        """
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        width = scale(320)
        height = scale(160)  # Reduzido: menos altura, mais compacto
        x = (parent_rect.width() - width) // 2
        y = (parent_rect.height() - height) // 2

        self.setGeometry(x, y, width, height)
        self.show()
        self.raise_()