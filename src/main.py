import logging
from sys import argv, exit
from PyQt5.QtWidgets import QApplication
from src.views.log_bot_view import ViewMain

from src.views.main_view import View


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def start():
    app = QApplication(argv)
    view = ViewMain()
    view.show()
    view.raise_()
    view.activateWindow()
    exit(app.exec_())
