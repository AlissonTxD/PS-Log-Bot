from src.core.viewmodels.descriptografador_viewmodel import DescriptografadorViewModel


class View:
    
    def __init__(self):

        self.descrip = DescriptografadorViewModel()
        resposta = self.descrip.descriptografar()

        if resposta["success"]:
            print("Acesso Liberado")
        else:
            print(f"Erro {resposta["erro"]}")
            exit()
        self.__menu()

    def __menu(self):
        while True:
            print("1 - Ativar Bot")
            print("2 - Sair")

            option = input("Escolha uma opção: ")
            match option:
                case "1":
                    self.descrip.ativar_bot()
                case "2":
                    print("Adeus")
                    exit()
                case _:
                    print("invalid")
