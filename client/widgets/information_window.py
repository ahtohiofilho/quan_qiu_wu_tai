# --- client/widgets/information_window.py ---
# Atualizado para salvar/carregar seleções e adicionar ícones para mulheres
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QFrame, QTextEdit,
    QGroupBox, QComboBox, QDialog,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from shared.settlement import Assentamento
from client.dialogs.military_config import MilitaryUnitConfigDialog
from client.utils.scaling import scale

class JanelaInformacaoRegiao(QWidget):
    """Window for displaying information about a clicked region.
    If there's a settlement on the clicked parcel, it also shows settlement information.
    Otherwise, it shows only general tile/region info.
    """

    def __init__(self, assentamento: Assentamento, region_clicked: str, tile_coords, mundo, overlay_coords=None):
        super().__init__(parent=None)
        self.assentamento = assentamento
        self.region_clicked = region_clicked
        self.tile_coords = tile_coords
        self.mundo = mundo
        self.overlay_coords = overlay_coords
        self.units_list = None

        tamanho_icone = 64
        tamanho_escalado = scale(tamanho_icone)

        self.men_allocation_icon_label = QLabel("No Allocation")
        self.men_allocation_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.men_allocation_icon_label.setMinimumSize(tamanho_escalado, tamanho_escalado)
        self.men_allocation_icon_label.setMaximumSize(tamanho_escalado, tamanho_escalado)
        self.men_allocation_icon_label.setScaledContents(True)

        self.women_allocation_icon_label = QLabel("No Allocation")
        self.women_allocation_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.women_allocation_icon_label.setMinimumSize(tamanho_escalado, tamanho_escalado)
        self.women_allocation_icon_label.setMaximumSize(tamanho_escalado, tamanho_escalado)
        self.women_allocation_icon_label.setScaledContents(True)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        if self.assentamento:
            print(f"Nome do assentamento: {self.assentamento.nome}")
            self.setWindowTitle(f"{self.assentamento.civilizacao.nome}")
        else:
            print(f"Região clicada: {region_clicked} em tile {tile_coords}, sem assentamento.")
            self.setWindowTitle("Informações da Região")

        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                color: #ECF0F1;
                border-radius: 8px;
            }
            QGroupBox {
                border: 1px solid #34495E;
                border-radius: 5px;
                margin-top: 5px;
                padding-top: 5px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTextEdit {
                background-color: #34495E;
                border: 1px solid #34495E;
                border-radius: 3px;
            }
            QListWidget {
                background-color: #34495E;
                border: 1px solid #34495E;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QComboBox {
                background-color: #34495E;
                border: 1px solid #34495E;
                border-radius: 3px;
                padding: 5px;
                color: #ECF0F1;
            }
        """)

        self.showMaximized()
        self.setup_ui()

        # --- Conectar os combos para atualizar os ícones ---
        print("🔍 [DEBUG] Verificando existência de combos e labels no __init__:")
        print(f"  - self.new_men_combo: {hasattr(self, 'new_men_combo')}")
        print(f"  - self.men_allocation_icon_label: {hasattr(self, 'men_allocation_icon_label')}")
        print(f"  - self.new_women_combo: {hasattr(self, 'new_women_combo')}")
        print(f"  - self.women_allocation_icon_label: {hasattr(self, 'women_allocation_icon_label')}")

        if hasattr(self, 'new_men_combo') and hasattr(self, 'men_allocation_icon_label'):
            print("🔗 [DEBUG] Conectando sinal de homens para atualizar ícone e salvar.")
            self.new_men_combo.currentTextChanged.connect(self._atualizar_icone_alocacao_homens)
            self.new_men_combo.currentTextChanged.connect(self._on_new_men_combo_changed) # Conexão para salvar e abrir popup
            self._carregar_selecao_homens_do_assentamento()

        if hasattr(self, 'new_women_combo') and hasattr(self, 'women_allocation_icon_label'):
            print("🔗 [DEBUG] Conectando sinal de mulheres para atualizar ícone e salvar.")
            # --- ADICIONANDO PRINT DE DEBUG ---
            print(f"   - Sinal currentTextChanged do combo de mulheres conectado a _atualizar_icone_alocacao_mulheres: {self._atualizar_icone_alocacao_mulheres}")
            print(f"   - Sinal currentTextChanged do combo de mulheres conectado a _on_new_women_combo_changed: {self._on_new_women_combo_changed}")
            # --- FIM ADICIONANDO PRINT DE DEBUG ---
            self.new_women_combo.currentTextChanged.connect(self._atualizar_icone_alocacao_mulheres)
            self.new_women_combo.currentTextChanged.connect(self._on_new_women_combo_changed) # Conexão para salvar
            self._carregar_selecao_mulheres_do_assentamento()
        else:
            print("⚠️ [DEBUG] Combo ou label de mulheres não encontrado(s) no __init__.")

        if self.overlay_coords:
            overlay_x, overlay_y, overlay_width, overlay_height = self.overlay_coords
            window_width = 800
            window_height = 600
            pos_x = overlay_x + overlay_width + 5
            pos_y = overlay_y + overlay_height + 5
            self.setGeometry(pos_x, pos_y, window_width, window_height)
            print(f"🔍 [JanelaInformacaoRegiao] Posicionada em ({pos_x}, {pos_y}) com base em overlay_coords.")

        self.load_region_data()
        if self.assentamento:
            self.load_settlement_data()

    def _carregar_selecao_homens_do_assentamento(self):
        """Carrega a seleção de alocação de homens do objeto assentamento."""
        if not self.assentamento:
            print("⚠️ [JanelaInformacaoRegiao] _carregar_selecao_homens_do_assentamento: Nenhum assentamento para carregar seleção.")
            return

        alocacoes = getattr(self.assentamento, 'alocacoes', {})
        selecao_salva = alocacoes.get('homens', 'Farm')

        index = self.new_men_combo.findText(selecao_salva)
        if index >= 0:
            self.new_men_combo.setCurrentIndex(index)
            print(f"🔍 [JanelaInformacaoRegiao] Seleção de homens carregada: {selecao_salva}")
        else:
            print(f"⚠️ [JanelaInformacaoRegiao] Seleção de homens salva '{selecao_salva}' não encontrada no combo. Usando padrão.")
            self.new_men_combo.setCurrentText('Farm')
        self._atualizar_icone_alocacao_homens(self.new_men_combo.currentText())

    def _carregar_selecao_mulheres_do_assentamento(self):
        """Carrega a seleção de alocação de mulheres do objeto assentamento."""
        if not self.assentamento:
            print("⚠️ [JanelaInformacaoRegiao] _carregar_selecao_mulheres_do_assentamento: Nenhum assentamento para carregar seleção.")
            return

        alocacoes = getattr(self.assentamento, 'alocacoes', {})
        selecao_salva = alocacoes.get('mulheres', 'Home')

        index = self.new_women_combo.findText(selecao_salva)
        if index >= 0:
            self.new_women_combo.setCurrentIndex(index)
            print(f"🔍 [JanelaInformacaoRegiao] Seleção de mulheres carregada: {selecao_salva}")
        else:
            print(f"⚠️ [JanelaInformacaoRegiao] Seleção de mulheres salva '{selecao_salva}' não encontrada no combo. Usando padrão.")
            self.new_women_combo.setCurrentText('Home')
            selecao_salva = 'Home'

        # --- ADICIONANDO PRINT DE DEBUG ---
        print(f"   - Chamando _atualizar_icone_alocacao_mulheres com texto carregado: '{self.new_women_combo.currentText()}'")
        # --- FIM ADICIONANDO PRINT DE DEBUG ---
        self._atualizar_icone_alocacao_mulheres(self.new_women_combo.currentText())

    def _atualizar_icone_alocacao_homens(self, texto_combo):
        """Atualiza o ícone exibido com base na seleção do combo de homens."""
        if not texto_combo:
            self.men_allocation_icon_label.setText("No Allocation")
            self.men_allocation_icon_label.setPixmap(QPixmap())
            return

        icon_paths = {
            "Farm": "client/resources/shovel.png",
            "Mine": "client/resources/pickaxe.png",
            "Home": "client/resources/house.png",
            "Armed Forces": "client/resources/helmet.png",
        }

        caminho_imagem = icon_paths.get(texto_combo)

        if caminho_imagem:
            pixmap = QPixmap(caminho_imagem)
            if not pixmap.isNull():
                print(f"🖼️ [JanelaInformacaoRegiao] Ícone para alocação de homens '{texto_combo}' carregado: {caminho_imagem}")
                self.men_allocation_icon_label.setPixmap(pixmap)
                self.men_allocation_icon_label.setText("") # Limpa o texto, se houver
            else:
                print(f"⚠️ [JanelaInformacaoRegiao] Imagem do ícone para alocação de homens '{texto_combo}' não encontrada: {caminho_imagem}")
                self.men_allocation_icon_label.setText(f"Icon: {texto_combo}")
                self.men_allocation_icon_label.setPixmap(QPixmap())
        else:
            print(f"⚠️ [JanelaInformacaoRegiao] Nenhum ícone mapeado para alocação de homens '{texto_combo}'.")
            self.men_allocation_icon_label.setText(f"Icon: {texto_combo}")
            self.men_allocation_icon_label.setPixmap(QPixmap())

    def _atualizar_icone_alocacao_mulheres(self, texto_combo):
        """Atualiza o ícone exibido com base na seleção do combo de mulheres."""
        print(f"🔄 [DEBUG] _atualizar_icone_alocacao_mulheres chamado com texto_combo: '{texto_combo}'") # <-- DEBUG

        if not texto_combo:
            print("🔍 [DEBUG] texto_combo é vazio, limpando label.") # <-- DEBUG
            self.women_allocation_icon_label.setText("No Allocation")
            self.women_allocation_icon_label.setPixmap(QPixmap())
            return

        # Mapeia o texto do combo para o caminho da imagem
        # Certifique-se de que os caminhos estejam corretos e as imagens existam
        icon_paths = {
            "Home": "client/resources/house.png", # Exemplo - verifique se o caminho está correto
            "Farm": "client/resources/shovel.png", # Exemplo - verifique se o caminho está correto
            "Mine": "client/resources/pickaxe.png", # Exemplo - verifique se o caminho está correto
            # Adicione mais mapeamentos conforme as opções do combo
        }

        print(f"   - Dicionário icon_paths: {icon_paths}") # <-- DEBUG
        caminho_imagem = icon_paths.get(texto_combo)
        print(f"   - Caminho imagem encontrado para '{texto_combo}': {caminho_imagem}") # <-- DEBUG

        if caminho_imagem:
            print(f"   - Tentando carregar QPixmap de: {caminho_imagem}") # <-- DEBUG
            pixmap = QPixmap(caminho_imagem)
            if not pixmap.isNull():
                print(f"🖼️ [JanelaInformacaoRegiao] Ícone para alocação de mulheres '{texto_combo}' carregado: {caminho_imagem}")
                self.women_allocation_icon_label.setPixmap(pixmap)
                self.women_allocation_icon_label.setText("") # Limpa o texto, se houver
            else:
                print(f"⚠️ [JanelaInformacaoRegiao] Imagem do ícone para alocação de mulheres '{texto_combo}' não encontrada ou inválida: {caminho_imagem}")
                self.women_allocation_icon_label.setText(f"Icon: {texto_combo}")
                self.women_allocation_icon_label.setPixmap(QPixmap())
        else:
            print(f"⚠️ [JanelaInformacaoRegiao] Nenhum ícone mapeado para alocação de mulheres '{texto_combo}'.")
            self.women_allocation_icon_label.setText(f"Icon: {texto_combo}")
            self.women_allocation_icon_label.setPixmap(QPixmap())

    def setup_ui(self):
        """Sets up the UI widgets."""
        print("🎨 [DEBUG] Iniciando setup_ui") # <-- DEBUG
        # Use a main layout to position the close button and content
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add margins around the content
        main_layout.setSpacing(5)  # Add spacing between elements

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
        content_split_layout.setContentsMargins(0, 0, 0, 0)  # Opcional: remover margens internas
        content_split_layout.setSpacing(5)  # Opcional: espaçamento entre as colunas

        # --- Left Column Layout (1/3 width) ---
        left_column_layout = QVBoxLayout()
        left_column_layout.setContentsMargins(0, 0, 0, 0)  # Opcional: remover margens
        left_column_layout.setSpacing(5)  # Espaçamento entre os widgets da coluna esquerda

        # --- Region Info Group (Always Present) ---
        info_region_group = QGroupBox("Region Information")
        info_region_layout = QVBoxLayout(info_region_group)

        self.info_region_text = QTextEdit()
        self.info_region_text.setReadOnly(True)
        info_region_layout.addWidget(self.info_region_text)
        # main_layout.addWidget(info_region_group) # <-- REMOVIDO daqui
        left_column_layout.addWidget(info_region_group)  # <-- ADICIONADO aqui

        # --- Settlement Info Group (Conditional) ---
        if self.assentamento:
            info_settlement_group = QGroupBox("Settlement Information")
            info_settlement_layout = QVBoxLayout(info_settlement_group)

            # --- Simple Settlement Data ---
            self.info_settlement_text = QTextEdit()
            self.info_settlement_text.setReadOnly(True)
            self.info_settlement_text.setMaximumHeight(150)  # Limit text box height
            info_settlement_layout.addWidget(self.info_settlement_text)

            # --- Other groups can be added here ---
            # Ex: Resources, Buildings, etc.

            # main_layout.addWidget(info_settlement_group) # <-- REMOVIDO daqui
            left_column_layout.addWidget(info_settlement_group)  # <-- ADICIONADO aqui

        # Adiciona a coluna esquerda ao layout horizontal com fator de estiramento 1
        content_split_layout.addLayout(left_column_layout, 1)  # 1 parte

        # --- NEW: Right Column Layout (2/3 width) ---
        right_column_layout = QVBoxLayout()  # Layout vertical para o lado direito
        right_column_layout.setContentsMargins(0, 0, 0, 0)  # Opcional: remover margens
        right_column_layout.setSpacing(5)  # Espaçamento entre widgets na coluna direita (se houver mais)

        if self.assentamento:  # Só adiciona o QTabWidget se houver assentamento
            # --- NEW: Tab Widget para Occupation, Economy (e futuramente Armed Forces popup) ---
            tabs_group = QGroupBox("Settlement")
            tabs_layout = QVBoxLayout(tabs_group)

            self.tabs_widget = QTabWidget()

            # --- Adiciona abas (exceto Armed Forces) ---
            self._setup_tabs_ui()  # Esta função agora deve conter apenas Occupation e Economy

            tabs_layout.addWidget(self.tabs_widget)

            # Adiciona o grupo (com abas) ao layout da coluna direita
            right_column_layout.addWidget(tabs_group)

        # Adiciona o layout da coluna direita ao layout horizontal com fator de estiramento 2
        content_split_layout.addLayout(right_column_layout, 3)  # 3 partes

        # Adiciona o layout horizontal ao layout principal
        main_layout.addLayout(content_split_layout)

        # --- Close Button (Positioned Top Right) ---
        # Create a horizontal layout just for the close button
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch()  # Add a stretchable space to push the button to the right

        self.btn_close = QPushButton("Close")  # Changed text to English
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
        self.btn_close.clicked.connect(self.close)  # Connect close signal
        close_button_layout.addWidget(self.btn_close)  # Add button to the right-aligned layout

        main_layout.addLayout(close_button_layout)  # Add the button layout to the main layout
        print("✅ [DEBUG] setup_ui concluído") # <-- DEBUG

    def _setup_tabs_ui(self):
        """Configura as abas da interface: Occupation, Economy."""
        print("🎨 [DEBUG] Iniciando _setup_tabs_ui") # <-- DEBUG
        # --- Aba: Occupation ---
        occupation_page = QWidget()
        occupation_layout = QVBoxLayout(occupation_page)

        # --- Subdivisão: Novos Homens ---
        new_men_group = QGroupBox("New Men Allocation")
        new_men_group_layout = QVBoxLayout(new_men_group)

        # Cria o combo para homens
        self.new_men_combo = QComboBox()
        self.new_men_combo.addItems(["Farm", "Mine", "Armed Forces"])
        # Layout para agrupar combo e ícone (VERTICAL - ícone abaixo do combo)
        men_combo_icon_layout = QVBoxLayout()
        men_combo_icon_layout.addWidget(self.new_men_combo)
        men_combo_icon_layout.addWidget(self.men_allocation_icon_label)
        new_men_group_layout.addLayout(men_combo_icon_layout)

        # --- Subdivisão: Novas Mulheres ---
        new_women_group = QGroupBox("New Women Allocation")
        new_women_group_layout = QVBoxLayout(new_women_group)

        # Cria o combo para mulheres
        self.new_women_combo = QComboBox()
        self.new_women_combo.addItems(["Home", "Farm", "Mine"])
        print(f"   - Combo de mulheres criado com itens: {self.new_women_combo.count()} itens") # <-- DEBUG
        # Layout para agrupar combo e ícone (VERTICAL - ícone abaixo do combo)
        women_combo_icon_layout = QVBoxLayout()
        women_combo_icon_layout.addWidget(self.new_women_combo)
        women_combo_icon_layout.addWidget(self.women_allocation_icon_label)
        print(f"   - Label de ícone de mulheres adicionado ao layout: {self.women_allocation_icon_label}") # <-- DEBUG
        new_women_group_layout.addLayout(women_combo_icon_layout)

        # --- Ajuste de Tamanho: Limitar tamanho dos grupos e seus conteúdos ---
        # Definir tamanho fixo ou máximo para os grupos
        # Exemplo: (Largura, Altura) - Ajuste os valores conforme necessário
        tamanho_max_grupo = (200, 150) # Largura e altura máximas desejadas (ajuste estes valores)
        new_men_group.setMaximumSize(tamanho_max_grupo[0], tamanho_max_grupo[1])
        new_women_group.setMaximumSize(tamanho_max_grupo[0], tamanho_max_grupo[1])

        # Opcional: Definir tamanho fixo para os grupos (mais rígido)
        # new_men_group.setFixedSize(tamanho_max_grupo[0], tamanho_max_grupo[1])
        # new_women_group.setFixedSize(tamanho_max_grupo[0], tamanho_max_grupo[1])

        # Opcional: Limitar também o QLabel dos ícones se estiverem esticando demais
        # Exemplo: (Largura, Altura) - Ajuste os valores conforme necessário
        tamanho_max_icone = (100, 100) # Largura e altura máximas desejadas (ajuste estes valores)
        self.men_allocation_icon_label.setMaximumSize(tamanho_max_icone[0], tamanho_max_icone[1])
        self.women_allocation_icon_label.setMaximumSize(tamanho_max_icone[0], tamanho_max_icone[1])

        # Opcional: Definir tamanho fixo para os ícones (mais rígido)
        # self.men_allocation_icon_label.setFixedSize(tamanho_max_icone[0], tamanho_max_icone[1])
        # self.women_allocation_icon_label.setFixedSize(tamanho_max_icone[0], tamanho_max_icone[1])
        # --- Fim Ajuste de Tamanho ---


        # Adiciona os grupos ao layout principal da aba Occupation
        # Agora eles terão limites de tamanho
        occupation_layout.addWidget(new_men_group)
        occupation_layout.addWidget(new_women_group)

        # Adiciona a aba Occupation ao QTabWidget principal
        self.tabs_widget.addTab(occupation_page, "Occupation")

        # --- Aba: Economy ---
        economy_page = QWidget()
        economy_layout = QVBoxLayout(economy_page)
        economy_info_label = QLabel("Economy Information will be displayed here.")
        economy_info_label.setWordWrap(True)
        economy_layout.addWidget(economy_info_label)
        self.tabs_widget.addTab(economy_page, "Economy")
        print("✅ [DEBUG] _setup_tabs_ui concluído") # <-- DEBUG

    def _on_new_men_combo_changed(self, text):
        """Chama a janela de configuração de parâmetros militares se 'Armed Forces' for selecionado."""
        if text == "Armed Forces":
            # Nova Lógica: Abrir nova janela/popup de configuração de parâmetros
            self._abrir_janela_configuracao_militar_homens()
        # Salva a seleção no objeto assentamento
        self._salvar_selecao_homens_no_assentamento(text)

    def _salvar_selecao_mulheres_no_assentamento(self, texto_selecionado):
        """Salva a seleção de alocação de mulheres no objeto assentamento."""
        if not self.assentamento:
            print("⚠️ [JanelaInformacaoRegiao] _salvar_selecao_mulheres_no_assentamento: Nenhum assentamento para salvar seleção.")
            return

        # Garante que o dicionário 'alocacoes' exista no assentamento
        if not hasattr(self.assentamento, 'alocacoes'):
            self.assentamento.alocacoes = {}
        # Salva a seleção no dicionário
        self.assentamento.alocacoes['mulheres'] = texto_selecionado
        print(f"💾 [JanelaInformacaoRegiao] Seleção de mulheres salva no assentamento: {texto_selecionado}")

    def _salvar_selecao_mulheres_no_assentamento(self, texto_selecionado):
        """Salva a seleção de alocação de mulheres no objeto assentamento."""
        if not self.assentamento:
            print("⚠️ [JanelaInformacaoRegiao] _salvar_selecao_mulheres_no_assentamento: Nenhum assentamento para salvar seleção.")
            return

        # Garante que o dicionário 'alocacoes' exista no assentamento
        if not hasattr(self.assentamento, 'alocacoes'):
            self.assentamento.alocacoes = {}
        # Salva a seleção no dicionário
        self.assentamento.alocacoes['mulheres'] = texto_selecionado
        print(f"💾 [JanelaInformacaoRegiao] Seleção de mulheres salva no assentamento: {texto_selecionado}")

    def _on_new_women_combo_changed(self, text):
        """Ação ao mudar a seleção de alocação de mulheres."""
        print(f"🔄 [DEBUG] _on_new_women_combo_changed chamado com texto: '{text}'") # <-- DEBUG
        # Salva a seleção no objeto assentamento
        self._salvar_selecao_mulheres_no_assentamento(text)
        # Opcional: Aqui você pode adicionar outras lógicas que devem ocorrer ao mudar a seleção
        # print(f"🔄 [JanelaInformacaoRegiao] Seleção de mulheres mudou para: {text}")

    def _abrir_janela_configuracao_militar_homens(self):
        """Abre o popup de configuração de parâmetros da unidade militar."""
        print("🔧 [DEBUG] Janela de configuração de parâmetros militares para homens acionada.")

        if not self.assentamento:
            print("⚠️ [DEBUG] Nenhum assentamento selecionado para configuração militar.")
            return # Não pode abrir sem um assentamento

        # Cria e exibe o diálogo de configuração
        dialog = MilitaryUnitConfigDialog(self.assentamento, parent=self) # Passa o assentamento e o parent
        if dialog.exec() == QDialog.DialogCode.Accepted:
            print("✅ [DEBUG] Configuração de parâmetros militares salva com sucesso.")
            # Opcional: Atualizar algum label ou informação na janela principal
            # Ex: self.label_tipo_unidade_militar.setText(f"Type: {self.assentamento.tipo_unidade_militar_padrao}")
        else:
            print("ℹ️ [DEBUG] Configuração de parâmetros militares cancelada.")

    def _on_configure_men_role_clicked(self):
        """Chamado quando o botão de configuração de papel militar de homens é clicado."""
        print("🔧 [DEBUG] Configuração de papel militar para homens acionada.")
        # Futura lógica: abrir janela de configuração com self.assentamento.alocacao_novos_homens_params

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

        print(
            f"🔍 [JanelaInformacaoRegiao] Loading data for settlement of '{self.assentamento.civilizacao.nome}' on parcel {self.assentamento.indice_parcela} of tile {self.assentamento.coordenadas_tile}.")

        # --- Obter dados reais do assentamento ---
        populacao_total = self.assentamento.get_populacao_total()
        producao = self.assentamento.get_producao_real()

        # --- Atualizar informações básicas ---
        info_text_content = (
            f"Civilization: {self.assentamento.civilizacao.nome}\n"
            f"Parcel on Tile: {self.assentamento.indice_parcela}\n"
            f"Tile Coordinates: {self.assentamento.coordenadas_tile}\n"
            f"Total Population: {populacao_total}\n"
            f"Estimated Production: {producao:.2f}\n"
        )
        # Verifica se o widget de texto ainda é válido antes de usar
        # (Embora raro, é bom ser consistente se estamos fazendo para outros widgets)
        if hasattr(self, 'info_settlement_text') and self.info_settlement_text:
            try:
                # Qualquer operação no widget C++ pode levantar RuntimeError se ele foi deletado
                self.info_settlement_text.setPlainText(info_text_content)
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(
                        f"⚠️ [load_settlement_data] info_settlement_text foi deletado pelo Qt. Ignorando atualização.")
                    return  # Sai, pois o widget principal da UI pode estar comprometido
                else:
                    raise  # Re-lança se for outro tipo de RuntimeError

        # --- NEW: Atualizar labels de alocação de civis (Farm, Mine, Home) ---
        # Agora lendo diretamente do assentamento
        # Adicionando verificações para os labels também, por segurança
        if hasattr(self, 'farm_men_label') and self.farm_men_label:
            try:
                self.farm_men_label.setText(f"Men: {self.assentamento.farm_homens}")
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(f"⚠️ [load_settlement_data] farm_men_label foi deletado pelo Qt. Ignorando atualização.")
                    return
                else:
                    raise
        if hasattr(self, 'farm_women_label') and self.farm_women_label:
            try:
                self.farm_women_label.setText(f"Women: {self.assentamento.farm_mulheres}")
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(f"⚠️ [load_settlement_data] farm_women_label foi deletado pelo Qt. Ignorando atualização.")
                    return
                else:
                    raise
        if hasattr(self, 'mine_men_label') and self.mine_men_label:
            try:
                self.mine_men_label.setText(f"Men: {self.assentamento.mine_homens}")
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(f"⚠️ [load_settlement_data] mine_men_label foi deletado pelo Qt. Ignorando atualização.")
                    return
                else:
                    raise
        if hasattr(self, 'mine_women_label') and self.mine_women_label:
            try:
                self.mine_women_label.setText(f"Women: {self.assentamento.mine_mulheres}")
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(f"⚠️ [load_settlement_data] mine_women_label foi deletado pelo Qt. Ignorando atualização.")
                    return
                else:
                    raise
        if hasattr(self, 'home_men_label') and self.home_men_label:
            try:
                self.home_men_label.setText(f"Men: {self.assentamento.home_homens}")
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(f"⚠️ [load_settlement_data] home_men_label foi deletado pelo Qt. Ignorando atualização.")
                    return
                else:
                    raise
        if hasattr(self, 'home_women_label') and self.home_women_label:
            try:
                self.home_women_label.setText(f"Women: {self.assentamento.home_mulheres}")
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e):
                    print(f"⚠️ [load_settlement_data] home_women_label foi deletado pelo Qt. Ignorando atualização.")
                    return
                else:
                    raise

        print("ℹ️ [load_settlement_data] Dados militares agora são gerenciados pelo popup 'Armed Forces'.")

    def _salvar_selecao_homens_no_assentamento(self, texto_selecionado):
        """Salva a seleção de alocação de homens no objeto assentamento."""
        if not self.assentamento:
            print("⚠️ [JanelaInformacaoRegiao] _salvar_selecao_homens_no_assentamento: Nenhum assentamento para salvar seleção.")
            return

        if not hasattr(self.assentamento, 'alocacoes'):
            self.assentamento.alocacoes = {}
        self.assentamento.alocacoes['homens'] = texto_selecionado
        print(f"💾 [JanelaInformacaoRegiao] Seleção de homens salva no assentamento: {texto_selecionado}")

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
