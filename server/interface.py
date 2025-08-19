# server/interface.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton,
    QComboBox, QSpinBox, QMessageBox, QFormLayout, QGroupBox,
    QFileDialog
)
from server.signals import WorkerSignals
from server.serialization import Serializador
from server.manager import Gerenciador
from server.aws_loader import AWSLoader
from server.commander import Comandante


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Servidor - Global Arena")
        self.setGeometry(100, 100, 700, 500)

        # === Inicialização de dependências ===
        try:
            self.aws_loader = AWSLoader()
            self.gerenciador = Gerenciador(self.aws_loader)
            print("✅ Gerenciador inicializado com AWS.")
        except Exception as e:
            QMessageBox.critical(self, "Erro AWS", f"Não foi possível conectar à AWS:\n{e}")
            self.gerenciador = None

        # ✅ Inicializa o Comandante
        try:
            self.comandante = Comandante(self.gerenciador, self.aws_loader)
            self.comandante.iniciar()
            print("✅ Comandante iniciado.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao iniciar o Comandante:\n{e}")
            self.comandante = None

        # ✅ Cria e conecta os sinais
        self.setup_signals()

        # ✅ Armazena o último mundo criado
        self.ultimo_mundo = None

        # Configuração do sistema de abas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # ✅ Cria as abas
        self.backup_tab = self.create_backup_tab()
        self.config_tab = QWidget()
        self.tabs.addTab(self.backup_tab, "Backup & Criação")
        self.tabs.addTab(self.config_tab, "Configurações")

    def closeEvent(self, event):
        if self.comandante:
            self.comandante.parar()
        event.accept()

    def setup_signals(self):
        """Cria e conecta os sinais para comunicação segura."""
        self.signals = WorkerSignals()
        self.signals.success.connect(self.on_success)
        self.signals.error.connect(self.on_error)
        self.signals.finished.connect(self.on_finished)

    def on_success(self, resultado):
        sucesso, mundo = resultado
        if sucesso:
            self.ultimo_mundo = mundo
            QMessageBox.information(
                self, "Sucesso", f"Mundo {mundo.id_mundo} criado e enviado!"
            )
        else:
            QMessageBox.critical(self, "Falha", "Upload falhou.")

    def on_error(self, mensagem: str):
        QMessageBox.critical(self, "Erro", f"Falha: {mensagem}")

    def on_finished(self):
        print("✅ Operação concluída.")

    # ————————————————————————————————
    # Métodos para construção da UI
    # ————————————————————————————————

    def create_backup_tab(self):
        """Cria a aba de operações de backup e criação de mundos"""
        tab = QWidget()
        layout = QVBoxLayout()

        # === Grupo: Criar e Upload de Mundo ===
        group_criar = QGroupBox("Criar e Enviar Novo Mundo")
        form_layout = QFormLayout()

        self.spin_fator = QSpinBox()
        self.spin_fator.setMinimum(2)
        self.spin_fator.setMaximum(8)
        self.spin_fator.setValue(4)
        form_layout.addRow("Fator:", self.spin_fator)

        self.combo_bioma = QComboBox()
        biomas = ["Meadow", "Forest", "Savanna", "Desert", "Hills", "Mountains"]
        self.combo_bioma.addItems(biomas)
        self.combo_bioma.setCurrentText("Meadow")
        form_layout.addRow("Bioma Inicial:", self.combo_bioma)

        group_criar.setLayout(form_layout)
        layout.addWidget(group_criar)

        btn_upload = QPushButton("🌍 Criar e Enviar Mundo para Nuvem")
        btn_upload.clicked.connect(self.handle_criar_e_upload)
        layout.addWidget(btn_upload)

        layout.addSpacing(20)

        # === Grupo: Salvar Localmente ===
        group_local = QGroupBox("Salvar Estado Localmente")
        layout_local = QVBoxLayout()

        btn_save = QPushButton("💾 Salvar Estado como JSON (Local)")
        btn_save.clicked.connect(self.handle_save_json)
        layout_local.addWidget(btn_save)

        group_local.setLayout(layout_local)
        layout.addWidget(group_local)

        layout.addSpacing(20)

        # === Botão: Reinicializar Infraestrutura AWS ===
        btn_reiniciar = QPushButton("⚠️ Reinicializar Infraestrutura AWS")
        btn_reiniciar.setStyleSheet("""
            QPushButton {
                background-color: #a83232;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c03939;
            }
        """)
        btn_reiniciar.clicked.connect(self.handle_reinicializar_servidor)
        layout.addWidget(btn_reiniciar)
        layout.addSpacing(10)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def handle_save_json(self):
        """Salva o último mundo criado (se existir) como JSON local."""
        if not self.ultimo_mundo:
            QMessageBox.warning(self, "Aviso", "Nenhum mundo foi criado ainda.")
            return

        try:
            mundo = self.ultimo_mundo
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Mundo como JSON",
                f"saves/mundo_{mundo.id_mundo}.json",
                "JSON Files (*.json)"
            )
            if not filepath:
                return  # Cancelado

            caminho_salvo = Serializador.save_mundo(mundo, filepath)
            if caminho_salvo:
                QMessageBox.information(
                    self, "Sucesso", f"Mundo salvo localmente:\n{caminho_salvo}"
                )
            else:
                QMessageBox.critical(self, "Falha", "Erro ao salvar o arquivo.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar: {str(e)}")

    def handle_criar_e_upload(self):
        if not self.comandante:
            QMessageBox.critical(self, "Erro", "Comandante não está disponível.")
            return

        fator = self.spin_fator.value()
        bioma = self.combo_bioma.currentText()

        self.comandante.criar_e_upload_mundo(
            fator=fator,
            bioma=bioma,
            signals=self.signals
        )

    def handle_reinicializar_servidor(self):
        if not self.comandante:
            QMessageBox.critical(self, "Erro", "Comandante não está disponível.")
            return

        reply = QMessageBox.question(
            self,
            "⚠️ Reinicializar Infraestrutura",
            "Isso apagará TODOS os mundos e metadados no S3 e DynamoDB.\n"
            "Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.comandante.reinicializar_infra(
            confirmar=False,
            signals=self.signals
        )


# Execução da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec())