# client/dialogs/auth_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QTabWidget, QWidget, QFormLayout, QLineEdit,
    QDialogButtonBox, QMessageBox, QVBoxLayout
)
import requests


class DialogoAutenticacao(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Autenticação")
        self.setModal(True)
        self.resize(350, 200)

        layout_principal = QVBoxLayout(self)

        # Abas: Login e Registro
        self.abas = QTabWidget()  # Salvando como atributo para acesso futuro
        self.abas.addTab(self.criar_aba_login(), "Entrar")
        self.abas.addTab(self.criar_aba_registro(), "Registrar")
        layout_principal.addWidget(self.abas)

        # Botões comuns → AGORA salvo como atributo: self.buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.on_ok)
        self.buttons.rejected.connect(self.reject)
        layout_principal.addWidget(self.buttons)

    def criar_aba_login(self):
        widget = QWidget()
        layout = QFormLayout()

        self.username_login = QLineEdit()
        self.senha_login = QLineEdit()
        self.senha_login.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Usuário:", self.username_login)
        layout.addRow("Senha:", self.senha_login)
        widget.setLayout(layout)
        return widget

    def criar_aba_registro(self):
        widget = QWidget()
        layout = QFormLayout()

        self.username_registro = QLineEdit()
        self.senha_registro = QLineEdit()
        self.confirmar_senha = QLineEdit()

        self.senha_registro.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmar_senha.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Usuário:", self.username_registro)
        layout.addRow("Senha:", self.senha_registro)
        layout.addRow("Confirmar Senha:", self.confirmar_senha)
        widget.setLayout(layout)
        return widget

    def on_ok(self):
        """Chamado quando o botão OK é pressionado. Executa login ou registro conforme aba ativa."""
        aba_atual = self.abas.currentIndex()  # ✅ Acesso direto ao QTabWidget
        if aba_atual == 0:
            self.tentar_login()
        else:
            self.tentar_registro()

    def tentar_login(self):
        username = self.username_login.text().strip()
        password = self.senha_login.text()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Usuário e senha são obrigatórios.")
            return

        try:
            response = requests.post(
                "http://localhost:5000/auth/login",
                json={"username": username, "password": password}
            )
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                with open("session.txt", "w") as f:
                    f.write(username)
                QMessageBox.information(self, "Sucesso", f"Bem-vindo, {username}!")
                self.accept()  # Fecha o diálogo com sucesso
            else:
                QMessageBox.critical(self, "Erro", data.get("message", "Falha no login."))
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar ao servidor.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {e}")

    def tentar_registro(self):
        username = self.username_registro.text().strip()
        password = self.senha_registro.text()
        confirmar = self.confirmar_senha.text()

        if not username or not password or not confirmar:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return
        if password != confirmar:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem.")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres.")
            return

        try:
            response = requests.post(
                "http://localhost:5000/auth/registrar",
                json={"username": username, "password": password}
            )
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                QMessageBox.information(self, "Sucesso", "Conta criada com sucesso! Faça login.")
                # Podemos mudar para aba de login automaticamente
                self.parent().findChild(QTabWidget).setCurrentIndex(0)
                self.username_login.setText(username)
            else:
                QMessageBox.critical(self, "Erro", data.get("message", "Falha no registro."))
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar ao servidor.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {e}")