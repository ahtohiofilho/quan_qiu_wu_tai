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

    def __init__(self, assentamento: Assentamento, region_clicked: str, tile_coords, mundo, parent=None):
        super().__init__(parent)
        self.assentamento = assentamento
        self.region_clicked = region_clicked # Name of the region where the click occurred
        self.tile_coords = tile_coords
        self.mundo = mundo # Reference to the world for fetching information
        self.parent_widget = parent # Optional, for reference to TileOverlay or another parent

        # --- Ensure opaque background ---
        # Remove the translucent background attribute (if inherited)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        # Set window flags (optional, for a standard window with title bar and buttons)
        # self.setWindowFlags(Qt.WindowType.Window) # Uncomment for standard title bar
        # To keep it frameless but ensure it covers the parent:
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Define title based on settlement existence
        if self.assentamento:
            civ_nome = self.assentamento.civilizacao.nome if self.assentamento.civilizacao else "Unknown"
            self.setWindowTitle(f"Settlement: {civ_nome} - Region: {region_clicked}")
        else:
            self.setWindowTitle(f"Region: {region_clicked} - Tile: {tile_coords}")

        # Set initial size (this will be overridden if maximizing to parent)
        # self.resize(600, 500)

        # --- Set Parent and Geometry (to cover the parent) ---
        # This makes it behave more like an overlay on the parent widget
        if self.parent_widget:
            self.setParent(self.parent_widget)
            # Optionally, you can set a stylesheet for the parent to see the overlay clearly
            # self.parent_widget.setStyleSheet("background-color: rgba(0, 0, 0, 100);") # Example
        # --- FIM NOVO ---

        # Apply style sheet for opaque background and other styling
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
        # Adjust geometry after UI is set up
        if self.parent_widget:
             self.setGeometry(self.parent_widget.rect()) # Cover the entire parent
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
            title_label = QLabel(f"Settlement of {self.assentamento.civilizacao.nome}")
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

        # --- Region Info Group (Always Present) ---
        info_region_group = QGroupBox("Region Information")
        info_region_layout = QVBoxLayout(info_region_group)

        self.info_region_text = QTextEdit()
        self.info_region_text.setReadOnly(True)
        info_region_layout.addWidget(self.info_region_text)
        main_layout.addWidget(info_region_group)

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

            main_layout.addWidget(info_settlement_group)

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
        # Assuming get_populacao_total() and calcular_producao_total() exist and work
        populacao = self.assentamento.get_populacao_total()
        producao = self.assentamento.calcular_producao_total()

        info_text_content = f"civilization: {self.assentamento.civilizacao.nome}\n" # Changed to English
        info_text_content += f"Parcel on Tile: {self.assentamento.indice_parcela}\n"
        info_text_content += f"Tile Coordinates: {self.assentamento.coordenadas_tile}\n"
        info_text_content += f"Total Population: {populacao}\n"
        info_text_content += f"Estimated Production: {producao:.2f}\n"
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