import hashlib
import random

K_TGS_file = "../src/K_TGS_file.txt"
K_S_file = "../src/K_S_file.txt"

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    return result[:16]

def defK_TGS():
    n_k_tgs = random.randint(0, 10000)
    k_tgs = md5Hash(str(n_k_tgs))
    f = open(K_TGS_file,'w+')
    f.write(k_tgs)
    f.close()

def defK_S():
    n_k_s = random.randint(0, 10000)
    k_s = md5Hash(str(n_k_s))
    f = open(K_S_file,'w+')
    f.write(k_s)
    f.close()

def getK_TGS():
    k_tgs = open(K_TGS_file).readline()
    return k_tgs

def getK_S():
    k_s = open(K_S_file).readline()
    return k_s
