# server/admin_gui.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QComboBox, QSpinBox, QMessageBox, QFormLayout, QGroupBox,
    QFileDialog, QTextEdit, QPushButton
)
from server.config.signals import WorkerSignals
from server.serialization import Serializador
from server.core.manager import Gerenciador
from server.integrations.aws_loader import AWSLoader
from server.core.commander import Comandante


class ServerAdminGUI(QMainWindow):
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
        """Trata diferentes tipos de sucesso: criação de mundo ou mensagens de log."""
        if isinstance(resultado, tuple):
            # Caso 1: resultado de upload de mundo (sucesso, mundo)
            try:
                sucesso, mundo = resultado
                if sucesso:
                    self.ultimo_mundo = mundo
                    QMessageBox.information(
                        self, "Sucesso", f"Mundo {mundo.id_mundo} criado e enviado!"
                    )
                else:
                    QMessageBox.critical(self, "Falha", "Upload falhou.")
            except Exception as e:
                print(f"❌ Erro ao processar resultado de upload: {e}")
        else:
            # Caso 2: mensagem de log (ex: simulação de players)
            self.log_output.append(f"🟢 {resultado}")  # Exibe no widget de log
            print(f"🟢 {resultado}")  # Também imprime no terminal

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

        # === Grupo: Simulação de Players ===
        group_sim = QGroupBox("Simulação de Players Online")
        layout_sim = QVBoxLayout()

        btn_iniciar_sim = QPushButton("▶️ Iniciar Simulação de Players")
        btn_iniciar_sim.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; font-weight: bold; border-radius: 6px; padding: 8px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        btn_iniciar_sim.clicked.connect(self.handle_iniciar_simulacao)
        layout_sim.addWidget(btn_iniciar_sim)

        btn_parar_sim = QPushButton("⏹️ Parar Simulação de Players")
        btn_parar_sim.setStyleSheet("""
            QPushButton { background-color: #e74c3c; color: white; font-weight: bold; border-radius: 6px; padding: 8px; }
            QPushButton:hover { background-color: #c0392b; }
        """)
        btn_parar_sim.clicked.connect(self.handle_parar_simulacao)
        layout_sim.addWidget(btn_parar_sim)

        group_sim.setLayout(layout_sim)
        layout.addWidget(group_sim)

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

        # === Log de Atividades ===
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        self.log_output.setPlaceholderText("Log de atividades...")
        layout.addWidget(self.log_output)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def handle_iniciar_simulacao(self):
        """Inicia a simulação de players online."""
        if not self.comandante:
            QMessageBox.critical(self, "Erro", "Comandante não está disponível.")
            return
        self.comandante.iniciar_simulacao_players(signals=self.signals)

    def handle_parar_simulacao(self):
        """Para a simulação de players online."""
        if not self.comandante:
            return
        self.comandante.parar_simulacao_players()
        self.signals.success.emit("🛑 Simulação interrompida pelo usuário.")

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
    window = ServerAdminGUI()
    window.show()
    sys.exit(app.exec())