from src.core.models.descriptografador_model import Descriptografador,ArquivoFaltando
from src.core.models.log_bot_model import start
from discord.errors import LoginFailure

import threading
response = ""

class DescriptografadorViewModel:
    def __init__(self):
        self.descriptografador = Descriptografador()

    def descriptografar(self):
        global response
        try:
            response = self.descriptografador.verificar_acesso()
            return {"success": True}
        except ArquivoFaltando as e:
            return {"success": False, "erro": str(e)}
        except LoginFailure:
            return {"success": False, "erro": "Discord Key Invalida"}
        
    def ativar_bot(self):
        thread_bot = threading.Thread(target=start, args=(response,),daemon=True)
        thread_bot.start()
        