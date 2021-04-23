from urllib.parse import urlparse, parse_qs
import sys
sys.path.insert(1, '../src/')
import common_data as cd
import AES as aes
from datetime import datetime, date


DEBUG = True

def CheckService(id_s, services):
    for i in range(len(services)):
        if(id_s == services[i]):
            print("service registered ", services[i])
            return True
    return False

def CheckClients(c1, c2):
    if(c1 == c2):
        return True
    return False

def CheckTime(t, t_):
    if(t == t_):
        return True
    return False

def CheckVerification(t_a):
    now = datetime.now()
    t_a = datetime.strptime(t_a, '%m/%d/%Y %H:%M:%S')
    # t_a = t_a.strftime("%m/%d/%Y, %H:%M:%S")
    print("datetime now: ", now)
    print("Authorized acces until:", t_a)
    # t_a = datetime.fromisoformat(t_a)
    r = t_a > now
    print("Access Authorized:", r)
    return r

def DegenerateServiceTicket(t_c_s, k_s):
    #T_c_s = {ID_C + T_A + K_c_s}K_s
    t_c_s_dec = aes.DecryptMsg(t_c_s, k_s)

    status = False
    data = False

    if(t_c_s_dec is False):
        data = "Key incorrect or message corrupted"
    else:
        try:
            row = t_c_s_dec.split(',')
            id_c, time_a, k_c_s = [i.strip() for i in row]
            status = True
            data = {'id_c': id_c, 't_a': time_a, 'k_c_s': k_c_s}
        except:
            data = "Ticket Invalid"

    return {'status': status, 'data': data}

def ReadM5(path, services):
    # M5 = [{ID_C + (T_A ou T_R) + S_R + N3}K_c_s + T_c_s]
    #Onde T_c_s = {ID_C + T_A + K_c_s}K_s
    # m5_1 = client_id + "," + t + "," + s_r + "," + str(n3)
    # m5_1 = EncryptMsg(m3_1, k_c_s)
    # m5_2 = t_c_s

    query_components = parse_qs(urlparse(path).query)
    m5_1 = query_components["m5_1"][0]
    m5_2 = query_components["m5_2"][0]

    # if(DEBUG):
    #     print("m5_1:", m5_1)
    #     print("m5_2:", m5_2)

    k_s = cd.getK_S()
    t_c_s = DegenerateServiceTicket(m5_2, k_s)

    # if(DEBUG):
    #     print("t_c_s:", t_c_s)

    status = False
    data = False

    if(t_c_s["status"] is False):
        data = t_c_s["data"]
    else:
        #{'id_c': id_c, 'time_a': time_a, 'k_c_s': k_c_s}
        id_c = t_c_s['data']['id_c']
        t_a = t_c_s['data']['t_a']
        k_c_s = t_c_s['data']['k_c_s']

        msg = aes.DecryptMsg(m5_1, k_c_s)
        if(msg is False):
            data = "Key incorrect or message corrupted"
        else:
            # {ID_C + (T_A ou T_R) + S_R + N3}K_c_s
            client_id, t, s_r, n3 = msg.split(',')

            if(DEBUG):
                print("Reading M5:")
                print("\tid_c:", id_c)
                print("\tt_a:", t_a)
                print("\tk_c_s:", k_c_s)

                print("\tclient_id:", client_id)
                print("\tt:", t)
                print("\ts_r:", s_r)
                print("\tn3:", n3)

            servicechek = CheckService(s_r, services)
            if(servicechek is False):
                data = "Service not Found"
            elif(CheckClients(id_c, client_id) is False):
                data = "Client is diferent from Ticket"
            elif(CheckTime(t_a, t) is False):
                data = "Time is diferent from Ticket"
            else:
                status = True
                data = {'n3': n3, 'k_c_s': k_c_s, 't_a': t_a}

    return {'status': status, 'data': data}

def CreateM6(n3, k_c_s, t_a):
    # M6 = [{Resposta, N3}K_c_s]

    response = "Request Denied"
    if(CheckVerification(t_a) is not False):
        response = "Request Authorized"

    msg = response + ',' + n3
    msg = aes.EncryptMsg(msg, k_c_s)

    if(DEBUG):
        print("Creating in M6: ")
        print("\tM6: ")
        print("\t\tciphertext: ", msg['ciphertext'])
        print("\t\ttag: ", msg['tag'])
        print("\t\tnonce: ", msg['nonce'])

    return msg
