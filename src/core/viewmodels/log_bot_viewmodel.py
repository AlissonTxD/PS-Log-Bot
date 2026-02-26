import logging
import os

from src.core.models.descriptografador_model import Descriptografador,ArquivoFaltando
from src.core.models.json_model import JsonModel
from src.core.models.log_bot_model import LogBotModel
from discord.errors import LoginFailure

import threading
response = ""

class LogBotViewModel:
    def __init__(self):
        self.descriptografador = Descriptografador()
        self.cut_coords = None
        self.config = None
        self.log_bot = None
        self.thread_bot = None

    #----------------------- Descriptografia e Configuração -----------------------
    def descriptografar(self):
        global response
        try:
            response = self.descriptografador.verificar_acesso()
            self.config = {
                "token": response[0],
                "channel_id": response[1],
                "cut_coords": self.cut_coords,
                "testmode": False
            }
            return {"success": True}
        except ArquivoFaltando as e:
            return {"success": False, "erro": str(e)}
        except LoginFailure:
            return {"success": False, "erro": "Discord Key Invalida"}
        except Exception as e:
            return {"success": False, "erro": f"Erro desconhecido: {str(e)}"}
        
    #----------------------- Ativar Bot -----------------------
    def ativar_bot(self):
        self.config["cut_coords"] = self.cut_coords
        self.log_bot=LogBotModel(self.config)
        self.thread_bot = threading.Thread(target=self.log_bot.run,daemon=True)
        self.thread_bot.start()
        
    #----------------------- Parar Bot -----------------------
    def parar_bot(self):
        if self.log_bot:
            self.log_bot.stop()
            self.log_bot = None
            self.thread_bot = None
            logging.info("Bot parado com sucesso.")

    def get_json_config(self):
        json_model = JsonModel()
        return json_model.open_json()
    