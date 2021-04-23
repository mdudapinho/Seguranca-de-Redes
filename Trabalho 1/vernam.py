"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
##################################################################
"""

import random

vector = []

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
        f = open('./texto_aberto.txt', 'r').read()
    elif(file == 2):
        f = open('./texto_cifrado.txt', 'r').read()
    else:
        print("nenhum arquivo selecionado")
        f = "ERRO"
    return f

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

def GetCaracter(a):
    for i in range(0, len(vector)):
        if (ord(a) == vector[i]):
            return i
    return -1

def printVector():
    for i in range(0, len(vector)):
        print (i, chr(vector[i]))

def get_randomkey(text):
    key =[]
    for i in range(0, len(text)):
        key.append(random.randint(0, len(vector)))
    #print(key)
    return key

def Encrypt():
    print("Encrypting...")
    texto_aberto = ReadFile(1)
    print(texto_aberto)
    k = get_randomkey(texto_aberto)
    print("chave usada: ", k)

    new_text = ""
    index = 0
    for palavra in texto_aberto:
        for letra in palavra:
            if(letra != None):
                if(letra == " " or letra == "\n"):
                    newLetter = letra
                else:
                    newPosition = GetCaracter(letra)
                    if(newPosition != -1):
                        newPosition += k[index]
                        if(newPosition>=len(vector)):
                            newPosition -=len(vector)
                        newLetter = chr(vector[newPosition])
                    else:
                        newLetter = " "
                new_text += newLetter
            index +=1

    print(new_text)
    output = open("texto_cifrado.txt", "w")
    n = output.write(new_text)
    output.close()
    return k

def Decrypt(k):
    print("Decrypting...")

    texto_cifrado = ReadFile(2)
    print("texto_cifrado ")
    print(texto_cifrado)

    print("chave usada: ", k)

    new_text = ""
    index = 0
    for palavra in texto_cifrado:
        for letra in palavra:
            if(letra != None):
                if(letra == " " or letra == "\n"):
                    newLetter = letra
                else:
                    newPosition = GetCaracter(letra)
                    if(newPosition != -1):
                        newPosition -= k[index]
                        if(newPosition<0):
                            newPosition +=len(vector)
                        newLetter = chr(vector[newPosition])
                    else:
                        newLetter = " "
                new_text += newLetter
            index +=1

    print(new_text)
    output = open("texto_aberto.txt", "w")
    n = output.write(new_text)
    output.close()

def main():
    Vector()
    keyMaster = []
    end = False
    show_ = raw_input("Show Frequency Analasys? 1 - Yes / 2 - No \n")
    if(int(show_) == 1):
        show = True
    else:
        show = False

    while(not end):
        opt = raw_input("Choose: 1 - Encript / 2 - Decrypt / Other - Exit\n")

        if(int(opt) == 1):
            keyMaster = Encrypt()
        elif(int(opt) == 2):
            if(len(keyMaster) == 0):
                print("Sorry, please encryp the text first to generate de key")
            else:
                Decrypt(keyMaster)
        else:
            end = True

        if(show):
            print("-----ANALISE DE FREQUENCIA TEXTO ABERTO-----")
            Frequencias(ReadFile(1))
            print("-----ANALISE DE FREQUENCIA TEXTO ENCRIPTADO-----")
            Frequencias(ReadFile(2))


main()
