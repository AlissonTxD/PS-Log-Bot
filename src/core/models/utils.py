import sys
import os

def resource_path(relative_path):
    """Retorna caminho correto tanto em dev quanto em .exe"""
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)