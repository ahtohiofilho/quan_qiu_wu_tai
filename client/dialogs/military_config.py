# --- client/dialogs/military_config_dialog.py ---
# Atualizado para novos tipos e configurações mínimas
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QDialogButtonBox, QGroupBox, QGridLayout, QSpinBox
)
from PyQt6.QtCore import Qt # Importe Qt para setReadOnly
from shared.unit import Unidade # Importa a classe base Unidade

class MilitaryUnitConfigDialog(QDialog):
    def __init__(self, assentamento, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Military Unit Type")
        self.setModal(True)
        self.assentamento = assentamento # Referência ao assentamento para salvar configurações

        # Dicionário com as configurações mínimas para cada tipo
        self.configuracoes_minimas = {
            "Infantry": (1, 1, 1, 1, 1), # (ataque, defesa, vida, alcance, movimento)
            "Mechanized": (1, 3, 2, 1, 3),
            "Naval": (2, 1, 2, 1, 2),
            "Aerial": (3, 1, 3, 1, 4)
        }

        self.layout = QVBoxLayout(self)

        # --- Título ---
        title_label = QLabel("Configure Default Military Unit Parameters for New Recruits:")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        self.layout.addWidget(title_label)

        # --- Parâmetros da Unidade ---
        unit_group = QGroupBox("Unit Parameters")
        unit_layout = QGridLayout(unit_group)

        # --- Spin Boxes para os parâmetros ---
        # Definindo limites razoáveis para os spin boxes
        max_value = 999 # Valor máximo para os parâmetros numéricos

        self.ataque_spin = QSpinBox()
        self.ataque_spin.setRange(1, max_value)
        self.ataque_spin.setValue(1) # Valor padrão
        # Conectar a mudança de valor para recalcular o custo
        self.ataque_spin.valueChanged.connect(self._calcular_custo)

        self.defesa_spin = QSpinBox()
        self.defesa_spin.setRange(1, max_value)
        self.defesa_spin.setValue(1) # Valor padrão
        # Conectar a mudança de valor para recalcular o custo
        self.defesa_spin.valueChanged.connect(self._calcular_custo)

        self.vida_spin = QSpinBox()
        self.vida_spin.setRange(1, max_value)
        self.vida_spin.setValue(1) # Valor padrão
        # Conectar a mudança de valor para recalcular o custo
        self.vida_spin.valueChanged.connect(self._calcular_custo)

        self.alcance_spin = QSpinBox()
        self.alcance_spin.setRange(1, max_value)
        self.alcance_spin.setValue(1) # Valor padrão
        # Conectar a mudança de valor para recalcular o custo
        self.alcance_spin.valueChanged.connect(self._calcular_custo)

        self.movimento_spin = QSpinBox()
        self.movimento_spin.setRange(1, max_value)
        self.movimento_spin.setValue(1) # Valor padrão
        # Conectar a mudança de valor para recalcular o custo
        self.movimento_spin.valueChanged.connect(self._calcular_custo)

        # --- Custo (Calculado automaticamente) ---
        self.custo_spin = QSpinBox()
        self.custo_spin.setRange(1, max_value * 5) # Ajuste o máximo conforme necessário, baseado na fórmula
        self.custo_spin.setValue(1) # Valor inicial, será recalculado
        self.custo_spin.setReadOnly(True) # Torna o campo de custo somente leitura
        # Não conectamos valueChanged para custo, pois ele é calculado, não definido

        # --- Tipo de Unidade (ComboBox com novos tipos) ---
        self.tipo_combo = QComboBox()
        # Adiciona os novos tipos
        self.tipo_combo.addItems(["Infantry", "Mechanized", "Naval", "Aerial"])
        # Conectar a mudança de tipo para aplicar os valores mínimos
        self.tipo_combo.currentTextChanged.connect(self._aplicar_valores_minimos_tipo)

        # --- Layout dos Spin Boxes ---
        row = 0
        unit_layout.addWidget(QLabel("Attack:"), row, 0)
        unit_layout.addWidget(self.ataque_spin, row, 1)
        row += 1
        unit_layout.addWidget(QLabel("Defense:"), row, 0)
        unit_layout.addWidget(self.defesa_spin, row, 1)
        row += 1
        unit_layout.addWidget(QLabel("Health:"), row, 0)
        unit_layout.addWidget(self.vida_spin, row, 1)
        row += 1
        unit_layout.addWidget(QLabel("Range:"), row, 0)
        unit_layout.addWidget(self.alcance_spin, row, 1)
        row += 1
        unit_layout.addWidget(QLabel("Movement:"), row, 0)
        unit_layout.addWidget(self.movimento_spin, row, 1)
        row += 1
        unit_layout.addWidget(QLabel("Cost:"), row, 0)
        unit_layout.addWidget(self.custo_spin, row, 1) # Agora é somente leitura
        row += 1
        unit_layout.addWidget(QLabel("Type:"), row, 0)
        unit_layout.addWidget(self.tipo_combo, row, 1)

        # Botões OK/Cancelar
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.layout.addWidget(unit_group)
        self.layout.addWidget(buttons)

        # Carrega a configuração anterior, se existir
        self._carregar_configuracao_atual()

    def _aplicar_valores_minimos_tipo(self, texto_tipo):
        """Aplica os valores mínimos para o tipo de unidade selecionado."""
        if texto_tipo in self.configuracoes_minimas:
            atq_min, def_min, vid_min, alc_min, mov_min = self.configuracoes_minimas[texto_tipo]

            # Verifica se o valor atual é menor que o mínimo exigido pelo tipo
            if self.ataque_spin.value() < atq_min:
                self.ataque_spin.setValue(atq_min)
            if self.defesa_spin.value() < def_min:
                self.defesa_spin.setValue(def_min)
            if self.vida_spin.value() < vid_min:
                self.vida_spin.setValue(vid_min)
            if self.alcance_spin.value() < alc_min:
                self.alcance_spin.setValue(alc_min)
            if self.movimento_spin.value() < mov_min:
                self.movimento_spin.setValue(mov_min)

            # O custo será recalculado automaticamente pelas conexões valueChanged dos spin boxes
            print(f"🔧 [MilitaryUnitConfigDialog] Valores mínimos aplicados para {texto_tipo}: A:{atq_min}, D:{def_min}, H:{vid_min}, R:{alc_min}, M:{mov_min}")


    def _calcular_custo(self):
        """Calcula o custo com base nos outros parâmetros."""
        ataque = self.ataque_spin.value()
        defesa = self.defesa_spin.value()
        vida = self.vida_spin.value()
        alcance = self.alcance_spin.value()
        movimento = self.movimento_spin.value()

        custo_calculado = (ataque + defesa + vida + alcance + movimento - 4) * 5
        # Garante que o custo não seja menor que 1
        custo_calculado = max(1, custo_calculado)

        self.custo_spin.setValue(custo_calculado) # Define o valor calculado no spin box


    def _carregar_configuracao_atual(self):
        """Carrega os parâmetros da unidade configurados anteriormente no assentamento."""
        # Tenta obter os parâmetros salvos no assentamento
        params = getattr(self.assentamento, 'params_unidade_militar', None)
        if params:
            print(f"🔧 [DEBUG] Carregando configuração anterior: {params}")
            # Carrega os valores dos parâmetros
            self.ataque_spin.setValue(params.get('ataque', 1))
            self.defesa_spin.setValue(params.get('defesa', 1))
            self.vida_spin.setValue(params.get('vida', 1))
            self.alcance_spin.setValue(params.get('alcance', 1))
            self.movimento_spin.setValue(params.get('movimento', 1))
            # O custo é calculado automaticamente, então não definimos diretamente
            tipo_atual = params.get('tipo', 'Infantry') # Valor padrão 'Infantry'
            index_tipo = self.tipo_combo.findText(tipo_atual)
            if index_tipo >= 0:
                self.tipo_combo.setCurrentIndex(index_tipo)
            else:
                print(f"⚠️ [DEBUG] Tipo '{tipo_atual}' não encontrado no combo, usando 'Infantry'.")
                self.tipo_combo.setCurrentText('Infantry')

            # Chama _calcular_custo após carregar os outros parâmetros
            # para atualizar o custo com base nos valores carregados
            self._calcular_custo()
        else:
            print("🔧 [DEBUG] Nenhuma configuração anterior encontrada, usando valores padrão (1).")
            # O custo será calculado automaticamente após os valores padrão serem definidos
            # Chamando _calcular_custo uma vez com os valores padrão (1, 1, 1, 1, 1)
            self._calcular_custo() # Custo inicial será (1+1+1+1+1-4)*5 = 1*5 = 5, mas como min é 1, será 5


    def get_current_unit_info(self):
        """Retorna um dicionário com os parâmetros atuais dos spin boxes e combo."""
        return {
            "nome": f"Custom_{self.ataque_spin.value()}_{self.defesa_spin.value()}_{self.vida_spin.value()}", # Nome genérico ou personalizado
            "ataque": self.ataque_spin.value(),
            "defesa": self.defesa_spin.value(),
            "vida": self.vida_spin.value(),
            "alcance": self.alcance_spin.value(),
            "movimento": self.movimento_spin.value(),
            "custo": self.custo_spin.value(), # Pega o valor calculado
            "tipo": self.tipo_combo.currentText() # Pega o tipo selecionado
        }

    def accept(self):
        """Sobrescreve o método accept para salvar a configuração."""
        current_info = self.get_current_unit_info()
        if current_info:
            # Salva a configuração no objeto do assentamento
            # O nome pode ser genérico ou personalizado pelo jogador posteriormente
            self.assentamento.tipo_unidade_militar_padrao = current_info["nome"] # Pode-se usar outro nome se for personalizado
            self.assentamento.params_unidade_militar = current_info # Armazena todos os parâmetros
            print(f"🔧 [MilitaryUnitConfigDialog] Configuração salva: {current_info} para assentamento {self.assentamento.indice_parcela}")
        super().accept()
