CHAVE = "test"

def xor_criptografar(dados, chave):
    dados_bytes = dados.encode()
    chave_bytes = chave.encode()
    
    resultado = bytearray()

    for i in range(len(dados_bytes)):
        resultado.append(
            dados_bytes[i] ^ chave_bytes[i % len(chave_bytes)]
        )

    return bytes(resultado)


dado = input("Digite o dado para criptografar: ")

criptografado = xor_criptografar(dado, CHAVE)

with open("key.enc", "wb") as arquivo:
    arquivo.write(criptografado)

print("Arquivo key.enc gerado com sucesso!")