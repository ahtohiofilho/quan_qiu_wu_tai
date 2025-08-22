# server/signals.py
from PyQt6.QtCore import QObject, pyqtSignal

class WorkerSignals(QObject):
    """
    Define sinais para comunicação segura com a thread da UI.
    Usado pelo Comandante para enviar feedback.
    """
    success = pyqtSignal(object)   # resultado
    error = pyqtSignal(str)        # mensagem de erro
    finished = pyqtSignal()        # operação concluída