import random
from urllib.parse import urlparse, parse_qs
import sys
sys.path.insert(1, './src/')
import AES as aes
import file_operations as fo
from datetime import datetime, timedelta

# id_c = "client1"
# service_ = "service_1"
f_year_ = 0
f_month_ = 0
f_day_ = 1
f_hour_ = 1

# TEST = True

def defineRequestTime():
    now = datetime.now()
    print ("Today's date & time: ", str(now))
    print ("Requested time:")

    f_year = int(input("year:"))
    f_month = int(input("month:"))
    f_day = int(input("day:"))
    f_hour = int(input("hour:"))

    future_date = timedelta(days = f_day + 30 * f_month + 365 * f_year, hours = f_hour)

    hours =  (f_day + 30 * f_month + 365 * f_year)*24 + f_hour
    print('Time requested: ', future_date)

    return str(hours)

def getDataM1():
    services = fo.ReadServicesFileFromUser()
    for i in range(len(services)):
        print("service: ", services[i])

    service = input("Service:")

    time_requested = defineRequestTime()
    n1 = random.randint(0, 1000)
    return service, time_requested, n1

def CreateM1(client, service, time_requested, kc, n1):
    #M1 = [ID_C + {ID_S + T_R + N1}Kc]
    msg = service + "," + time_requested + "," + str(n1)
    msg = aes.EncryptMsg(msg, kc)
    message = {'id_c': client, 'msg': msg}

    print("\t|creating M1")
    print("\t|\tid_c: ", client)
    # print("\t{ID_S + T_R + N1}Kc: ", msg)
    print("\t|\t{ID_S + T_R + N1}Kc: ")
    print("\t|\t\tciphertext: ", msg['ciphertext'])
    print("\t|\t\ttag: ", msg['tag'])
    print("\t|\t\tnonce: ", msg['nonce'])

    return message

def ReadM2(r, kc):
    #[{K_c_tgs + N_1}Kc + T_c_tgs]
    #Onde T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    #m2_1 = {K_c_tgs + N_1}Kc
    #m2_2 = T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    m2_1 = str(r["m2_1"])
    m2_1 = aes.DecryptMsg(m2_1, kc)

    res = {'status': False, 'data': "Key incorrect or message corrupted"}

    if(m2_1 is not False):
        row = m2_1.split(',')
        k_c_tgs, n1 = [i.strip() for i in row]
        m2_2 = r["m2_2"]

        # if(True):
        print("\t|Receveid in M2: ")
        print("\t|\tk_c_tgs: ", k_c_tgs)
        print("\t|\tn1: ", n1)
        print("\t|\tm2_2: ")
        print("\t|\t\tciphertext: ", m2_2['ciphertext'])
        print("\t|\t\ttag: ", m2_2['tag'])
        print("\t|\t\tnonce: ", m2_2['nonce'])

        res = {'status': True, 'data':{'k_c_tgs': k_c_tgs, 'n1_': n1, 'm2_2': m2_2}}
    return res

def CheckResponse(n_send, n_received):
    if(str(n_send) == n_received):
        return True
    return False

def CreateM3(client_id, service_id, time_requested, k_c_tgs, t_c_tgs, n2):
    #M3 = [{ID_C + ID_S + T_R + N2 }K_c_tgs + T_c_tgs]
    m3_1 = client_id + "," + service_id + "," + time_requested + "," + str(n2)
    m3_1 = aes.EncryptMsg(m3_1, k_c_tgs)
    m3_2 = t_c_tgs

    # if(True):
    print("\t|Creating M3: ")
    print("\t|\tm3_1: ")
    print("\t|\t\tciphertext: ", m3_1['ciphertext'])
    print("\t|\t\ttag: ", m3_1['tag'])
    print("\t|\t\tnonce: ", m3_1['nonce'])
    print("\t|\tm3_2: ")
    print("\t|\t\tciphertext: ", m3_2['ciphertext'])
    print("\t|\t\ttag: ", m3_2['tag'])
    print("\t|\t\tnonce: ", m3_2['nonce'])

    msg = {'m3_1': m3_1, 'm3_2': m3_2}

    return msg

def ReadM4(r, k_c_tgs):
    # M4 = [{K_c_s + T_A + N2}K_c_tgs + T_c_s]
    #Onde T_c_s = {ID_C + T_A + K_c_s}K_s
    #m4_1 = k_c_s + ',' + t_a + ',' + n2
    #m4_1 = EncryptMsg(m4_1, k_c_tgs)
    #m4_2 = GenerateServiceTicket(id_c, t_a, k_c_s, k_s)

    m4_1 = str(r["m4_1"])
    m4_1 = aes.DecryptMsg(m4_1, k_c_tgs)

    res = {'status': False, 'data': "Key incorrect or message corrupted"}

    if(m4_1 is not False):
        row = m4_1.split(',')
        print('m4_1:', row)
        k_c_s, t_a, n2 = [i.strip() for i in row]
        m4_2 = r["m4_2"] #t_c_s
        t_c_s = m4_2

        # if(DEBUG):
        print("\t|Reading in M4: ")
        print("\t|\tk_c_s: ", k_c_s)
        print("\t|\tt_a: ", t_a)
        print("\t|\tn2: ", n2)
        print("\t|\tt_c_s(m4_2): ")
        print("\t|\t\tciphertext: ", t_c_s['ciphertext'])
        print("\t|\t\ttag: ", t_c_s['tag'])
        print("\t|\t\tnonce: ", t_c_s['nonce'])

        res = {'status': True, 'data':{'k_c_s': k_c_s, 't_a': t_a, 'n2_': n2, 't_c_s': t_c_s}}

    return res

def CreateM5(client_id, t_a, s_r, n3, k_c_s, t_c_s):
    # M5 = [{ID_C + (T_A ou T_R) + S_R + N3}K_c_s + T_c_s]
    m5_1 = client_id + "," + t_a + "," + s_r + "," + str(n3)
    m5_1 = aes.EncryptMsg(m5_1, k_c_s)
    m5_2 = t_c_s

    # if(DEBUG):
    print("\t|Creating M5: ")
    print("\t|\tm5_1: ")
    print("\t|\t\tciphertext: ", m5_1['ciphertext'])
    print("\t|\t\ttag: ", m5_1['tag'])
    print("\t|\t\tnonce: ", m5_1['nonce'])
    print("\t|\tm5_2: ")
    print("\t|\t\tciphertext: ", m5_2['ciphertext'])
    print("\t|\t\ttag: ", m5_2['tag'])
    print("\t|\t\tnonce: ", m5_2['nonce'])

    msg = {'m5_1': m5_1, 'm5_2': m5_2}

    return msg

def ReadM6(msg, k_c_s):
    # M6 = [{Resposta, N3}K_c_s]
    msg = str(msg)
    m6 = aes.DecryptMsg(msg, k_c_s)
    r = {'status': False, 'data': "Key incorrect or message corrupted"}

    if(m6 is not False):
        row = m6.split(',')
        response, n3 = [i.strip() for i in row]

        # if(DEBUG):
        print("\t|Reading in M6: ")
        print("\t|\tresponse: ", response)
        print("\t|\tn3: ", n3)
        r = {'status': True, 'data':{'response': response, 'n3': n3}}

    return r
