"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################               APP                ################
##################################################################
"""
import os
import hashlib
import datetime

users = []
file = "./file.txt"

class User:
    def __init__(self, user, local_password, seed_password):
        self.user = user
        self.local_password = local_password
        self.seed_password = seed_password
        self.tokens = []

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    return result[:8]

def readFromFile():
    fh = open(file).readlines()
    for line in fh:
        row = line.split(',')
        user_, local_password_, seed_password_ = [i.strip() for i in row]
        new_user = User(user_, local_password_, seed_password_)
        users.append(new_user)

def generateToken(hs_seed):
    x = datetime.datetime.now()

    #year, month, day, hour, minute
    password = hs_seed + str(x.year) + str(x.month) + str(x.day) + str(x.hour) + str(x.minute)
    s0 = md5Hash(password)
    s1 = md5Hash(s0)
    s2 = md5Hash(s1)
    s3 = md5Hash(s2)
    s4 = md5Hash(s3)

    # creating list
    tokens = [[s0, True], [s1, True], [s2, True], [s3, True], [s4, True]]
    return tokens

def checkTime(this_minute):
    x = datetime.datetime.now().minute
    if(x == this_minute):
        return False
    return True

def Login():
    this_minute = datetime.datetime.now().minute
    for i in range(len(users)):
        users[i].tokens = generateToken(users[i].seed_password)

    while(True):
        checked = False
        user_input = (raw_input("User:"))
        local_input = (raw_input("Token:"))

        if(checkTime(this_minute)):
            this_minute = (this_minute + 1) % 60
            for i in range(len(users)):
                users[i].tokens = generateToken(users[i].seed_password)

        for i in range(len(users)):
            if(user_input == users[i].user):
                for j in range(len(users[i].tokens)):
                    if(local_input == users[i].tokens[j][0] and users[i].tokens[j][1]):
                        checked = True
                        for k in range(j, len(users[i].tokens)):
                            users[i].tokens[k][1] = False

        if(checked):
            print("User and key valid for this minute!")
        else:
            print("Something went wrong! Please check your user and key.")


def main():
    print("--App--")
    readFromFile()

    if(len(users) == 0):
        print("There's no user registered!")
    else:
        os.system('clear')
        print("Login")
        Login()

main()
