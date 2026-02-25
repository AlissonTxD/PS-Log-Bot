from src.core.viewmodels.log_bot_viewmodel import LogBotViewModel


class View:
    
    def __init__(self):

        self.log_view_model = LogBotViewModel()
        resposta = self.log_view_model.descriptografar()

        if resposta["success"]:
            print("Acesso Liberado")
        else:
            print(f"Erro {resposta['erro']}")
            exit()
        self.__menu()

    def __menu(self):
        while True:
            print("1 - Ativar Bot")
            print("2 - Sair")

            option = input("Escolha uma opção: ")
            match option:
                case "1":
                    self._sub_menu_1()
                case "2":
                    print("Adeus")
                    exit()
                case _:
                    print("invalid")

    def _sub_menu_1(self):
        while True:
            print("qual resolução do seu monitor?")
            print("1 - 1920x1080")
            print("2 - 2560x1440")
            print("3 - 3440x1440")
            option = input("Escolha uma opção: ")
            match option:
                case "1":
                    print("resolução indisponível no momento")
                    return
                case "2":
                    self.log_view_model.cut_coords = (1035, 283, 1500, 339)
                    self.log_view_model.ativar_bot()
                    return
                case "3":
                    self.log_view_model.cut_coords = (1475, 285, 1945, 339)
                    self.log_view_model.ativar_bot()
                case _:     print("invalid")