from urllib.parse import urlparse, parse_qs
import hashlib
import sys
sys.path.insert(1, '../src/')
import common_data as cd
import AES as aes
import random

DEBUG = True

def GetClientKey(id_c, clients):
    for i in range(len(clients)):
            if(id_c == clients[i].id_c):
                print("Client registered ", clients[i].id_c)
                return clients[i].kc
    print("Client not Found")
    return False

def ReadM1(path, clients):
    #M1 = [ID_C + {ID_S + T_R + N1}Kc]
    query_components = parse_qs(urlparse(path).query)
    id_c = query_components["id_c"][0]
    msg = query_components["msg"][0]

    clientKey = GetClientKey(id_c, clients)
    r = {'status': False, 'data': "Client Not Found"}

    if(clientKey is not False):
        msg = aes.DecryptMsg(msg, clientKey)
        if(msg is False):
            r = {'status': False, 'data': "Key incorrect or message corrupted"}
        else:
            service, time_requested, n1 = msg.split(',')
            if(DEBUG):
                print("Reading in M1: ")
                print("\tid_c: ", id_c)
                print("\tservice: ", service)
                print("\ttime_requested(h): ", time_requested)
                print("\tn1: ", n1)
                print("\tclientKey: ", clientKey)
            r = {'status': True, 'data': {'id_c': id_c, 'service': service, 'time_requested': time_requested, 'n1': n1, 'clientKey': clientKey}}

    return r

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    #print(result)
    return result[:16]

def GenerateK_C_TGS():
    n = random.randint(0, 10000)
    k = str(n)
    k = md5Hash(k)
    return k

def GenerateTGSTicket(id_c, time_requested, k_c_tgs, k_tgs):
    #T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    msg = aes.EncryptMsg(id_c + ',' + time_requested + ',' + k_c_tgs, k_tgs)
    return msg

def CreateM2(id_c, service, time_requested, n1, kc):
    #[{K_c_tgs + N_1}Kc + T_c_tgs]
    #Onde T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    k_c_tgs = GenerateK_C_TGS()
    m2_1 = aes.EncryptMsg(k_c_tgs + ',' + n1, kc)
    cd.defK_TGS()
    k_tgs = cd.getK_TGS()
    m2_2 = GenerateTGSTicket(id_c, time_requested, k_c_tgs, k_tgs)
    if(DEBUG):
        print("Creating in M2: ")
        # print("\tk_c_tgs: ", k_c_tgs)
        # print("\tn1: ", n1)
        # print("\tkc: ", kc)
        print("\tm2_1: ")
        print("\t\tciphertext: ", m2_1['ciphertext'])
        print("\t\ttag: ", m2_1['tag'])
        print("\t\tnonce: ", m2_1['nonce'])
        print("\tm2_2: ")
        print("\t\tciphertext: ", m2_2['ciphertext'])
        print("\t\ttag: ", m2_2['tag'])
        print("\t\tnonce: ", m2_2['nonce'])

    msg = {'m2_1': m2_1, 'm2_2': m2_2}
    return msg

'''
from urllib.parse import urlparse, parse_qs
import hashlib
import sys
sys.path.insert(1, '../src/')
import common_data as cd
import AES as aes
import random

DEBUG = True

def GetClientKey(id_c, clients):
    for i in range(len(clients)):
            if(id_c == clients[i].id_c):
                print("Client registered ", clients[i].id_c)
                return clients[i].kc
    print("Client not Found")
    return False

def ReadM1(path, clients):
    #M1 = [ID_C + {ID_S + T_R + N1}Kc]
    query_components = parse_qs(urlparse(path).query)
    id_c = query_components["id_c"][0]
    msg = query_components["msg"][0]

    clientKey = GetClientKey(id_c, clients)
    r = {'status': False, 'data': "Client Not Found"}

    if(clientKey is not False):
        msg = aes.DecryptMsg(msg, clientKey)
        if(msg is False):
            r = {'status': False, 'data': "Key incorrect or message corrupted"}
        else:
            service, time_requested, n1 = msg.split(',')
            if(DEBUG):
                print("Reading in M1: ")
                print("\tid_c: ", id_c)
                print("\tservice: ", service)
                print("\ttime_requested(h): ", time_requested)
                print("\tn1: ", n1)
                print("\tclientKey: ", clientKey)
            r = {'status': True, 'data': {'id_c': id_c, 'service': service, 'time_requested': time_requested, 'n1': n1, 'clientKey': clientKey}}

    return r

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    #print(result)
    return result[:16]

def GenerateK_C_TGS():
    n = random.randint(0, 1000)
    k = md5Hash(str(n))
    return k

def GenerateTGSTicket(id_c, time_requested, k_c_tgs, k_tgs):
    #T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    msg = aes.EncryptMsg(id_c + ',' + time_requested + ',' + k_c_tgs, k_tgs)
    return msg

def CreateM2(id_c, service, time_requested, n1, kc):
    #[{K_c_tgs + N_1}Kc + T_c_tgs]
    #Onde T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    k_c_tgs = GenerateK_C_TGS()
    m2_1 = aes.EncryptMsg(k_c_tgs + ',' + n1, kc)
    k_tgs = cd.getK_TGS()
    m2_2 = GenerateTGSTicket(id_c, time_requested, k_c_tgs, k_tgs)
    if(DEBUG):
        print("Creating in M2: ")
        # print("\tk_c_tgs: ", k_c_tgs)
        # print("\tn1: ", n1)
        # print("\tkc: ", kc)
        print("\tm2_1: ")
        print("\t\tciphertext: ", m2_1['ciphertext'])
        print("\t\ttag: ", m2_1['tag'])
        print("\t\tnonce: ", m2_1['nonce'])
        print("\tm2_2: ")
        print("\t\tciphertext: ", m2_2['ciphertext'])
        print("\t\ttag: ", m2_2['tag'])
        print("\t\tnonce: ", m2_2['nonce'])

    msg = {'m2_1': m2_1, 'm2_2': m2_2}
    return msg
'''
