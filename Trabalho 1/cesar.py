"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
##################################################################
"""

vector = []

#Sequence (0-9,A-Z,a-z)
def Vector():
    for x in range(48, 58):
        vector.append(x)
    for x in range(65, 91):
        vector.append(x)
    for x in range(97, 123):
        vector.append(x)

def ReadFile(file):
    if(file == 1):
        f = open("./texto_aberto.txt", "r")
    elif(file == 2):
        f = open("./texto_cifrado.txt", "r")
    else:
        print("nenhum arquivo selecionado")
        f = "ERRO"
    return f

def GetCaracter(a):
    for i in range(0, len(vector)):
        if (ord(a) == vector[i]):
            return i
    return -1

def printVector():
    for i in range(0, len(vector)):
        print (i, chr(vector[i]))

def Encrypt(k):
    print("Encripting...")
    texto_aberto = ReadFile(1)
    new_text = ""
    for palavra in texto_aberto:
        for letra in palavra:
            if(letra != None):
                #print("letra", letra)
                if(letra == " " or letra == "\n"):
                    newLetter = letra
                else:
                    newPosition = GetCaracter(letra)
                    if(newPosition != -1):
                        newPosition += k
                        if(newPosition>=len(vector)):
                            newPosition -=len(vector)
                        newLetter = chr(vector[newPosition])
                    else:
                        newLetter = " "

                #print("newLetter", newLetter)
                new_text += newLetter
    print(new_text)
    output = open("texto_cifrado.txt", "w")
    n = output.write(new_text)
    output.close()

def Decrypt(k):
    print("Decripting...")
    texto_cifrado = ReadFile(2)
    new_text = ""
    for palavra in texto_cifrado:
        for letra in palavra:
            if(letra != None):
                #print("letra", letra)
                if(letra == " " or letra == "\n"):
                    newLetter = letra
                else:
                    newPosition = GetCaracter(letra)
                    if(newPosition != -1):
                        newPosition -= k
                        if(newPosition<0):
                            newPosition +=len(vector)
                        newLetter = chr(vector[newPosition])
                    else:
                        newLetter = " "

                #print("newLetter", newLetter)
                new_text += newLetter
    print(new_text)
    output = open("texto_aberto.txt", "w")
    n = output.write(new_text)
    output.close()

def main():
    Vector()
    end = False
    string = "Choose k (1 - " + str(len(vector)) + ")\n"
    while(not end):
        opt = int(raw_input("Choose: 1-Encript / 2-Decrypt\n"))

        if(opt == 1 or opt == 2):
            k = int(raw_input(string))
            if(k<0 or k>len(vector)):
                print("k out of index")
            else:
                if(opt == 1):
                    Encrypt(k)
                elif(opt == 2):
                    Decrypt(k)

        else:
            end = True

main()
