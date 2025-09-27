# client/widgets/tile.py
import os
import math
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor, QPainter


class TileOverlay(QWidget):
    """
    Overlay flutuante para exibir a textura do bioma do tile e máscaras regionais ao passar o mouse.
    - Imagem centralizada com escala responsiva
    - Botão '✕' redondo no canto superior direito
    - Widget Regiao sobreposto à imagem para mostrar regiões ao passar o mouse
    - Centralizado fisicamente no widget de referência (OpenGLWidget)
    - Fecha com clique fora, no botão ou em ESC
    """
    closed = pyqtSignal()

    def __init__(self, mundo, parent=None):
        super().__init__(parent)
        self.mundo = mundo  # Referência ao mundo atual (Já estava correto)
        self.region_widget = None # Widget Regiao para máscaras (Já estava correto)
        self.image_label = QLabel("...") # QLabel para a imagem do bioma (Já estava correto)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.Popup |           # Fecha com clique fora
            Qt.WindowType.FramelessWindowHint  # Sem bordas
        )

        from client.utils.scaling import scale

        # === Layout principal (grid para posicionamento preciso) ===
        layout = QGridLayout(self)
        layout.setContentsMargins(scale(16), scale(16), scale(16), scale(16))
        layout.setSpacing(0)

        # --- Label da imagem ---
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: transparent;")

        # --- Botão fechar: apenas '✕' em círculo ---
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(scale(30), scale(30))
        self.btn_close.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(200, 50, 50, 200);
                color: white;
                border-radius: {scale(15)}px;
                font-size: {int(scale(18))}px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba(230, 70, 70, 220);
            }}
        """)
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.clicked.connect(self.close)

        # Adiciona widgets ao grid
        layout.addWidget(self.image_label, 0, 0)
        layout.addWidget(
            self.btn_close,
            0, 0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.setLayout(layout)

        # Estilo do fundo do overlay
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            border-radius: 16px;
        """)

        # Widget de referência para centralização
        self.reference_widget = None

        # Dicionário para armazenar QPixmap carregadas: chave = caminho_da_imagem, valor = QPixmap
        self.bandeira_pixmaps = {}

    def set_reference_widget(self, widget):
        """Define o widget de referência (ex: OpenGLWidget) para centralização."""
        self.reference_widget = widget

    def carregar_imagem(self, caminho_imagem, formato="hex_up", coords_tile_alvo=None): # Adiciona coords_tile_alvo
        from client.utils.scaling import scale
        from client.widgets.region import Regiao

        # --- Verificações iniciais ---
        if not os.path.exists(caminho_imagem):
            print(f"❌ Textura não encontrada: {caminho_imagem}")
            return

        # Verifica se o mundo e as civilizações estão carregados para acessar assentamentos e overlays
        # Correção: usar 'civs' em vez de 'civilizacoes'
        if coords_tile_alvo and (not self.mundo or not hasattr(self.mundo, 'civs')):
             print("⚠️ [TileOverlay] Mundo ou Civilizações ('civs') não carregadas, não é possível processar assentamentos.")
             coords_tile_alvo = None # Desativa a lógica de bandeira se o mundo/civs não estiver disponível

        pixmap = QPixmap(caminho_imagem)
        if pixmap.isNull():
            print("❌ QPixmap inválido.")
            return

        # --- Obter dimensões do widget de referência ---
        ref = self.reference_widget or self.parent()
        if not ref:
            max_w, max_h = 800, 600
        else:
            rect = ref.rect()
            max_w, max_h = rect.width(), rect.height()

        # === 🔽 LIMITES BASEADOS NA TELA ===
        target_size = int(min(max_w, max_h) * 1.0)
        MAX_SIZE_ALLOWED = int(min(max_w, max_h) * 0.85)
        MAX_SIZE_HARD = scale(700)
        target_size = min(target_size, MAX_SIZE_ALLOWED, MAX_SIZE_HARD)

        scaled_pixmap = pixmap.scaled(
            target_size,
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        # self.image_label.setPixmap(scaled_pixmap) # <-- Comentado temporariamente

        self.setMinimumSize(
            scaled_pixmap.width() + scale(32),
            scaled_pixmap.height() + scale(32)
        )

        # --- NOVO: Sobrepor Bandeiras no Bioma/Layout Central ---
        if coords_tile_alvo:
            print(f"🔍 [TileOverlay] Carregando assentamentos para tile {coords_tile_alvo} para sobreposição direta.")
            # Encontrar assentamentos no tile alvo
            assentamentos_no_tile = []
            for civ in self.mundo.civs: # <-- Itera pelas civilizações (civs)
                for assentamento in civ.assentamentos: # <-- Itera pelos assentamentos da civilização
                    if assentamento.coordenadas_tile == coords_tile_alvo: # <-- Verifica as coordenadas
                        assentamentos_no_tile.append(assentamento) # <-- Adiciona à lista se for do tile certo

            if assentamentos_no_tile:
                print(f"🖼️ [TileOverlay] {len(assentamentos_no_tile)} assentamento(s) encontrado(s) no tile {coords_tile_alvo}, sobrepondo bandeiras...")
                # Chama a função que desenha as bandeiras diretamente no pixmap do bioma/layout
                self._desenhar_bandeiras_no_bioma(scaled_pixmap, assentamentos_no_tile, formato)
            else:
                print(f"🟢 [TileOverlay] Nenhum assentamento encontrado no tile {coords_tile_alvo}.")

        # Define o pixmap (original ou modificado com bandeiras) no QLabel
        self.image_label.setPixmap(scaled_pixmap) # <-- Agora define o pixmap com ou sem bandeiras
        # --- FIM NOVO ---

        # ======= INTEGRAÇÃO DA REGIAO (color picking 2D para hover) =======
        # As cores no picking_path são usadas *internamente* pelo Regiao para detectar regiões.
        # O mapa de overlays define *o que é exibido* quando uma região é detectada (hover).

        # --- Picking path (arquivo invisível para detectar regiões) ---
        picking_path = f"assets/picking/{formato}.png"

        # --- Mapa de cor para as regiões (deve bater com as cores do arquivo de picking) ---
        region_color_map = {
            (255, 0, 0): "center",
            (0, 255, 0): "top",
            (255, 0, 255): "bottom",
            (127, 127, 127): "left",
            (127, 0, 127): "right",
            (1, 11, 111): "topleft",
            (0, 0, 255): "topright",
            (0, 255, 255): "bottomleft",
            (255, 255, 0): "bottomright"
        }

        # --- Carregar Overlays corretos para o formato atual (visíveis ao passar o mouse) ---
        # Supõe que mundo.ref.overlay_paths[formato] é um dicionário
        # mapeando nomes de regiões para caminhos de arquivos de overlay.
        try:
            # Carregar os pixmaps originais
            overlay_pixmaps_originais = {
                reg: QPixmap(path) for reg, path in self.mundo.ref.overlay_paths[formato].items()
            }
            print(f"🟢 [TileOverlay] {len(overlay_pixmaps_originais)} pixmaps de overlay originais carregados para formato '{formato}'.")
        except (AttributeError, KeyError) as e:
            print(f"⚠️ Erro ao carregar overlays para formato '{formato}': {e}. Usando dicionário vazio.")
            overlay_pixmaps_originais = {}

        # --- NOVO: Modificar Overlays com Bandeiras (se coords_tile_alvo for fornecido e mundo/civs carregados) ---
        # (Esta parte é opcional agora, pois as bandeiras principais estão no bioma)
        # Se você quiser *também* mostrar bandeiras no hover, mantenha esta lógica.
        # Caso contrário, pode removê-la ou simplificar.
        if coords_tile_alvo:
            print(f"🔍 [TileOverlay] Carregando assentamentos para tile {coords_tile_alvo} para overlays de hover (opcional).")
            # Encontrar assentamentos no tile alvo (já feito acima, poderia ser otimizado)
            assentamentos_no_tile_hover = []
            for civ in self.mundo.civs:
                for assentamento in civ.assentamentos:
                    if assentamento.coordenadas_tile == coords_tile_alvo:
                        assentamentos_no_tile_hover.append(assentamento)

            if assentamentos_no_tile_hover:
                print(f"🖼️ [TileOverlay] {len(assentamentos_no_tile_hover)} assentamento(s) encontrado(s) para overlays de hover, modificando...")
                # Chama a função que sobrepõe as bandeiras nos pixmaps de overlay
                # Passando a lista já filtrada de assentamentos
                overlay_pixmaps_modificados = self._sobrepor_bandeiras_nos_overlays(
                    overlay_pixmaps_originais,
                    assentamentos_no_tile_hover # <-- Passa a lista filtrada
                )
                # Usa os pixmaps modificados
                overlay_pixmaps_para_usar = overlay_pixmaps_modificados
            else:
                print(f"🟢 [TileOverlay] Nenhum assentamento encontrado para overlays de hover, usando originais.")
                # Usa os pixmaps originais
                overlay_pixmaps_para_usar = overlay_pixmaps_originais
        else:
            if not coords_tile_alvo:
                print("⚠️ [TileOverlay] Nenhuma coordenada de tile fornecida para overlays de hover, usando originais.")
            # Caso não haja coordenadas ou mundo/civs inválido, usa os originais
            overlay_pixmaps_para_usar = overlay_pixmaps_originais
        # --- FIM NOVO ---


        # Remove o widget anterior se existir (evita leaks e sobreposição)
        if self.region_widget:
            self.region_widget.setParent(None)
            self.region_widget.deleteLater()
            self.region_widget = None

        # Cria o novo widget Regiao sobre a image_label (tamanho igual à imagem exibida)
        # O Regiao usa picking_path e region_color_map internamente para color picking.
        # Ele exibe os pixmaps de overlay_pixmaps_para_usar conforme a região detectada (hover).
        self.region_widget = Regiao(picking_path, region_color_map, parent=self.image_label)
        print(f"🔵 [TileOverlay] Configurando Regiao com {len(overlay_pixmaps_para_usar)} overlays de hover.")
        self.region_widget.set_overlay_pixmaps(overlay_pixmaps_para_usar) # <-- Define os overlays de hover (modificados ou não)
        self.region_widget.setGeometry(0, 0, scaled_pixmap.width(), scaled_pixmap.height())

        # Garantir que o Regiao receba eventos de mouse (hover)
        # self.region_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # Opcional, já é False por padrão
        # self.region_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True) # Opcional, já é True no Regia

        self.region_widget.show()

    def _desenhar_bandeiras_no_bioma(self, pixmap_bioma, assentamentos_no_tile, formato_tile):
        """Desenha as bandeiras dos assentamentos diretamente no pixmap do bioma/layout."""
        if pixmap_bioma.isNull():
            print("⚠️ [TileOverlay] Pixmap do bioma é nulo, não é possível desenhar bandeiras.")
            return

        painter = QPainter(pixmap_bioma)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) # Opcional

        # --- Definir regiões aproximadas no pixmap do bioma/layout ---
        # Esta é a parte crucial. Vamos definir áreas fixas relativas ao pixmap
        # para representar a parcela central e as periféricas.
        # A imagem do bioma/layout é uma representação 2D estilizada.
        # Vamos usar proporções fixas para simplificar.
        # Supondo que a imagem tenha uma forma que represente bem um hexágono/pentágono.
        pixmap_w = pixmap_bioma.width()
        pixmap_h = pixmap_bioma.height()

        # Margens para evitar desenhar exatamente na borda
        margem_x = pixmap_w * 0.05
        margem_y = pixmap_h * 0.05
        area_w = pixmap_w - 2 * margem_x
        area_h = pixmap_h - 2 * margem_y

        # --- Mapeamento de parcela para região 2D no pixmap ---
        # Este mapeamento deve refletir a geometria descrita (hexágono/pentágono central, trapézios periféricos),
        # mas de forma simplificada para coordenadas 2D.
        # O formato_tile pode influenciar levemente a orientação, mas usaremos uma divisão genérica por enquanto.
        # O formato 'hex_up' e 'hex_side' provavelmente precisam de tratamento ligeiramente diferente
        # para mapear as direções periféricas corretamente, mas vamos começar com uma base comum.

        # Definir regiões fixas (x, y, w, h) para cada parcela
        # Supondo layout hexagonal de pé como base para as regiões
        regioes_parcelas = {}

        # Parcela Central (índice 0)
        regioes_parcelas[0] = {
            'x': pixmap_w / 2 - area_w * 0.2 / 2, # Aproximadamente 20% da largura da área
            'y': pixmap_h / 2 - area_h * 0.2 / 2, # Aproximadamente 20% da altura da área
            'w': area_w * 0.2,
            'h': area_h * 0.2
        }

        # Parcelas Periféricas (índices 1 a 6 para hexágono, 1 a 5 para pentágono)
        # Vamos mapear índices para direções aproximadas e calcular regiões
        # com base em divisões radiais ou trapézios em torno da área central.
        # Este é o ponto mais delicado e pode exigir ajustes visuais.
        # Usaremos divisões radiais em torno do centro para simplificar.
        # Índices periféricos: 1 (topo), 2 (topo-direita), 3 (baixo-direita),
        #                       4 (baixo), 5 (baixo-esquerda), 6 (topo-esquerda)
        num_parcelas_perifericas = 6 # Assume hexágono por padrão
        if formato_tile in ["pent_up", "pent_side"]: # Ajuste se os nomes forem diferentes
            num_parcelas_perifericas = 5

        angulo_inicio = -30 if formato_tile.startswith("hex") else -36 # Ajuste inicial para hex (e aprox pent)
        angulo_setor = 360 / num_parcelas_perifericas # 60 graus para hex, 72 para pent

        for i in range(1, num_parcelas_perifericas + 1):
            idx_parcela = i
            angulo_central = angulo_inicio + (idx_parcela - 1) * angulo_setor
            angulo_rad = math.radians(angulo_central)

            # Calcular centro da região periférica baseado em um raio proporcional
            # ao tamanho da área, fora da área central.
            raio_proporcional = (area_w + area_h) / 4 # Aproximadamente metade da média
            offset_x = math.cos(angulo_rad) * raio_proporcional
            offset_y = math.sin(angulo_rad) * raio_proporcional

            centro_x = pixmap_w / 2 + offset_x
            centro_y = pixmap_h / 2 + offset_y

            # Dimensões da região da bandeira
            regiao_w = area_w * 0.15 # Aprox 15% da largura da área total
            regiao_h = area_h * 0.15 # Aprox 15% da altura da área total

            regioes_parcelas[idx_parcela] = {
                'x': centro_x - regiao_w / 2,
                'y': centro_y - regiao_h / 2,
                'w': regiao_w,
                'h': regiao_h
            }

        # --- Iterar sobre os assentamentos e desenhar as bandeiras ---
        for assentamento in assentamentos_no_tile:
            regiao_dados = regioes_parcelas.get(assentamento.indice_parcela)

            if not regiao_dados:
                print(f"⚠️ [TileOverlay] Índice de parcela {assentamento.indice_parcela} não mapeado para região 2D no bioma.")
                continue # Pula este assentamento

            # --- Pegar a bandeira da civilização do assentamento ---
            civ = assentamento.civilizacao
            if not civ:
                 print(f"⚠️ [TileOverlay] Civilização não definida para assentamento em parcela {assentamento.indice_parcela}.")
                 continue

            # --- Construir o caminho da bandeira com base no nome da civilização e no ID do mundo ---
            # Verifica se o mundo e o ID do mundo estão disponíveis
            if not self.mundo or not hasattr(self.mundo, 'id_mundo'):
                 print(f"⚠️ [TileOverlay] ID do mundo não disponível para construir caminho da bandeira de {civ.nome}.")
                 continue

            # Supõe que o nome do arquivo da bandeira é '{civ.nome}.png'
            # e que ele está em 'assets/worlds/{id_mundo}/flags/'
            nome_arquivo_bandeira = f"{civ.nome}.png"
            caminho_bandeira = f"assets/worlds/{self.mundo.id_mundo}/flags/{nome_arquivo_bandeira}"

            print(f"   - Tentando caminho da bandeira para {civ.nome}: {caminho_bandeira}") # DEBUG

            # --- Verificar se o arquivo existe ---
            import os
            if not os.path.exists(caminho_bandeira):
                 print(f"❌ [TileOverlay] Arquivo da bandeira não encontrado: {caminho_bandeira}")
                 continue # Pula este assentamento

            # --- Carregar a imagem da bandeira ---
            pixmap_bandeira = QPixmap(caminho_bandeira)
            if pixmap_bandeira.isNull():
                 print(f"❌ [TileOverlay] Erro ao carregar imagem da bandeira (pixmap nulo): {caminho_bandeira}")
                 continue # Pula este assentamento

            print(f"   - Bandeira carregada com sucesso: {pixmap_bandeira.width()}x{pixmap_bandeira.height()} para parcela {assentamento.indice_parcela}") # DEBUG

            # --- Calcular posição e escala da bandeira dentro da região definida ---
            regiao_x = regiao_dados['x']
            regiao_y = regiao_dados['y']
            regiao_w = regiao_dados['w']
            regiao_h = regiao_dados['h']

            # Dimensões da bandeira
            bandeira_w = pixmap_bandeira.width()
            bandeira_h = pixmap_bandeira.height()

            # Calcular escala para caber na região com uma margem de segurança
            escala_fator = 0.8 # Por exemplo, 80% do tamanho da região
            max_largura = regiao_w * escala_fator
            max_altura = regiao_h * escala_fator

            proporcao = bandeira_w / bandeira_h
            if (max_largura / proporcao) <= max_altura:
                largura_final = max_largura
                altura_final = largura_final / proporcao
            else:
                altura_final = max_altura
                largura_final = altura_final * proporcao

            print(f"   - Dimensionando bandeira para região {assentamento.indice_parcela}: Original ({bandeira_w}x{bandeira_h}), Região ({regiao_w:.2f}x{regiao_h:.2f}), Escala ({largura_final:.2f}x{altura_final:.2f})") # DEBUG

            # Calcular coordenadas do canto superior esquerdo da bandeira
            # para centralizá-la dentro da região definida
            x_bandeira = regiao_x + (regiao_w - largura_final) / 2.0
            y_bandeira = regiao_y + (regiao_h - altura_final) / 2.0

            print(f"   - Posicionando bandeira em ({x_bandeira:.2f}, {y_bandeira:.2f})") # DEBUG

            # --- Desenhar a bandeira ---
            painter.drawPixmap(int(x_bandeira), int(y_bandeira), int(largura_final), int(altura_final), pixmap_bandeira)


        painter.end() # Sempre finalize o QPainter
        print(f"🖼️ [TileOverlay] Bandeiras desenhadas diretamente no pixmap do bioma/layout.")

    def _sobrepor_bandeiras_nos_overlays(self, overlay_pixmaps, assentamentos_no_tile): # Recebe a lista de assentamentos filtrada
        """Sobrepõe as bandeiras dos assentamentos nos pixmaps de overlay correspondentes."""
        # Dicionário para armazenar os pixmaps modificados
        pixmaps_modificados = {}

        # Mapeamento de índice de parcela para nome de região do overlay
        # Este mapeamento deve refletir como o arquivo de picking e o Regiao interpretam os índices.
        # Supondo que o Regiao use os nomes como "center", "top", "topleft", etc.
        # E que os índices de parcela sejam:
        # PARCELA_CENTRAL = 0
        # Parcelas Periféricas: 1 (topo), 2 (topo-direita), 3 (baixo-direita),
        #                       4 (baixo), 5 (baixo-esquerda), 6 (topo-esquerda)
        # Mapeamento padrão para HEXÁGONO (ajuste para PENTÁGONO se necessário)
        parcela_idx_para_regiao_nome = {
            0: "center", # Parcela Central
            1: "top",    # Parcela Periférica 1
            2: "topright", # Parcela Periférica 2
            3: "bottomright", # Parcela Periférica 3
            4: "bottom", # Parcela Periférica 4
            5: "bottomleft", # Parcela Periférica 5
            6: "topleft", # Parcela Periférica 6
        }

        # --- Constante para escala da bandeira no overlay de hover ---
        # Este valor define a proporção da área da região do overlay que a bandeira ocupará.
        # Ex: 0.6 significa que a bandeira tentará ocupar 60% da largura/altura da região disponível.
        ESCALA_BANDA_HOVER = 0.15 # <-- Ajuste este valor para aumentar/diminuir a escala relativa no hover
        # --- Fim Constante ---

        # --- Iterar sobre os assentamentos já filtrados ---
        for assentamento in assentamentos_no_tile:
            regiao_nome = parcela_idx_para_regiao_nome.get(assentamento.indice_parcela)

            if not regiao_nome:
                print(f"⚠️ [TileOverlay] Índice de parcela {assentamento.indice_parcela} não mapeado para região 2D.")
                continue # Pula este assentamento

            # --- Pegar o pixmap do overlay para esta região ---
            pixmap_overlay = overlay_pixmaps.get(regiao_nome)
            if not pixmap_overlay or pixmap_overlay.isNull():
                print(f"⚠️ [TileOverlay] Overlay para região '{regiao_nome}' não encontrado ou inválido.")
                continue # Pula este assentamento

            # --- Pegar a bandeira da civilização do assentamento ---
            civ = assentamento.civilizacao
            if not civ:
                 print(f"⚠️ [TileOverlay] Civilização não definida para assentamento em parcela {assentamento.indice_parcela}.")
                 continue

            # --- Construir o caminho da bandeira com base no nome da civilização e no ID do mundo ---
            # Verifica se o mundo e o ID do mundo estão disponíveis
            if not self.mundo or not hasattr(self.mundo, 'id_mundo'):
                 print(f"⚠️ [TileOverlay] ID do mundo não disponível para construir caminho da bandeira de {civ.nome}.")
                 continue

            # Supõe que o nome do arquivo da bandeira é '{civ.nome}.png'
            # e que ele está em 'assets/worlds/{id_mundo}/flags/'
            nome_arquivo_bandeira = f"{civ.nome}.png"
            caminho_bandeira = f"assets/worlds/{self.mundo.id_mundo}/flags/{nome_arquivo_bandeira}"

            print(f"   - Tentando caminho da bandeira para {civ.nome}: {caminho_bandeira}") # DEBUG

            # --- Verificar se o arquivo existe ---
            import os
            if not os.path.exists(caminho_bandeira):
                 print(f"❌ [TileOverlay] Arquivo da bandeira não encontrado: {caminho_bandeira}")
                 continue # Pula este assentamento

            # --- Carregar a imagem da bandeira ---
            pixmap_bandeira = QPixmap(caminho_bandeira)
            if pixmap_bandeira.isNull():
                 print(f"❌ [TileOverlay] Erro ao carregar imagem da bandeira (pixmap nulo): {caminho_bandeira}")
                 continue # Pula este assentamento

            print(f"   - Bandeira carregada com sucesso: {pixmap_bandeira.width()}x{pixmap_bandeira.height()}") # DEBUG

            # --- Preparar para desenhar ---
            # Se este pixmap_overlay ainda não foi modificado, usamos o original
            if regiao_nome not in pixmaps_modificados:
                # Cria uma cópia editável do pixmap original
                pixmap_editavel = pixmap_overlay.copy()
                print(f"   - Criando cópia editável do overlay '{regiao_nome}' ({pixmap_overlay.width()}x{pixmap_overlay.height()})") # DEBUG
            else:
                # Se já foi modificado por outro assentamento nesta mesma região (raro),
                # pegamos a versão já modificada para adicionar a nova bandeira.
                # Para simplificar, assumimos que NÃO haverá dois assentamentos na mesma parcela.
                # Se houver, a segunda bandeira sobrescreverá a primeira.
                pixmap_editavel = pixmaps_modificados[regiao_nome]
                print(f"   - Usando overlay já modificado para '{regiao_nome}'") # DEBUG

            painter = QPainter(pixmap_editavel)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing) # Opcional

            # --- Calcular posição e escala da bandeira dentro do pixmap_overlay ---
            # Esta é a parte mais importante e que precisa de ajuste fino.
            # As dimensões do pixmap_overlay representam a área 2D da parcela.
            overlay_w = pixmap_editavel.width()
            overlay_h = pixmap_editavel.height()

            # Dimensões da bandeira
            bandeira_w = pixmap_bandeira.width()
            bandeira_h = pixmap_bandeira.height()

            # Calcular escala para caber na área do overlay com uma margem de segurança
            # Usa a constante definida acima
            escala_fator = ESCALA_BANDA_HOVER # <-- Usa a constante
            max_largura = overlay_w * escala_fator
            max_altura = overlay_h * escala_fator

            proporcao = bandeira_w / bandeira_h
            if (max_largura / proporcao) <= max_altura:
                largura_final = max_largura
                altura_final = largura_final / proporcao
            else:
                altura_final = max_altura
                largura_final = altura_final * proporcao

            print(f"   - Dimensionando bandeira (hover): Original ({bandeira_w}x{bandeira_h}), Overlay ({overlay_w}x{overlay_h}), Escala Base ({escala_fator}), Escala ({largura_final:.2f}x{altura_final:.2f})") # DEBUG

            # Calcular coordenadas do canto superior esquerdo da bandeira
            # para centralizá-la dentro do pixmap_overlay
            x_bandeira = (overlay_w - largura_final) / 2.0
            y_bandeira = (overlay_h - altura_final) / 2.0

            print(f"   - Posicionando bandeira (hover) em ({x_bandeira:.2f}, {y_bandeira:.2f})") # DEBUG

            # --- Desenhar a bandeira ---
            painter.drawPixmap(int(x_bandeira), int(y_bandeira), int(largura_final), int(altura_final), pixmap_bandeira)
            painter.end()

            # --- Armazenar o pixmap modificado ---
            pixmaps_modificados[regiao_nome] = pixmap_editavel
            print(f"🖼️ [TileOverlay] Bandeira de {civ.nome} desenhada no overlay da região '{regiao_nome}' (Parcela {assentamento.indice_parcela}).")


        # --- Retornar o dicionário de pixmaps ---
        # Se um overlay não foi modificado, retornamos o original
        pixmaps_finais = overlay_pixmaps.copy() # Começa com os originais
        pixmaps_finais.update(pixmaps_modificados) # Atualiza com os modificados
        print(f"🔵 [TileOverlay] _sobrepor_bandeiras_nos_overlays retornando {len(pixmaps_finais)} pixmaps (originais + modificados).") # DEBUG
        return pixmaps_finais

    def show_centered(self):
        """Exibe o overlay com diagnóstico detalhado de posicionamento."""
        from PyQt6.QtWidgets import QApplication

        # --- 1. Obter janela principal ---
        app = QApplication.instance()
        window = app.activeWindow()
        if not window:
            print("❌ [DEBUG - SHOW] Nenhuma janela ativa encontrada.")
            return
        else:
            print(f"✅ [DEBUG - SHOW] Janela ativa: {window}")

        # --- 2. Obter geometria da área disponível (sem barra de tarefas) ---
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()
        print(f"📏 [DEBUG - SHOW] availableGeometry(): {screen_rect}")

        center_x = screen_rect.center().x()
        center_y = screen_rect.center().y()
        print(f"🎯 [DEBUG - SHOW] Centro absoluto da tela: ({center_x}, {center_y})")

        # --- 3. Tamanho do overlay ---
        self.adjustSize()
        w, h = self.width(), self.height()
        print(f"🖼️ [DEBUG - SHOW] Tamanho calculado do overlay: {w}x{h}")

        # --- 4. Posição final ---
        x = center_x - w // 2
        y = center_y - h // 2
        print(f"📌 [DEBUG - SHOW] Posição final calculada: ({x}, {y})")

        # --- 5. Informações adicionais para depuração visual ---
        print(f"🔍 [DEBUG - SHOW] Altura total da tela física: {screen.geometry().height()}")
        print(f"🔍 [DEBUG - SHOW] Margem superior (barra de tarefas?): {screen.geometry().top()}")
        print(f"🔍 [DEBUG - SHOW] Margem inferior estimada: {screen.geometry().bottom() - screen_rect.bottom()}")

        # --- 6. Aplicar posição ---
        self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()
        print(f"✅ [DEBUG - SHOW] Overlay mostrado em ({x}, {y}), tamanho {w}x{h}")

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        """Fecha o overlay ao pressionar ESC."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)