from src.core.models.descriptografador_model import Descriptografador,ArquivoFaltando
from src.core.models.log_bot_model import LogBotModel
from discord.errors import LoginFailure

import threading
response = ""

class LogBotViewModel:
    def __init__(self):
        self.descriptografador = Descriptografador()
        self.cut_coords = None
        self.config = None


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
        
    def ativar_bot(self):
        self.config["cut_coords"] = self.cut_coords
        logbot=LogBotModel(self.config)
        thread_bot = threading.Thread(target=logbot.run,daemon=True)
        thread_bot.start()
        