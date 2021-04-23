"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
##################################################################
"""

vector = []
freq = []

text = "g5Bt5 t54yvtz3v4A5 wrG t53 7Bv r9 6v995r9 9v 9z4Ar3\n58xB2y59r9. dBzA5 t54yvtz3v4A5, 7Bv 9v 9z4Ar3\nyB3z2uv9. Vy r99z3 7Bv r9 v96zxr9 9v3 x8r59 v8xBv3\nuv9uv4y59r3v4Av r trsvtr 6r8r 5 tvB, v47Br4A5 r9\ntyvzr9 r9 srzEr3 6r8r r Av88r, 9Br 3rv.\ncv54r8u5 Ur mz4tz."

def Vector():
    for x in range(48, 58):
        vector.append(x)
    for x in range(65, 91):
        vector.append(x)
    for x in range(97, 123):
        vector.append(x)

def Freq():
    for i in range(0, len(vector)):
        freq.append(0)

def ReadFile():
    f = open("./texto_cifrado.txt", "r")
    return f

def GetCaracter(a):
    for i in range(0, len(vector)):
        if (ord(a) == vector[i]):
            return i
    return -1

def printVector():
    for i in range(0, len(vector)):
        print (i, chr(vector[i]))

def FindK(texto):
    texto_cifrado = texto
    for palavra in texto_cifrado:
        for letra in palavra:
            if(letra != None and letra != " " and letra != "\n"):
                position = GetCaracter(letra)
                if(position != -1):
                    freq[position] += 1

    maior = 0
    for i in range(0, len(freq)):
        if(freq[i] > freq[maior]):
            maior = i
    k = maior - 36 #-a
    print("k ", k)
    return k

def Decrypt(k):
    print("Decripting...")
    texto_cifrado = ReadFile()
    new_text = ""
    for palavra in texto_cifrado:
        for letra in palavra:
            if(letra != None):
                if(letra == " " or letra == "\n" or letra =="."):
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
    Freq()
    output = open("texto_cifrado.txt", "w")
    n = output.write(text)
    output.close()

    k = FindK(ReadFile())
    Decrypt(k)

main()
