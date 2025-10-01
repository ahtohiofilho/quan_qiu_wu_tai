# client/widgets/information_window.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QTextEdit, QGroupBox, QListWidget)
from PyQt6.QtCore import Qt
from shared.settlement import Assentamento # Importar para usar PARCELA_CENTRAL e métodos

class JanelaInformacaoRegiao(QWidget):
    """Window for displaying information about a clicked region.
    If there's a settlement on the clicked parcel, it also shows settlement information.
    Otherwise, it shows only general tile/region info.
    """

    def __init__(self, assentamento: Assentamento, region_clicked: str, tile_coords, mundo, overlay_coords=None): # Removido parent, adicionado overlay_coords
        super().__init__(parent=None) # <--- Janela independente
        self.assentamento = assentamento
        self.region_clicked = region_clicked # Name of the region where the click occurred
        self.tile_coords = tile_coords
        self.mundo = mundo # Reference to the world for fetching information
        # self.parent_widget = parent # REMOVIDO
        self.overlay_coords = overlay_coords # Coordenadas globais do TileOverlay para posicionar esta janela

        # --- Ensure opaque background ---
        # Remove the translucent background attribute (if inherited)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        # Define title based on settlement existence
        if self.assentamento:
            print(f"Nome do assentamento: {self.assentamento.nome}")
            # self.setWindowTitle(self.assentamento.nome)
            self.setWindowTitle(f"{self.assentamento.civilizacao.nome}")
        else:
            print(f"Região clicada: {region_clicked} em tile {tile_coords}, sem assentamento.")
            # self.setWindowTitle(f"Region: {region_clicked} - Tile: {tile_coords}")
            self.setWindowTitle("Informações da Região")

        # Set initial size (this will be overridden if maximizing to parent)
        # self.resize(600, 500)

        # --- Apply style sheet for opaque background and other styling ---
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50; /* Solid background color (e.g., dark gray) */
                color: #ECF0F1; /* Text color */
                border-radius: 8px; /* Rounded corners, optional */
            }
            QGroupBox {
                border: 1px solid #34495E; /* Group box borders */
                border-radius: 5px;
                margin-top: 5px; /* Space above the group title */
                padding-top: 5px; /* Internal padding above the group title */
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px; /* Title position */
                padding: 0 5px 0 5px; /* Title internal padding */
            }
            QTextEdit {
                background-color: #34495E; /* QTextEdit background */
                border: 1px solid #34495E;
                border-radius: 3px;
            }
            QListWidget {
                background-color: #34495E; /* QListWidget background */
                border: 1px solid #34495E;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #3498DB; /* Button color */
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980B9; /* Button color on hover */
            }
        """)

        self.setup_ui()
        # --- Position the window based on overlay_coords ---
        if self.overlay_coords:
            overlay_x, overlay_y, overlay_width, overlay_height = self.overlay_coords
            # Position near the overlay, maybe slightly offset
            # You can adjust the offset (e.g., +20, +20) or center it relative to the overlay
            window_width = 800 # Ajustado para refletir a nova largura desejada
            window_height = 600 # Ajustado se necessário
            # Example: Position top-left corner near the bottom-right of the overlay
            pos_x = overlay_x + overlay_width + 5 # Small offset
            pos_y = overlay_y + overlay_height + 5 # Small offset
            # Ensure it doesn't go off-screen (optional)
            # screen = self.screen().availableGeometry()
            # pos_x = min(pos_x, screen.width() - window_width)
            # pos_y = min(pos_y, screen.height() - window_height)

            self.setGeometry(pos_x, pos_y, window_width, window_height)
            print(f"🔍 [JanelaInformacaoRegiao] Posicionada em ({pos_x}, {pos_y}) com base em overlay_coords.")
        # --- END Positioning ---

        self.load_region_data() # Load region data (always)
        if self.assentamento:
            self.load_settlement_data() # Load settlement data (if it exists)

    def setup_ui(self):
        """Sets up the UI widgets."""
        # Use a main layout to position the close button and content
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10) # Add margins around the content
        main_layout.setSpacing(5) # Add spacing between elements

        # --- Title ---
        if self.assentamento:
            title_label = QLabel(f"{self.assentamento.nome}")
        else:
            title_label = QLabel(f"Region: {self.region_clicked}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # --- Separator ---
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        # --- NEW: Horizontal Layout for Split Content ---
        content_split_layout = QHBoxLayout()
        content_split_layout.setContentsMargins(0, 0, 0, 0) # Opcional: remover margens internas
        content_split_layout.setSpacing(5) # Opcional: espaçamento entre as colunas

        # --- Left Column Layout (1/3 width) ---
        left_column_layout = QVBoxLayout()
        left_column_layout.setContentsMargins(0, 0, 0, 0) # Opcional: remover margens
        left_column_layout.setSpacing(5) # Espaçamento entre os widgets da coluna esquerda

        # --- Region Info Group (Always Present) ---
        info_region_group = QGroupBox("Region Information")
        info_region_layout = QVBoxLayout(info_region_group)

        self.info_region_text = QTextEdit()
        self.info_region_text.setReadOnly(True)
        info_region_layout.addWidget(self.info_region_text)
        # main_layout.addWidget(info_region_group) # <-- REMOVIDO daqui
        left_column_layout.addWidget(info_region_group) # <-- ADICIONADO aqui

        # --- Settlement Info Group (Conditional) ---
        if self.assentamento:
            info_settlement_group = QGroupBox("Settlement Information")
            info_settlement_layout = QVBoxLayout(info_settlement_group)

            # --- Simple Settlement Data ---
            self.info_settlement_text = QTextEdit()
            self.info_settlement_text.setReadOnly(True)
            self.info_settlement_text.setMaximumHeight(150) # Limit text box height
            info_settlement_layout.addWidget(self.info_settlement_text)

            # --- Units List ---
            units_list_group = QGroupBox("Units")
            units_list_layout = QVBoxLayout(units_list_group)
            self.units_list = QListWidget()
            # Populate with real data in load_settlement_data
            units_list_layout.addWidget(self.units_list)
            info_settlement_layout.addWidget(units_list_group)

            # --- Other groups can be added here ---
            # Ex: Resources, Buildings, etc.

            # main_layout.addWidget(info_settlement_group) # <-- REMOVIDO daqui
            left_column_layout.addWidget(info_settlement_group) # <-- ADICIONADO aqui

        # Adiciona a coluna esquerda ao layout horizontal com fator de estiramento 1
        content_split_layout.addLayout(left_column_layout, 1)

        # --- Empty Space on the Right (2/3 width) ---
        content_split_layout.addStretch(2)

        # Adiciona o layout horizontal ao layout principal
        main_layout.addLayout(content_split_layout)

        # --- Close Button (Positioned Top Right) ---
        # Create a horizontal layout just for the close button
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch() # Add a stretchable space to push the button to the right

        self.btn_close = QPushButton("Close") # Changed text to English
        # self.btn_close.setFixedSize(scale(30), scale(30)) # Don't use fixed size, let layout manage
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; /* Red color */
                color: white;
                border-radius: 4px; /* Slightly rounded corners */
                padding: 5px 10px; /* Internal padding */
                font-weight: bold;
                min-width: 60px; /* Minimum width */
            }
            QPushButton:hover {
                background-color: #c0392b; /* Darker red on hover */
            }
        """)
        self.btn_close.clicked.connect(self.close) # Connect close signal
        close_button_layout.addWidget(self.btn_close) # Add button to the right-aligned layout

        main_layout.addLayout(close_button_layout) # Add the button layout to the main layout

    def load_region_data(self):
        """Loads and displays general region data from the world."""
        print(f"🔍 [JanelaInformacaoRegiao] Loading data for region '{self.region_clicked}' on tile {self.tile_coords}.")

        # Get node data from the world graph
        node_data = self.mundo.planeta.geografia.nodes.get(self.tile_coords, {})
        bioma = node_data.get('bioma', 'Unknown')
        formato = node_data.get('formato', 'Unknown')
        # Add more data as needed (e.g., tile productivity coefficient, etc.)

        info_text_content = f"Region Name: {self.region_clicked}\n"
        info_text_content += f"Tile Coordinates: {self.tile_coords}\n"
        info_text_content += f"Biome: {bioma}\n"
        info_text_content += f"Tile Type: {formato}\n"
        # info_text_content += f"Other Data: {value}\n" # Add other data

        self.info_region_text.setPlainText(info_text_content)

    def load_settlement_data(self):
        """Loads and displays settlement data (if it exists)."""
        if not self.assentamento:
            print(f"⚠️ [JanelaInformacaoRegiao] load_settlement_data called, but settlement is None.")
            return

        print(f"🔍 [JanelaInformacaoRegiao] Loading data for settlement of '{self.assentamento.civilizacao.nome}' on parcel {self.assentamento.indice_parcela} of tile {self.assentamento.coordenadas_tile}.")

        # --- Settlement Information (initially just the civilization name and parcel) ---
        # Hardcoded por enquanto
        populacao = "N pessoas" # self.assentamento.get_populacao_total()
        producao = "X produção" # self.assentamento.calcular_producao_total()

        info_text_content = f"civilization: {self.assentamento.civilizacao.nome}\n" # Changed to English
        info_text_content += f"Parcel on Tile: {self.assentamento.indice_parcela}\n"
        info_text_content += f"Tile Coordinates: {self.assentamento.coordenadas_tile}\n"
        info_text_content += f"Total Population: {populacao}\n"
        info_text_content += f"Estimated Production: {producao}\n"
        # ... add more information as it becomes available

        self.info_settlement_text.setPlainText(info_text_content)

        # --- Populate Units List ---
        # Assuming the settlement has a list of units (e.g., self.assentamento.unidades)
        # For now, add placeholders
        self.units_list.clear()
        # Real example (uncomment if unit list exists):
        # for unidade in self.assentamento.unidades:
        #     self.units_list.addItem(f"{unidade.tipo} - Level {unidade.nivel}")

        # Placeholder for now
        self.units_list.addItem("Example Unit 1")
        self.units_list.addItem("Example Unit 2")
        # Add more placeholders or real data here

    def closeEvent(self, event):
        """
        Evento chamado quando a janela é fechada.
        Opcional: tentar forçar update do OpenGLWidget aqui também, embora sendo independente,
        o problema de sobreposição com o Popup original possa ser resolvido.
        """
        print("🔍 [JanelaInformacaoRegiao] closeEvent chamado.")
        # Chama o closeEvent original para garantir o fechamento padrão
        super().closeEvent(event)

        # Opcional: Tentar atualizar o OpenGLWidget pai (se acessível via módulo ou referência global)
        # Isso é mais difícil agora que não é filha direta do TileOverlay.
        # Talvez o TileOverlay, ao ver sua referência sendo limpa, force a atualização?
        # A responsabilidade de atualização pode voltar para o TileOverlay.

        print("✅ [JanelaInformacaoRegiao] closeEvent concluído.")