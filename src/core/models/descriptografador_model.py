import os
import logging

MAIN_KEY = "test"


class ArquivoFaltando(Exception):
    pass


class Descriptografador:

    def verificar_acesso(self):
        if not os.path.exists("key.enc"):
            logging.info("Arquivo de criptografia faltando")
            raise ArquivoFaltando("Arquivo de criptografia faltando")

        with open("key.enc", "rb") as arquivo:
            conteudo = arquivo.read()

        descriptografado = self.__descriptografar(conteudo)

        if descriptografado != None:
            logging.info("Senha válida")
            token, canal = descriptografado.split("canal")
            return (token, int(canal))
        else:
            logging.info("Senha inválida")
            raise ArquivoFaltando("Senha inválida")

    def __descriptografar(self, dados_bytes, chave=MAIN_KEY):
        chave_bytes = chave.encode()
        resultado = bytearray()

        for i in range(len(dados_bytes)):
            resultado.append(
                dados_bytes[i] ^ chave_bytes[i % len(chave_bytes)]
            )

        return resultado.decode("utf-8")
    
if __name__ == "__main__":
    pass
