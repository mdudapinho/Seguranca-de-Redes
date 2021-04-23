"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################             Client               ################
##################################################################
"""
import random
import os
import client_operations as co
import messages_operations as mo
import hashlib
import sys
sys.path.insert(1, './src/')
import file_operations as fo

DEBUG = False
# file = "./src/clients.txt"
users = []

class User:
    def __init__(self, user, hashed_password):
        self.user = user
        self.hashed_password = hashed_password

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    #print(result)
    return result[:16]

def AddUser(users):
    print("Adding user: Please, enter the following informations")
    user = (input("User:\n"))
    hashed_password = md5Hash((input("Password:\n")))
    new_user = User(user, hashed_password)
    users.append(new_user)
    fo.saveUserInFile(new_user)
    print("User added!")
    return users

def Login(users):
    print("Login")
    if(DEBUG):
        return {'id_c': "client1", 'k_c': "eee4c8d070139c84"}

    user_input = input("User:")
    pass_input = input("Password:")

    for i in range(len(users)):
        if(user_input == users[i].user and md5Hash(pass_input) == users[i].hashed_password):
            print("User checked!")
            return {'id_c': users[i].user, 'k_c': users[i].hashed_password}

    print("Something went wrong! Please check you user and password.")
    return False

def ClientToAS(client_id, service_id, time_requested, kc, n1):
    message1 = mo.CreateM1(client_id, service_id, time_requested, kc, n1)
    print("Sending request to AS. wait for response")
    responseAS = co.ClientToASRequest(message1)

    status = False
    data = False

    if(responseAS["status"] is False):
        data = "Error in AS Server: " + responseAS["message"]
        print(data)
    else:
        r2 = mo.ReadM2(responseAS["message"], kc)

        if(r2['status'] is False):
            data = r2['data']
            print("Error in AS Response: ", data)
        else:
            k_c_tgs = r2['data']['k_c_tgs']
            n1_ = r2['data']['n1_']
            m2_2 = r2['data']['m2_2']

            if(mo.CheckResponse(n1, n1_) is False):
                data = "Error in AS Response: n1 = ", n1, " ::: n1 received =  ", n1_
                print("Error in AS Response: n1 = ", n1, " ::: n1 received =  ", n1_)
            else:
                print("AS Response checked!")
                status = True
                data = {'k_c_tgs': k_c_tgs, 'm2_2': m2_2}

    r = {'status': status, 'data': data}
    return r

def ClienttoTGS(client_id, service_id, time_requested, k_c_tgs, m2_2):
    n2 = random.randint(0, 1000)
    message3 = mo.CreateM3(client_id, service_id, time_requested, k_c_tgs, m2_2, n2)
    print("Sending request to TGS. wait for response")
    responseTGS = co.ClientToTGSRequest(message3)

    status = False
    data = False

    if(responseTGS["status"] is False):
        data = responseTGS["message"]
        print(responseTGS["message"])
    else:
        r4 = mo.ReadM4(responseTGS["message"], k_c_tgs)
        if(r4['status'] is False):
            data = "Error in TGS Response: " + r4['data']
            print(data)
        else:
            k_c_s = r4['data']['k_c_s']
            t_a = r4['data']['t_a']
            n2_ = r4['data']['n2_']
            t_c_s = r4['data']['t_c_s']

            if(mo.CheckResponse(n2, n2_) is False):
                data = "Error in TGS Response: n2 = ", n2, " ::: n2 received =  ", n2_
                print(data)
            else:
                print("TGS Response checked!")
                status = True
                data = {'k_c_s': k_c_s, 't_a': t_a, 't_c_s': t_c_s}

    r = {'status': status, 'data': data}
    return r

def ClientToService(id_c, t, s_r, k_c_s, t_c_s):
    n3 = random.randint(0, 1000)
    message5 = mo.CreateM5(id_c, t, s_r, n3, k_c_s, t_c_s)
    print("Sending request to SS. wait for response")
    responseSS = co.ClientToServiceRequest(message5)

    status = False
    data = False

    if(responseSS["status"] is False):
        data = responseSS["message"]
        print(responseSS["message"])
    else:
        r6 = mo.ReadM6(responseSS["message"], k_c_s)
        if(r6['status'] is False):
            data = "Error in SS Response: " + r6['data']
            print(data)
        else:
            response = r6['data']['response']
            n3_ = r6['data']['n3']
            if(mo.CheckResponse(n3, n3_) is False):
                data = "Error in SS Response: n3 = ", n3, " ::: n3 received =  ", n3_
                print(data)
            else:
                print("SS Response checked!")
                status = True
                data = response

    r = {'status': status, 'data': data}
    return r

def main():
    print("--Client--")
    users = fo.readUserFromFile()

    if(len(users) == 0):
        print("There's no user resgistered yet")
        users = AddUser(users)
        os.system('clear')

    r = False
    while(not r):
        for i in range(len(users)):
            print('id_c:-' + users[i].user)

        input_ = input("1 - Login / 2 - Add New User")
        if(int(input_) == 1 ):
            r = Login(users)
        else:
            users = AddUser(users)

    os.system('clear')

    client_id = r['id_c']
    kc = r['k_c']
    service_id, time_requested, n1 = mo.getDataM1()

    input("Press to start ClientToAS function")
    responseAS = ClientToAS(client_id, service_id, time_requested, kc, n1)
    if(responseAS["status"]):
        k_c_tgs = responseAS["data"]["k_c_tgs"]
        m2_2 = responseAS["data"]["m2_2"]

        input("Press to start ClienttoTGS function")
        responseTGS = ClienttoTGS(client_id, service_id, time_requested, k_c_tgs, m2_2)
        if(responseTGS["status"]):
            k_c_s = responseTGS["data"]["k_c_s"]
            t_a = responseTGS["data"]["t_a"]
            t_c_s = responseTGS["data"]["t_c_s"]

            s_r = service_id #service requested
            input("Press to start ClientToService function")
            responseSS = ClientToService(client_id, t_a, s_r, k_c_s, t_c_s)

            if(responseSS['status'] is not False):
                print("response: ", responseSS['data'])

    print("the end")

main()
