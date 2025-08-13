# server/interface.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton,
    QComboBox, QSpinBox, QMessageBox, QFormLayout, QGroupBox,
    QFileDialog
)
from server.serialization import Serializador
from server.manager import Gerenciador
from server.aws_loader import AWSLoader


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Servidor - Global Arena")
        self.setGeometry(100, 100, 700, 500)

        # === Inicialização do Gerenciador ===
        try:
            self.aws_loader = AWSLoader()
            self.gerenciador = Gerenciador(self.aws_loader)
            print("✅ Gerenciador inicializado com AWS.")
        except Exception as e:
            QMessageBox.critical(self, "Erro AWS", f"Não foi possível conectar à AWS:\n{e}")
            self.gerenciador = None

        # ✅ Armazena o último mundo criado (inicialmente None)
        self.ultimo_mundo = None

        # Configuração do sistema de abas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Criação das abas
        self.backup_tab = self.create_backup_tab()
        self.config_tab = QWidget()
        self.tabs.addTab(self.backup_tab, "Backup & Criação")
        self.tabs.addTab(self.config_tab, "Configurações")

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

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def handle_save_json(self):
        """Cria um mundo com os parâmetros da UI e salva localmente."""
        if not self.gerenciador:
            QMessageBox.critical(self, "Erro", "Gerenciador não está disponível.")
            return

        fator = self.spin_fator.value()
        bioma = self.combo_bioma.currentText()

        try:
            # 1. Criar mundo usando o Gerenciador
            mundo = self.gerenciador.criar_mundo(fator, bioma)

            # 2. Escolher caminho com diálogo
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Mundo como JSON",
                f"saves/mundo_{mundo.id_mundo}.json",
                "JSON Files (*.json)"
            )
            if not filepath:
                return  # Cancelado pelo usuário

            # 3. Salvar usando Serializador.save_mundo (já trata diretórios)
            caminho_salvo = Serializador.save_mundo(mundo, filepath)

            if caminho_salvo:
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Mundo salvo com sucesso!\nArquivo: {caminho_salvo}",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self,
                    "Falha",
                    "Erro ao salvar o arquivo JSON.",
                    QMessageBox.StandardButton.Ok
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Falha ao salvar: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def handle_criar_e_upload(self):
        """Manipula a criação e upload de um novo mundo"""
        if not self.gerenciador:
            QMessageBox.critical(self, "Erro", "Gerenciador não está disponível.")
            return

        fator = self.spin_fator.value()
        bioma = self.combo_bioma.currentText()

        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"Criar e enviar um novo mundo?\nFator: {fator}\nBioma: {bioma}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            print(f"🔄 Criando e enviando mundo com fator={fator}, bioma='{bioma}'...")
            sucesso, mundo = self.gerenciador.criar_e_upload_mundo_com_retorno(fator=fator, bioma=bioma)

            if sucesso:
                self.ultimo_mundo = mundo  # Armazena para possível salvamento local
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Mundo criado e enviado com sucesso!\nID: {mundo.id_mundo}",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self,
                    "Falha",
                    "O upload falhou. Veja o log para detalhes.",
                    QMessageBox.StandardButton.Ok
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao criar/upload do mundo:\n{str(e)}",
                QMessageBox.StandardButton.Ok
            )
            print(f"❌ Erro em handle_criar_e_upload: {e}")


# Execução da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec())