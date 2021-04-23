from urllib.parse import urlparse, parse_qs
import sys
sys.path.insert(1, '../src/')
import common_data as cd
import AES as aes
from datetime import datetime, timedelta
import hashlib
import random

DEBUG = True

def CheckService(id_s, services):
    for i in range(len(services)):
        if(id_s == services[i]):
            print("service registered ", services[i])
            return True
    return False

def GenerateK_C_S():
    n = random.randint(0, 10000)
    k = str(n)
    k = md5Hash(k)
    return k

def DegenerateTGSTicket(t_c_tgs, k_tgs):
    #T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    print("t_c_tgs:", t_c_tgs)
    print("k_tgs:", k_tgs)
    t_c_tgs_dec = aes.DecryptMsg(t_c_tgs, k_tgs)

    status = False
    data = False

    if(t_c_tgs_dec is False):
        data = "Key incorrect or message corrupted"
    else:
        try:
            row = t_c_tgs_dec.split(',')
            id_c, time_requested, k_c_tgs = [i.strip() for i in row]
            status = True
            data = {'id_c': id_c, 'time_requested': time_requested, 'k_c_tgs': k_c_tgs}
        except:
            data = "Ticket Invalid"

    return {'status': status, 'data': data}

def CheckClients(c1, c2):
    if(c1 == c2):
        return True
    return False

def ReadM3(path, services):
    #M3 = [{ID_C + ID_S + T_R + N2 }K_c_tgs + T_c_tgs]
    #m3_1 = client_id + "," + service_id + "," + time_requested + "," + str(n2)
    #m3_1 = EncryptMsg(m3_1, k_c_tgs)
    #m3_2 = t_c_tgs
    #Onde T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    #msg = {'m3_1': m3_1, 'm3_2': m3_2}
    query_components = parse_qs(urlparse(path).query)
    m3_1 = query_components["m3_1"][0]
    m3_2 = query_components["m3_2"][0]

    if(DEBUG):
        print("\tm3_1: ", m3_1)
        # print("\t\tciphertext: ", m3_1['ciphertext'])
        # print("\t\ttag: ", m3_1['tag'])
        # print("\t\tnonce: ", m3_1['nonce'])
        print("\tm3_2: ", m3_2)
        # print("\t\tciphertext: ", m3_2['ciphertext'])
        # print("\t\ttag: ", m3_2['tag'])
        # print("\t\tnonce: ", m3_2['nonce'])

    k_tgs = cd.getK_TGS()
    t_c_tgs = DegenerateTGSTicket(m3_2, k_tgs)

    if(DEBUG):
        print("t_c_tgs:", t_c_tgs)

    status = False
    data = False

    if(t_c_tgs["status"] is False):
        data = t_c_tgs["data"]
    else:
        #'data': {id_c, time_requested, k_c_tgs}
        # id_c, time_requested, k_c_tgs = t_c_tgs["data"]
        id_c = t_c_tgs["data"]["id_c"]
        time_requested = t_c_tgs["data"]["time_requested"]
        k_c_tgs = t_c_tgs["data"]["k_c_tgs"]
        msg = aes.DecryptMsg(m3_1, k_c_tgs)

        if(msg is False):
            data = "Key incorrect or message corrupted"
        else:
            client_id, service_id, time_requested_, n2 = msg.split(',')

            if(DEBUG):
                print("Reading M3:")
                print("\tk_tgs:", k_tgs)
                print("\tid_c:", id_c)
                print("\ttime_requested:", time_requested)
                print("\tk_c_tgs:", k_c_tgs)
                print("\tclient_id:", client_id)
                print("\tservice_id:", service_id)
                print("\ttime_requested_:", time_requested_)
                print("\tn2:", n2)

            servicechek = CheckService(service_id, services)
            if(servicechek is False):
                data = "Service not Found"
            elif(CheckClients(id_c, client_id) is False):
                data = "Client is diferent from Ticket"
            else:
                #{k_tgs, id_c, time_requested, k_c_tgs, n2, serviceKey}
                #{       id_c, n2, k_c_tgs, serviceKey, time_requested}
                cd.defK_S()
                k_s = cd.getK_S()
                status = True
                data = {'id_c': id_c, 'n2': n2, 'k_c_tgs': k_c_tgs, 'k_s': k_s, 'time_requested': time_requested}

    return {'status': status, 'data': data}

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    #print(result)
    return result[:16]

def GenerateK_C_S():
    n = random.randint(0, 1000)
    k = md5Hash(str(n))
    return k

def GenerateServiceTicket(id_c, time_a, k_c_s, k_s):
    #T_c_s = {ID_C + T_A + K_c_s}K_s
    msg = aes.EncryptMsg(id_c + ',' + time_a + ',' + k_c_s, k_s)
    return msg

def AuthorizedTime(time_requested):
    now = datetime.now()
    print("datetime now: ", now)
    time_requested = timedelta(hours = int(time_requested))
    authorized_time = now + time_requested
    authorized_time = authorized_time.strftime("%m/%d/%Y %H:%M:%S")
    print("Access Authorized until :", authorized_time)
    return authorized_time

def CreateM4(id_c, n2, k_c_tgs, k_s, time_requested):
    #M4 = [{K_c_s + T_A + N2}K_c_tgs + T_c_s]
    #Onde T_c_s = {ID_C + T_A + K_c_s}K_s
    k_c_s = GenerateK_C_S()
    t_a = AuthorizedTime(time_requested)

    m4_1 = k_c_s + ',' + t_a + ',' + n2
    m4_1 = aes.EncryptMsg(m4_1, k_c_tgs)
    m4_2 = GenerateServiceTicket(id_c, t_a, k_c_s, k_s)

    if(DEBUG):
        print("Creating in M4: ")
        print("\tm4_1: ")
        print("\t\tciphertext: ", m4_1['ciphertext'])
        print("\t\ttag: ", m4_1['tag'])
        print("\t\tnonce: ", m4_1['nonce'])
        print("\tm4_2: ")
        print("\t\tciphertext: ", m4_2['ciphertext'])
        print("\t\ttag: ", m4_2['tag'])
        print("\t\tnonce: ", m4_2['nonce'])

    msg4 = {'m4_1': m4_1, 'm4_2': m4_2}
    return msg4
