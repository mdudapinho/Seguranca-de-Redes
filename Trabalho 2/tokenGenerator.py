"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################         TOKEN GENERATOR          ################
##################################################################
"""
import os
import hashlib
import json
import datetime

users = []
file = "./file.txt"

class User:
    def __init__(self, user, local_password, seed_password):
        self.user = user
        self.local_password = local_password
        self.seed_password = seed_password

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    #print(result)
    return result[:8]

def saveInFile(user):
    f = open(file,'a')
    f.write(user.user + ', ')
    f.write(user.local_password + ', ')
    f.write(user.seed_password + '\n')
    f.close()

def readFromFile():
    fh = open(file).readlines()
    for line in fh:
        row = line.split(',')
        user_, local_password_, seed_password_ = [i.strip() for i in row]
        new_user = User(user_, local_password_, seed_password_)
        users.append(new_user)

def AddUser():
    print("Please, enter the following informations")
    user = (raw_input("User:\n"))
    local_password = md5Hash((raw_input("Local password:\n")))
    seed_password = md5Hash((raw_input("Seed password:\n")))

    new_user = User(user, local_password, seed_password)
    users.append(new_user)
    saveInFile(new_user)

def generateToken(hs_seed):

    raw_input("Press any button to generate your tokens")

    x = datetime.datetime.now()
    #year, month, day, hour, minute
    password = hs_seed + str(x.year) + str(x.month) + str(x.day) + str(x.hour) + str(x.minute)

    print("Time now: " + str(x) + "\nThe following tokens are the acceptable for this minute")

    s0 = md5Hash(password)
    s1 = md5Hash(s0)
    s2 = md5Hash(s1)
    s3 = md5Hash(s2)
    s4 = md5Hash(s3)
    print("\t1 - " + s0)
    print("\t2 - " + s1)
    print("\t3 - " + s2)
    print("\t4 - " + s3)
    print("\t5 - " + s4)

    raw_input("Press any button to continue")

def Login():
    correct = False
    seed = ""
    while(not correct):
        user_input = (raw_input("User:"))
        local_input = (raw_input("Local password:"))

        for i in range(len(users)):
            if(user_input == users[i].user and md5Hash(local_input) == users[i].local_password):
                correct = True
                seed = users[i].seed_password

        if(not correct):
            print("Something went wrong! Please check you user and password.")

    print("User checked!")
    generateToken(seed)


def main():
    print("--Token Generator--")
    readFromFile()

    if(len(users) == 0):
        print("There's no user resgistered yet")
        AddUser()

    while(True):
        os.system('clear')
        opt = int(raw_input("Choose: 1-Login / 2-Add new User\n"))
        if(opt == 1):
            print("Login")
            Login()
        if(opt == 2):
            AddUser()

main()
