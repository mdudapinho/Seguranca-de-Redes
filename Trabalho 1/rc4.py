import os

vector = []
decrypt = "openssl rc4 -d -in output.rc4 -out input.txt"
encrypt = "openssl rc4 -in ./texto_aberto.txt -out ./output.rc4"

def Vector():
    for x in range(48, 58):
        vector.append(x)
    for x in range(65, 91):
        vector.append(x)
    for x in range(97, 123):
        vector.append(x)

def Freq():
    freq = []
    for i in range(0, len(vector)):
        freq.append(0)
    return freq

def ReadFile(file):
    if(file == 1):
        f = open("./texto_aberto.txt", "r")
    elif(file == 2):
        f = open("./output.rc4", "r")
    return f

def GetCaracter(a):
    for i in range(0, len(vector)):
        if (ord(a) == vector[i]):
            return i
    return -1

def Frequencias(texto):
    freq = Freq()
    texto_cifrado = texto
    for palavra in texto_cifrado:
        for letra in palavra:
            if(letra != None and letra != " " and letra != "\n"):
                position = GetCaracter(letra)
                if(position != -1):
                    freq[position] += 1

    maior = 0
    for i in range(0, len(freq)):
        print(chr(vector[i]), freq[i])
        if(freq[i] > freq[maior]):
            maior = i

    print("Letra mais repetida: " + chr(vector[maior]) + " (" + str(freq[maior])+ " vezes)")

def Encrypt():
    print("Encripting...")
    os.system(encrypt)


def Decrypt():
    print("Decripting...")
    os.system(decrypt)


def main():
    Vector()
    Freq()
    end = False
    enc = False

    while(not end):
        opt = raw_input("Choose: 1 - Encript / 2 - Decrypt / Other - Exit\n")

        if(int(opt) == 1):
            Encrypt()
            enc = True
        elif(int(opt) == 2):
            if(not enc):
                print("Sorry, please encryp the text first to generate de key")
            else:
                Decrypt()
        else:
            end = True

    print("-----ANALISE DE FREQUENCIA TEXTO ABERTO-----")
    Frequencias(ReadFile(1))
    print("-----ANALISE DE FREQUENCIA TEXTO ENCRIPTADO-----")
    Frequencias(ReadFile(2))


main()
