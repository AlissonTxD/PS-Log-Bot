from PyQt5.QtWidgets import QMainWindow, QPushButton, QCheckBox, QComboBox, QMessageBox
from PyQt5 import uic
import logging

from src.core.viewmodels.log_bot_viewmodel import LogBotViewModel


UI_PATH = "src/views/log_bot.ui"


class ViewMain(QMainWindow):
    def __init__(self):
        super(ViewMain, self).__init__()
        uic.loadUi(UI_PATH, self)
        self.log_view_model = LogBotViewModel()

        #----------------------- definindo os componentes da interface -----------------------
        self.btn_start = self.findChild(QPushButton, "btn_start")
        self.btn_stop = self.findChild(QPushButton, "btn_stop")
        self.checkBox = self.findChild(QCheckBox, "check_test")
        self.combobox = self.findChild(QComboBox, "combo_resolution")
        #----------------------- Conectando os botões -----------------------
        self.btn_start.clicked.connect(self.stat)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_stop.setEnabled(False)

        # ----------------------- Carregando as resoluções -----------------------
        dict_resolutions = self.log_view_model.get_json_config()
        for resolution, coords in dict_resolutions.items():
            self.combobox.addItem(resolution, coords)
        
        resposta = self.log_view_model.descriptografar()
        if resposta["success"]:
            logging.info("Acesso Liberado")
        else:
            logging.error(f"Erro {resposta['erro']}")
            self.popup_error(f"Erro {resposta['erro']}")
            exit()

    def popup_error(self, mensagem: str) -> None:
        """shows a popup with the given message.

        Args:
            mensagem (str): message to be shown.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(mensagem)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def stat(self):
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        print("Start button clicked")
        self.log_view_model.config["testmode"] = self.checkBox.isChecked()
        self.log_view_model.cut_coords = self.combobox.currentData()
        self.log_view_model.ativar_bot()

    def stop(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        print("Stop button clicked")
        self.log_view_model.parar_bot()
