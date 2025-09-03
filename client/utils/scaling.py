# utils/scaling.py
from PyQt6.QtWidgets import QApplication

# Base DPI (assumimos 96 como padrão)
BASE_DPI = 96

# Fator de escala global
def get_scale_factor():
    screen = QApplication.primaryScreen()
    dpi = screen.logicalDotsPerInch()
    return dpi / BASE_DPI

# Funções de ajuda para dimensionamento
def scale(value: int) -> int:
    """Escalona um valor em pixels com base no DPI."""
    return int(value * get_scale_factor())

def scale_font(size: int) -> int:
    """Escalona tamanho de fonte (opcional: pode ser mais suave)."""
    return int(size * get_scale_factor())