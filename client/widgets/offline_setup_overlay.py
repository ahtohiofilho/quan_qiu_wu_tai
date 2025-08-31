# client/widgets/offline_setup_overlay.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal


class OfflineSetupOverlay(QWidget):
    """
    Overlay flutuante para configurar partida offline: escolher fator e bioma.
    Emite sinal `on_start(fator, bioma)` ao clicar em "Iniciar".
    """

    on_start = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.setup_ui()

    def setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(30, 30, 40, 220);
            border-radius: 16px;
            border: 1px solid #3498db;
            color: white;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Título
        title = QLabel("🎮 Modo Offline")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Formulário
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Fator
        fator_layout = QHBoxLayout()
        fator_label = QLabel("Fator:")
        fator_label.setStyleSheet("min-width: 80px;")
        self.spin_fator = QSpinBox()
        self.spin_fator.setMinimum(4)  # fator >= 4
        self.spin_fator.setMaximum(99)  # limite técnico alto
        self.spin_fator.setValue(4)  # valor inicial
        self.spin_fator.setAccelerated(True)  # rolagem rápida
        self.spin_fator.setStyleSheet("padding: 6px;")
        fator_layout.addWidget(fator_label)
        fator_layout.addWidget(self.spin_fator)
        form_layout.addLayout(fator_layout)

        # Bioma
        bioma_layout = QHBoxLayout()
        bioma_label = QLabel("Bioma:")
        bioma_label.setStyleSheet("min-width: 80px;")
        self.combo_bioma = QComboBox()
        biomas_permitidos = ["Meadow", "Forest", "Savanna", "Desert", "Hills", "Mountains"]
        self.combo_bioma.addItems(biomas_permitidos)
        self.combo_bioma.setCurrentText("Meadow")
        self.combo_bioma.setStyleSheet("padding: 6px;")
        bioma_layout.addWidget(bioma_label)
        bioma_layout.addWidget(self.combo_bioma)
        form_layout.addLayout(bioma_layout)

        layout.addLayout(form_layout)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_start = QPushButton("Iniciar")

        self.btn_cancel.clicked.connect(self.on_cancel)
        self.btn_start.clicked.connect(self.on_confirm)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_start)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Tamanho fixo
        self.setFixedSize(400, 300)

    def on_confirm(self):
        fator = self.spin_fator.value()
        bioma = self.combo_bioma.currentText()
        self.on_start.emit(fator, bioma)  # ✅ Emite o sinal
        self.hide()

    def on_cancel(self):
        if hasattr(self.parent(), 'on_offline_setup_canceled'):
            self.parent().on_offline_setup_canceled()
        self.hide()

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent_widget:
            x = (self.parent_widget.width() - self.width()) // 2
            y = (self.parent_widget.height() - self.height()) // 2
            self.move(x, y)